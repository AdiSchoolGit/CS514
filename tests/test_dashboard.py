from tests.helpers import connect

PLANNED_ROUTES = {
    "GET /",
    "GET /patients",
    "GET /dashboard/<patient_id>",
    "GET /appointments/<patient_id>",
    "POST /appointments",
    "POST /appointments/<appointment_id>/cancel",
    "GET /tasks/<patient_id>",
    "POST /tasks",
    "POST /tasks/<task_id>/complete",
    "POST /tasks/<task_id>/delete",
    "GET /messages/<patient_id>",
    "POST /messages/<message_id>/read",
    "GET /results/<patient_id>",
    "POST /results/<result_id>/review",
    "GET /medications/<patient_id>",
    "GET /api/care-overview/<patient_id>",
}


def normalize(rule):
    replacements = {
        "<int:patient_id>": "<patient_id>",
        "<int:appointment_id>": "<appointment_id>",
        "<int:task_id>": "<task_id>",
        "<int:message_id>": "<message_id>",
        "<int:result_id>": "<result_id>",
    }
    for src, dest in replacements.items():
        rule = rule.replace(src, dest)
    return rule


def test_routes_match_plan(app):
    found = set()
    for rule in app.url_map.iter_rules():
        if rule.endpoint == "static":
            continue
        methods = rule.methods - {"HEAD", "OPTIONS"}
        for method in methods:
            found.add(f"{method} {normalize(rule.rule)}")
    assert found == PLANNED_ROUTES


def test_patient_list(client):
    for path in ("/", "/patients"):
        response = client.get(path)
        assert response.status_code == 200
        page = response.get_data(as_text=True)
        assert "Maya Chen" in page
        assert "Jordan Hale" in page
        assert "Elena Vasquez" in page


def test_dashboard_for_maya(client):
    response = client.get("/dashboard/1")
    assert response.status_code == 200
    page = response.get_data(as_text=True)
    assert "Maya Chen" in page
    assert "Annual visit" in page
    assert "Amira Patel" in page
    assert "Family Medicine" in page
    assert "Complete lab work" in page
    assert "Follow-up visit" in page


def test_missing_patient(client):
    response = client.get("/dashboard/999")
    assert response.status_code == 404
    assert "Patient not found." in response.get_data(as_text=True)


def test_empty_states_for_jordan(client):
    dashboard = client.get("/dashboard/2")
    page = dashboard.get_data(as_text=True)
    assert "No completed visit is on file." in page
    assert "No upcoming appointment." in page
    assert "No open tasks." in page
    messages = client.get("/messages/2").get_data(as_text=True)
    assert "No unread messages" in messages
    results = client.get("/results/2").get_data(as_text=True)
    assert "No test results" in results


def test_care_overview_api(client):
    response = client.get("/api/care-overview/1")
    assert response.status_code == 200
    payload = response.get_json()
    assert payload["overview"]["patient_name"] == "Maya Chen"
    assert payload["overview"]["unread_message_count"] == 1
    assert payload["recent_visit"]["department_name"] == "Family Medicine"
    assert payload["upcoming_appointment"]["reason"] == "Follow-up visit"
    assert payload["tasks_by_priority"]

    missing = client.get("/api/care-overview/999")
    assert missing.status_code == 404
    assert missing.get_json()["error"] == "Patient not found."


def test_care_overview_view_counts(app):
    conn = connect(app)
    maya = conn.execute(
        "SELECT * FROM care_overview_view WHERE patient_id = 1"
    ).fetchone()
    jordan = conn.execute(
        "SELECT * FROM care_overview_view WHERE patient_id = 2"
    ).fetchone()
    elena = conn.execute(
        "SELECT * FROM care_overview_view WHERE patient_id = 3"
    ).fetchone()
    conn.close()

    assert maya["patient_name"] == "Maya Chen"
    assert maya["last_completed_appointment_id"] == 1
    assert maya["next_appointment_id"] == 2
    assert maya["open_task_count"] == 3
    assert maya["overdue_task_count"] == 1
    assert maya["unread_message_count"] == 1
    assert maya["new_result_count"] == 1
    assert maya["active_referral_count"] == 1
    assert maya["refill_due_count"] == 1
    assert maya["open_notification_count"] == 3

    assert jordan["next_appointment_id"] is None
    assert jordan["open_task_count"] == 0
    assert jordan["unread_message_count"] == 0
    assert jordan["new_result_count"] == 0

    assert elena["last_completed_appointment_id"] == 4
    assert elena["next_appointment_id"] == 5
    assert elena["unread_message_count"] == 2
    assert elena["active_referral_count"] == 2
    assert elena["open_task_count"] == 3
