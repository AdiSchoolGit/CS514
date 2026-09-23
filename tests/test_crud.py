from tests.helpers import connect


def test_create_and_cancel_appointment(client, app):
    created = client.post(
        "/appointments",
        data={
            "patient_id": "2",
            "provider_id": "1",
            "department_id": "1",
            "starts_at": "2026-12-01T09:00",
            "visit_type": "office",
            "location": "Clinic Room 1",
            "reason": "General follow-up",
            "prep_notes": "Bring a medication list.",
        },
        follow_redirects=True,
    )
    assert created.status_code == 200
    assert "General follow-up" in created.get_data(as_text=True)
    assert "Appointment added." in created.get_data(as_text=True)

    conn = connect(app)
    appointment_id = conn.execute(
        "SELECT id FROM appointments WHERE patient_id = 2 AND reason = 'General follow-up'"
    ).fetchone()["id"]
    conn.close()

    cancelled = client.post(
        f"/appointments/{appointment_id}/cancel",
        follow_redirects=True,
    )
    page = cancelled.get_data(as_text=True)
    assert "Appointment cancelled." in page
    assert "Cancelled" in page

    conn = connect(app)
    status = conn.execute(
        "SELECT status FROM appointments WHERE id = ?",
        (appointment_id,),
    ).fetchone()["status"]
    conn.close()
    assert status == "cancelled"


def test_appointment_requires_reason(client):
    response = client.post(
        "/appointments",
        data={
            "patient_id": "1",
            "provider_id": "1",
            "department_id": "1",
            "starts_at": "2026-12-01T09:00",
            "visit_type": "office",
            "location": "Clinic Room 1",
            "reason": "",
        },
    )
    assert response.status_code == 400
    assert "Reason is required." in response.get_data(as_text=True)


def test_create_complete_and_delete_task(client, app):
    created = client.post(
        "/tasks",
        data={
            "patient_id": "2",
            "title": "Pick up forms",
            "details": "Forms are at the front desk.",
            "task_type": "general",
            "due_at": "2026-12-15",
            "priority": "normal",
            "visit_summary_id": "",
        },
        follow_redirects=True,
    )
    assert "Task added." in created.get_data(as_text=True)
    assert "Pick up forms" in created.get_data(as_text=True)

    conn = connect(app)
    task_id = conn.execute(
        "SELECT id FROM follow_up_tasks WHERE patient_id = 2 AND title = 'Pick up forms'"
    ).fetchone()["id"]
    conn.close()

    completed = client.post(f"/tasks/{task_id}/complete", follow_redirects=True)
    assert "Task marked complete." in completed.get_data(as_text=True)

    conn = connect(app)
    overview = conn.execute(
        "SELECT open_task_count FROM care_overview_view WHERE patient_id = 1"
    ).fetchone()
    jordan_open = conn.execute(
        "SELECT COUNT(*) AS total FROM follow_up_tasks WHERE patient_id = 2 AND status = 'open'"
    ).fetchone()["total"]
    conn.close()
    assert overview["open_task_count"] == 3
    assert jordan_open == 0

    removed = client.post("/tasks/1/complete", follow_redirects=True)
    assert "Task marked complete." in removed.get_data(as_text=True)
    conn = connect(app)
    open_count = conn.execute(
        "SELECT open_task_count FROM care_overview_view WHERE patient_id = 1"
    ).fetchone()["open_task_count"]
    conn.close()
    assert open_count == 2

    deleted = client.post("/tasks/3/delete", follow_redirects=True)
    assert "Task deleted." in deleted.get_data(as_text=True)
    conn = connect(app)
    remaining = conn.execute(
        "SELECT id FROM follow_up_tasks WHERE id = 3"
    ).fetchone()
    overdue = conn.execute(
        "SELECT overdue_task_count FROM care_overview_view WHERE patient_id = 1"
    ).fetchone()["overdue_task_count"]
    conn.close()
    assert remaining is None
    assert overdue == 0


def test_task_requires_title(client):
    response = client.post(
        "/tasks",
        data={
            "patient_id": "1",
            "title": "",
            "task_type": "general",
            "due_at": "2026-12-15",
            "priority": "normal",
        },
    )
    assert response.status_code == 400
    assert "Title is required." in response.get_data(as_text=True)


def test_mark_message_read_updates_count(client, app):
    response = client.post("/messages/1/read", follow_redirects=True)
    assert "Message marked read." in response.get_data(as_text=True)
    conn = connect(app)
    unread = conn.execute(
        "SELECT unread_message_count FROM care_overview_view WHERE patient_id = 1"
    ).fetchone()["unread_message_count"]
    conn.close()
    assert unread == 0


