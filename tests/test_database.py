import sqlite3

import pytest

import db
from tests.helpers import connect


def test_seed_loads(app):
    conn = connect(app)
    count = conn.execute("SELECT COUNT(*) FROM patients").fetchone()[0]
    conn.close()
    assert count == 3


def test_foreign_keys_enforced(app):
    conn = connect(app)
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute(
            """
            INSERT INTO messages (patient_id, provider_id, subject, body, sent_at, status)
            VALUES (999, 1, 's', 'b', '2026-01-01 00:00:00', 'unread')
            """
        )
    conn.close()


def test_not_null_enforced(app):
    conn = connect(app)
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute(
            "INSERT INTO patients (first_name, last_name, dob, email) VALUES ('A', NULL, '2000-01-01', 'a@example.com')"
        )
    conn.close()


def test_invalid_status_rejected(app):
    conn = connect(app)
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute("UPDATE follow_up_tasks SET status = 'done' WHERE id = 1")
    conn.close()


def test_duplicate_email_rejected(app):
    conn = connect(app)
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute(
            """
            INSERT INTO patients (first_name, last_name, dob, email)
            VALUES ('A', 'B', '2000-01-01', 'maya.chen@example.com')
            """
        )
    conn.close()


def test_negative_refills_rejected(app):
    conn = connect(app)
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute("UPDATE prescriptions SET refills_remaining = -1 WHERE id = 1")
    conn.close()


def test_overview_counts(app):
    with app.app_context():
        db.connect(app.config["DB_PATH"])
        overview = db.care_overview(1)
        db.close()
    assert overview["open_task_count"] == 3
    assert overview["overdue_task_count"] == 1
    assert overview["unread_message_count"] == 1
    assert overview["new_result_count"] == 1
    assert overview["refill_due_count"] == 1
    assert overview["open_notification_count"] == 3


def test_sparse_patient_has_empty_overview(app):
    with app.app_context():
        db.connect(app.config["DB_PATH"])
        overview = db.care_overview(2)
        upcoming = db.upcoming_appointment(2)
        db.close()
    assert overview["next_appointment_id"] is None
    assert overview["open_task_count"] == 0
    assert overview["unread_message_count"] == 0
    assert upcoming is None


def test_recent_visit_is_latest_completed(app):
    with app.app_context():
        db.connect(app.config["DB_PATH"])
        visit = db.recent_visit(1)
        db.close()
    assert visit["visit_reason"] == "Annual visit"
    assert visit["provider_name"] == "Amira Patel"


def test_next_appointment_is_soonest_scheduled(app):
    with app.app_context():
        db.connect(app.config["DB_PATH"])
        appointment = db.upcoming_appointment(3)
        db.close()
    assert appointment["reason"] == "Endocrinology follow-up"


def test_complete_task_updates_count(app):
    with app.app_context():
        db.connect(app.config["DB_PATH"])
        db.complete_task(1)
        overview = db.care_overview(1)
        db.close()
    assert overview["open_task_count"] == 2


def test_mark_message_read_updates_count(app):
    with app.app_context():
        db.connect(app.config["DB_PATH"])
        db.mark_message_read(1)
        overview = db.care_overview(1)
        db.close()
    assert overview["unread_message_count"] == 0


def test_review_result_transaction(app):
    with app.app_context():
        db.connect(app.config["DB_PATH"])
        outcome = db.review_result(1)
        overview = db.care_overview(1)
        db.close()
    assert outcome["task_created"] is True
    assert overview["new_result_count"] == 0
    assert overview["open_task_count"] == 4
    assert overview["open_notification_count"] == 2


def test_review_result_rolls_back_on_failure(app):
    conn = connect(app)
    conn.execute("DROP TABLE notifications")
    conn.commit()
    conn.close()
    with app.app_context():
        db.connect(app.config["DB_PATH"])
        with pytest.raises(sqlite3.OperationalError):
            db.review_result(1)
        status = db.fetch_one("SELECT status FROM test_results WHERE id = 1")["status"]
        db.close()
    assert status == "new"


def test_delete_task(app):
    with app.app_context():
        db.connect(app.config["DB_PATH"])
        task_id = db.create_task(2, "Test task", None, "general", "2026-12-15", "normal", None)
        db.delete_task(task_id)
        remaining = db.get_task(task_id)
        db.close()
    assert remaining is None
