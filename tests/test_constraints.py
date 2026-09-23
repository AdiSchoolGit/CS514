import sqlite3

import pytest

from tests.helpers import connect


def test_tables_and_seed_exist(app):
    conn = connect(app)
    tables = {
        row["name"]
        for row in conn.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table'"
        ).fetchall()
    }
    patient_count = conn.execute("SELECT COUNT(*) AS total FROM patients").fetchone()["total"]
    conn.close()
    assert "care_overview_view" not in tables
    assert {
        "patients",
        "departments",
        "providers",
        "appointments",
        "visit_summaries",
        "follow_up_tasks",
        "messages",
        "test_results",
        "medications",
        "prescriptions",
        "referrals",
        "notifications",
        "quick_access_items",
    } <= tables
    assert patient_count == 3

    conn = connect(app)
    view = conn.execute(
        "SELECT name FROM sqlite_master WHERE type = 'view' AND name = 'care_overview_view'"
    ).fetchone()
    conn.close()
    assert view is not None


def test_foreign_key_is_enforced(app):
    conn = connect(app)
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute(
            """
            INSERT INTO appointments (
              patient_id, provider_id, department_id, starts_at, visit_type, location,
              reason, status, check_in_status
            ) VALUES (999, 1, 1, '2026-12-01 09:00:00', 'office', 'Room 1', 'Visit', 'scheduled', 'not_started')
            """
        )
    conn.close()


def test_required_name_rejects_null(app):
    conn = connect(app)
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute(
            "INSERT INTO patients (first_name, last_name, dob, email) VALUES (NULL, 'Test', '2000-01-01', 'test@example.com')"
        )
    conn.close()


def test_invalid_status_fails(app):
    conn = connect(app)
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute(
            """
            INSERT INTO appointments (
              patient_id, provider_id, department_id, starts_at, visit_type, location,
              reason, status, check_in_status
            ) VALUES (1, 1, 1, '2026-12-01 09:00:00', 'office', 'Room 1', 'Visit', 'pending', 'not_started')
            """
        )
    conn.close()


def test_duplicate_email_fails(app):
    conn = connect(app)
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute(
            """
            INSERT INTO patients (first_name, last_name, dob, email)
            VALUES ('Other', 'Person', '1990-01-01', 'maya.chen@example.com')
            """
        )
    conn.close()


def test_negative_refills_fail(app):
    conn = connect(app)
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute(
            """
            INSERT INTO prescriptions (
              medication_id, provider_id, pharmacy, refills_remaining, status
            ) VALUES (1, 1, 'River City Pharmacy', -1, 'active')
            """
        )
    conn.close()
