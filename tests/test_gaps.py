import sqlite3

import pytest

import db


def test_get_patients_lists_all_seeded_patients(conn):
    patients = db.get_patients(conn)
    assert len(patients) == 3
    assert all({"id", "first_name", "last_name", "dob"} <= p.keys() for p in patients)


def test_get_patients_sorted_by_last_name(conn):
    last_names = [p["last_name"] for p in db.get_patients(conn)]
    assert last_names == sorted(last_names)


def test_get_patient_returns_none_for_unknown_id(conn):
    assert db.get_patient(conn, 999) is None


def test_get_patient_returns_full_record(conn):
    patient = db.get_patient(conn, 1)
    assert patient["id"] == 1
    assert "email" in patient


def test_get_open_tasks_orders_overdue_first(conn):
    tasks = db.get_open_tasks(conn, 1)
    overdue_flags = [t["is_overdue"] for t in tasks]
    assert overdue_flags == sorted(overdue_flags, reverse=True)


def test_get_open_tasks_only_returns_open_status(conn):
    conn.execute(
        "UPDATE follow_up_tasks SET status = 'dismissed' WHERE patient_id = 1 AND status = 'open'"
    )
    assert db.get_open_tasks(conn, 1) == []


def test_get_quick_access_only_active_items_in_sort_order(conn):
    conn.execute("DELETE FROM quick_access_items")
    conn.execute(
        "INSERT INTO quick_access_items (label, path, sort_order, is_active) VALUES "
        "('Third', '/c', 3, 1), ('First', '/a', 1, 1), ('Hidden', '/b', 2, 0)"
    )
    items = db.get_quick_access(conn)
    assert [i["label"] for i in items] == ["First", "Third"]


def test_get_recent_visit_returns_none_without_completed_appointment(conn):
    conn.execute("UPDATE appointments SET status = 'scheduled' WHERE patient_id = 2")
    assert db.get_recent_visit(conn, 2) is None


def test_get_next_appointment_returns_earliest(conn):
    row = conn.execute(
        "SELECT id FROM appointments WHERE patient_id = 1 AND status = 'scheduled' "
        "ORDER BY starts_at LIMIT 1"
    ).fetchone()
    appt = db.get_next_appointment(conn, 1)
    assert appt is None or appt["id"] == row["id"]


def test_review_result_raises_for_unknown_id(conn):
    with pytest.raises(ValueError):
        db.review_result(conn, 999999)


def test_complete_task_on_already_complete_task_is_a_no_op(conn):
    db.complete_task(conn, 2)
    first_completed_at = conn.execute(
        "SELECT completed_at FROM follow_up_tasks WHERE id = 2"
    ).fetchone()[0]

    db.complete_task(conn, 2)
    second_completed_at = conn.execute(
        "SELECT completed_at FROM follow_up_tasks WHERE id = 2"
    ).fetchone()[0]

    assert first_completed_at == second_completed_at


def test_mark_message_read_on_already_read_message_is_a_no_op(conn):
    db.mark_message_read(conn, 1)
    first_read_at = conn.execute("SELECT read_at FROM messages WHERE id = 1").fetchone()[0]

    db.mark_message_read(conn, 1)
    second_read_at = conn.execute("SELECT read_at FROM messages WHERE id = 1").fetchone()[0]

    assert first_read_at == second_read_at


def test_delete_task_on_unknown_id_does_not_error(conn):
    db.delete_task(conn, 999999)


def test_create_task_with_minimal_arguments(conn):
    task_id = db.create_task(conn, 2, "Minimal task", "form")
    row = conn.execute(
        "SELECT due_at, priority, details, status FROM follow_up_tasks WHERE id = ?", (task_id,)
    ).fetchone()
    assert row["due_at"] is None
    assert row["priority"] == "normal"
    assert row["details"] is None
    assert row["status"] == "open"


def test_appointment_invalid_visit_type_rejected(conn):
    row = conn.execute("SELECT provider_id, department_id FROM appointments LIMIT 1").fetchone()
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute(
            """
            INSERT INTO appointments (patient_id, provider_id, department_id, starts_at, visit_type, reason)
            VALUES (1, ?, ?, '2026-12-01 09:00', 'carrier_pigeon', 'Checkup')
            """,
            (row["provider_id"], row["department_id"]),
        )


def test_test_result_invalid_category_rejected(conn):
    row = conn.execute("SELECT provider_id FROM test_results LIMIT 1").fetchone()
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute(
            """
            INSERT INTO test_results (patient_id, provider_id, test_name, category)
            VALUES (1, ?, 'Mystery panel', 'astrology')
            """,
            (row["provider_id"],),
        )


def test_medication_invalid_status_rejected(conn):
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute(
            "INSERT INTO medications (patient_id, name, status) VALUES (1, 'Test Med', 'on_the_moon')"
        )


def test_referral_requires_known_department(conn):
    row = conn.execute("SELECT provider_id FROM referrals LIMIT 1").fetchone()
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute(
            """
            INSERT INTO referrals (patient_id, provider_id, department_id, reason)
            VALUES (1, ?, 999999, 'Follow-up')
            """,
            (row["provider_id"],),
        )


def test_notification_invalid_severity_rejected(conn):
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute(
            """
            INSERT INTO notifications (patient_id, source_type, source_id, title, severity)
            VALUES (1, 'task', 1, 'Test notice', 'urgent')
            """
        )


def test_quick_access_is_active_must_be_zero_or_one(conn):
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute(
            "INSERT INTO quick_access_items (label, path, sort_order, is_active) VALUES (?, ?, ?, ?)",
            ("Broken", "/broken", 99, 2),
        )


def test_department_name_must_be_unique(conn):
    existing = conn.execute("SELECT name FROM departments LIMIT 1").fetchone()[0]
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute("INSERT INTO departments (name) VALUES (?)", (existing,))


def test_visit_summary_appointment_id_must_be_unique(conn):
    appointment_id = conn.execute(
        "SELECT appointment_id FROM visit_summaries LIMIT 1"
    ).fetchone()[0]
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute(
            "INSERT INTO visit_summaries (appointment_id, summary) VALUES (?, 'Duplicate summary')",
            (appointment_id,),
        )
