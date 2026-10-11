import re

from tests.helpers import connect


def focus_text(client, patient_id):
    html = client.get(f"/dashboard/{patient_id}").get_data(as_text=True)
    match = re.search(r'class="focus[^"]*".*?</section>', html, re.S)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", match.group(0))).strip()


def clear_tasks(app, patient_id):
    conn = connect(app)
    conn.execute("DELETE FROM follow_up_tasks WHERE patient_id = ?", (patient_id,))
    conn.commit()
    conn.close()


def test_overdue_task_is_the_focus(client):
    text = focus_text(client, 1)
    assert "Do this next" in text
    assert "Update pharmacy information" in text
    assert "Overdue" in text
    assert "Mark done" in text


def test_focus_task_is_not_repeated_in_the_checklist(client):
    html = client.get("/dashboard/1").get_data(as_text=True)
    checklist = html.split('id="steps-heading"')[1]
    assert "Update pharmacy information" not in checklist
    assert "Complete lab work" in checklist


def test_unread_message_is_the_focus_when_no_tasks_are_left(app, client):
    clear_tasks(app, 1)
    text = focus_text(client, 1)
    assert "Lab visit reminder" in text
    assert "Read message" in text


def test_new_result_is_the_focus_after_messages_are_read(app, client):
    clear_tasks(app, 1)
    client.post("/messages/1/read")
    text = focus_text(client, 1)
    assert "Lipid panel" in text
    assert "View result" in text


def test_all_caught_up_when_nothing_is_left(app, client):
    clear_tasks(app, 1)
    client.post("/messages/1/read")
    client.post("/results/1/review")
    clear_tasks(app, 1)
    text = focus_text(client, 1)
    assert "All caught up" in text
    assert "No open tasks." in text


def test_patient_with_no_records_is_caught_up(client):
    assert "All caught up" in focus_text(client, 2)


def test_summary_sentence_counts_everything(client):
    html = client.get("/dashboard/1").get_data(as_text=True)
    assert "You have 3 tasks to do (1 overdue), 1 new message and 1 new result." in html


def test_summary_says_caught_up_for_empty_patient(client):
    assert "You&#39;re all caught up." in client.get("/dashboard/2").get_data(as_text=True)


def test_completing_a_task_can_return_to_the_dashboard(client):
    response = client.post("/tasks/3/complete", data={"next": "/dashboard/1"})
    assert response.headers["Location"].endswith("/dashboard/1")


def test_complete_task_ignores_off_site_redirects(client):
    for target in ("//evil.example", "https://evil.example", "javascript:alert(1)"):
        response = client.post("/tasks/3/complete", data={"next": target})
        assert response.headers["Location"].endswith("/tasks/1")


def test_complete_task_without_next_goes_to_tasks_page(client):
    response = client.post("/tasks/3/complete")
    assert response.headers["Location"].endswith("/tasks/1")
