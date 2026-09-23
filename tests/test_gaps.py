import sqlite3

import pytest

import db
from tests.helpers import connect


def test_get_patients_lists_all_seeded_patients(app):
    with app.app_context():
        db.connect(app.config["DB_PATH"])
        patients = db.list_patients()
        db.close()
    assert len(patients) == 3
    assert all({"id", "first_name", "last_name", "dob"} <= set(patient) for patient in patients)


def test_get_patients_sorted_by_last_name(app):
    with app.app_context():
        db.connect(app.config["DB_PATH"])
        last_names = [patient["last_name"] for patient in db.list_patients()]
        db.close()
    assert last_names == sorted(last_names)


def test_get_patient_returns_none_for_unknown_id(app):
    with app.app_context():
        db.connect(app.config["DB_PATH"])
        missing = db.get_patient(999)
        db.close()
    assert missing is None


def test_get_patient_returns_full_record(app):
    with app.app_context():
        db.connect(app.config["DB_PATH"])
        patient = db.get_patient(1)
        db.close()
    assert patient["id"] == 1
    assert patient["email"] == "maya.chen@example.com"


def test_get_open_tasks_orders_overdue_first(app):
    with app.app_context():
        db.connect(app.config["DB_PATH"])
        tasks = db.list_tasks(1, open_only=True)
        db.close()
    assert tasks[0]["is_overdue"] == 1


def test_get_open_tasks_only_returns_open_status(app):
    conn = connect(app)
    conn.execute("UPDATE follow_up_tasks SET status = 'dismissed' WHERE patient_id = 1 AND status = 'open'")
    conn.commit()
    conn.close()
    with app.app_context():
        db.connect(app.config["DB_PATH"])
        tasks = db.list_tasks(1, open_only=True)
        db.close()
    assert tasks == []


def test_get_quick_access_only_active_items_in_sort_order(app):
    conn = connect(app)
    conn.execute("DELETE FROM quick_access_items")
    conn.execute(
        "INSERT INTO quick_access_items (label, path, sort_order, is_active) VALUES "
        "('Third', '/c', 3, 1), ('First', '/a', 1, 1), ('Hidden', '/b', 2, 0)"
    )
    conn.commit()
    conn.close()
    with app.app_context():
        db.connect(app.config["DB_PATH"])
        labels = [item["label"] for item in db.quick_links(1)]
        db.close()
    assert labels == ["First", "Third"]


def test_get_recent_visit_returns_none_without_completed_appointment(app):
    with app.app_context():
        db.connect(app.config["DB_PATH"])
        visit = db.recent_visit(2)
        db.close()
    assert visit is None


def test_get_next_appointment_returns_earliest(app):
    conn = connect(app)
    earliest = conn.execute(
        """
        SELECT id FROM appointments
        WHERE patient_id = 1 AND status = 'scheduled' AND starts_at > datetime('now', 'localtime')
        ORDER BY starts_at
        LIMIT 1
        """
    ).fetchone()["id"]
    conn.close()
    with app.app_context():
        db.connect(app.config["DB_PATH"])
        appointment = db.upcoming_appointment(1)
        db.close()
    assert appointment["id"] == earliest


def test_review_result_raises_for_unknown_id(app):
    with app.app_context():
        db.connect(app.config["DB_PATH"])
        missing = db.review_result(999999)
        db.close()
    assert missing is None


def test_complete_task_on_already_complete_task_is_a_no_op(app):
    with app.app_context():
        db.connect(app.config["DB_PATH"])
        _, outcome = db.complete_task(4)
        db.close()
    assert outcome == "already"


def test_mark_message_read_on_already_read_message_is_a_no_op(app):
    with app.app_context():
        db.connect(app.config["DB_PATH"])
        _, outcome = db.mark_message_read(2)
        db.close()
    assert outcome == "already"


def test_delete_task_on_unknown_id_does_not_error(app):
    with app.app_context():
        db.connect(app.config["DB_PATH"])
        missing = db.delete_task(999999)
        db.close()
    assert missing is None


def test_create_task_with_required_fields(app):
    with app.app_context():
        db.connect(app.config["DB_PATH"])
        task_id = db.create_task(2, "Minimal task", None, "general", "2026-12-15", "normal", None)
        task = db.get_task(task_id)
        db.close()
    assert task["priority"] == "normal"
    assert task["details"] is None
    assert task["status"] == "open"


def test_medication_invalid_status_rejected(app):
    conn = connect(app)
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute("INSERT INTO medications (patient_id, name, status) VALUES (1, 'Test Med', 'on_the_moon')")
    conn.close()


def test_referral_requires_known_department(app):
    conn = connect(app)
    provider_id = conn.execute("SELECT provider_id FROM referrals LIMIT 1").fetchone()[0]
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute(
            """
            INSERT INTO referrals (patient_id, provider_id, department_id, reason, status)
            VALUES (1, ?, 999999, 'Follow-up', 'pending')
            """,
            (provider_id,),
        )
    conn.close()


def test_notification_invalid_severity_rejected(app):
    conn = connect(app)
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute(
            """
            INSERT INTO notifications (
              patient_id, source_type, source_id, title, body, severity, status
            ) VALUES (1, 'task', 1, 'Test notice', 'Body', 'urgent', 'open')
            """
        )
    conn.close()


def test_quick_access_is_active_must_be_zero_or_one(app):
    conn = connect(app)
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute(
            "INSERT INTO quick_access_items (label, path, sort_order, is_active) VALUES (?, ?, ?, ?)",
            ("Broken", "/broken", 99, 2),
        )
    conn.close()


def test_department_name_must_be_unique(app):
    conn = connect(app)
    existing = conn.execute("SELECT name FROM departments LIMIT 1").fetchone()[0]
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute("INSERT INTO departments (name) VALUES (?)", (existing,))
    conn.close()


def test_visit_summary_appointment_id_must_be_unique(app):
    conn = connect(app)
    appointment_id = conn.execute("SELECT appointment_id FROM visit_summaries LIMIT 1").fetchone()[0]
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute(
            "INSERT INTO visit_summaries (appointment_id, reason, summary) VALUES (?, 'Visit', 'Duplicate summary')",
            (appointment_id,),
        )
    conn.close()