def test_review_result_transaction(client, app):
    response = client.post("/results/1/review", follow_redirects=True)
    page = response.get_data(as_text=True)
    assert "Result marked reviewed." in page
    assert "A follow-up task was added." in page

    conn = connect(app)
    result = conn.execute("SELECT status FROM test_results WHERE id = 1").fetchone()
    notice = conn.execute("SELECT status FROM notifications WHERE id = 2").fetchone()
    overview = conn.execute(
        "SELECT * FROM care_overview_view WHERE patient_id = 1"
    ).fetchone()
    task = conn.execute(
        """
        SELECT id FROM follow_up_tasks
        WHERE patient_id = 1 AND title = 'Discuss Lipid panel with your care team'
        """
    ).fetchone()
    conn.close()
    assert result["status"] == "reviewed"
    assert notice["status"] == "dismissed"
    assert overview["new_result_count"] == 0
    assert overview["open_notification_count"] == 2
    assert overview["open_task_count"] == 4
    assert task is not None


def test_review_without_follow_up_task(client, app):
    response = client.post("/results/3/review", follow_redirects=True)
    assert "Result marked reviewed." in response.get_data(as_text=True)
    assert "A follow-up task was added." not in response.get_data(as_text=True)
    conn = connect(app)
    notice = conn.execute("SELECT status FROM notifications WHERE id = 4").fetchone()
    open_tasks = conn.execute(
        "SELECT open_task_count FROM care_overview_view WHERE patient_id = 3"
    ).fetchone()["open_task_count"]
    conn.close()
    assert notice["status"] == "dismissed"
    assert open_tasks == 3


def test_review_rolls_back_when_task_insert_fails(client, app):
    conn = connect(app)
    conn.execute(
        """
        CREATE TRIGGER fail_task_insert
        BEFORE INSERT ON follow_up_tasks
        BEGIN
          SELECT RAISE(ABORT, 'fail');
        END
        """
    )
    conn.commit()
    conn.close()

    response = client.post("/results/1/review", follow_redirects=True)
    assert "could not be reviewed" in response.get_data(as_text=True)

    conn = connect(app)
    status = conn.execute("SELECT status FROM test_results WHERE id = 1").fetchone()["status"]
    note = conn.execute("SELECT status FROM notifications WHERE id = 2").fetchone()["status"]
    conn.close()
    assert status == "new"
    assert note == "open"


def test_reschedule_appointment(client, app):
    conn = connect(app)
    appointment_id = conn.execute(
        "SELECT id FROM appointments WHERE status = 'scheduled' ORDER BY id LIMIT 1"
    ).fetchone()["id"]
    conn.close()

    response = client.post(
        f"/appointments/{appointment_id}/reschedule",
        data={"starts_at": "2026-12-15T14:30"},
        follow_redirects=True,
    )
    assert "Appointment rescheduled." in response.get_data(as_text=True)

    conn = connect(app)
    starts_at = conn.execute(
        "SELECT starts_at FROM appointments WHERE id = ?",
        (appointment_id,),
    ).fetchone()["starts_at"]
    conn.close()
    assert starts_at == "2026-12-15 14:30:00"


def test_reschedule_rejects_bad_date_and_past_visits(client, app):
    conn = connect(app)
    scheduled_id = conn.execute(
        "SELECT id FROM appointments WHERE status = 'scheduled' ORDER BY id LIMIT 1"
    ).fetchone()["id"]
    completed_id = conn.execute(
        "SELECT id FROM appointments WHERE status = 'completed' ORDER BY id LIMIT 1"
    ).fetchone()["id"]
    conn.close()

    bad = client.post(
        f"/appointments/{scheduled_id}/reschedule",
        data={"starts_at": "not a date"},
        follow_redirects=True,
    )
    assert "Enter a valid date and time." in bad.get_data(as_text=True)

    done = client.post(
        f"/appointments/{completed_id}/reschedule",
        data={"starts_at": "2026-12-15T14:30"},
        follow_redirects=True,
    )
    assert "Only scheduled appointments can be rescheduled." in done.get_data(as_text=True)

    missing = client.post("/appointments/9999/reschedule", data={"starts_at": "2026-12-15T14:30"})
    assert missing.status_code == 404


def test_dismiss_notification_updates_count(client, app):
    conn = connect(app)
    before = conn.execute(
        "SELECT open_notification_count FROM care_overview_view WHERE patient_id = 1"
    ).fetchone()[0]
    conn.close()

    response = client.post("/notifications/1/dismiss", follow_redirects=True)
    assert "Notification dismissed." in response.get_data(as_text=True)

    conn = connect(app)
    notice = conn.execute("SELECT status, dismissed_at FROM notifications WHERE id = 1").fetchone()
    after = conn.execute(
        "SELECT open_notification_count FROM care_overview_view WHERE patient_id = 1"
    ).fetchone()[0]
    conn.close()
    assert notice["status"] == "dismissed"
    assert notice["dismissed_at"] is not None
    assert after == before - 1

    again = client.post("/notifications/1/dismiss", follow_redirects=True)
    assert "Notification is already dismissed." in again.get_data(as_text=True)
    assert client.post("/notifications/9999/dismiss").status_code == 404
