import sqlite3

import pytest

import db


def test_seed_loads(conn):
    assert len(db.get_patients(conn)) == 3


def test_foreign_keys_enforced(conn):
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute("INSERT INTO messages (patient_id, provider_id, subject, body) VALUES (999, 1, 's', 'b')")


def test_not_null_enforced(conn):
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute("INSERT INTO patients (first_name, last_name, dob) VALUES ('A', NULL, '2000-01-01')")


def test_invalid_status_rejected(conn):
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute("UPDATE follow_up_tasks SET status = 'done' WHERE id = 1")


def test_duplicate_email_rejected(conn):
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute("""
            INSERT INTO patients (first_name, last_name, dob, email)
            VALUES ('A', 'B', '2000-01-01', 'maria.alvarez@example.com')
        """)


def test_negative_refills_rejected(conn):
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute("UPDATE prescriptions SET refills_remaining = -1 WHERE id = 1")


def test_overview_counts(conn):
    overview = db.get_overview(conn, 1)
    assert overview["open_task_count"] == 3
    assert overview["overdue_task_count"] == 1
    assert overview["unread_message_count"] == 2
    assert overview["new_result_count"] == 1
    assert overview["refill_due_count"] == 1
    assert overview["open_notification_count"] == 4


def test_sparse_patient_has_empty_overview(conn):
    overview = db.get_overview(conn, 2)
    assert overview["next_appointment_id"] is None
    assert overview["open_task_count"] == 0
    assert overview["unread_message_count"] == 0
    assert db.get_next_appointment(conn, 2) is None


def test_recent_visit_is_latest_completed(conn):
    visit = db.get_recent_visit(conn, 1)
    assert visit["reason"] == "Blood pressure follow-up"
    assert visit["provider"] == "Dr. Michael Grant"


def test_next_appointment_skips_cancelled(conn):
    appt = db.get_next_appointment(conn, 3)
    assert appt["reason"] == "Diabetes follow-up"


def test_complete_task_updates_count(conn):
    db.complete_task(conn, 2)
    overview = db.get_overview(conn, 1)
    assert overview["open_task_count"] == 2
    assert overview["open_notification_count"] == 3


def test_mark_message_read_updates_count(conn):
    db.mark_message_read(conn, 1)
    assert db.get_overview(conn, 1)["unread_message_count"] == 1


def test_review_result_transaction(conn):
    db.review_result(conn, 1, needs_follow_up=True)
    overview = db.get_overview(conn, 1)
    assert overview["new_result_count"] == 0
    assert overview["open_task_count"] == 4
    assert overview["open_notification_count"] == 3


def test_review_result_rolls_back_on_failure(conn):
    conn.execute("DROP TABLE notifications")
    with pytest.raises(sqlite3.OperationalError):
        db.review_result(conn, 1)
    status = conn.execute("SELECT status FROM test_results WHERE id = 1").fetchone()[0]
    assert status == "new"


def test_completed_task_requires_completed_at(conn):
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute("UPDATE follow_up_tasks SET status = 'complete' WHERE id = 1")


def test_delete_task(conn):
    task_id = db.create_task(conn, 2, "Test task", "form")
    db.delete_task(conn, task_id)
    assert conn.execute("SELECT COUNT(*) FROM follow_up_tasks WHERE id = ?", (task_id,)).fetchone()[0] == 0
