import os
import sqlite3
from datetime import date, datetime
from pathlib import Path

from flask import g

ROOT = Path(__file__).resolve().parent
DEFAULT_DB = ROOT / "care_overview.db"


def init_db(db_path, quiet=False):
    if os.path.exists(db_path):
        os.remove(db_path)
    conn = sqlite3.connect(db_path)
    try:
        conn.execute("PRAGMA foreign_keys = ON")
        conn.executescript((ROOT / "schema.sql").read_text(encoding="utf-8"))
        conn.executescript((ROOT / "seed.sql").read_text(encoding="utf-8"))
        conn.commit()
        count = conn.execute("SELECT COUNT(*) FROM patients").fetchone()[0]
    except Exception:
        conn.close()
        if os.path.exists(db_path):
            os.remove(db_path)
        raise
    conn.close()
    if not quiet:
        print(f"Database ready at {db_path} with {count} patients.")


def connect(path):
    if "db" not in g:
        conn = sqlite3.connect(path)
        conn.row_factory = sqlite3.Row
        conn.isolation_level = None
        conn.execute("PRAGMA foreign_keys = ON")
        g.db = conn
    return g.db


def close(_exc=None):
    conn = g.pop("db", None)
    if conn is not None:
        conn.close()


def get_db():
    return g.db


def fetch_all(sql, params=()):
    rows = get_db().execute(sql, params).fetchall()
    return [dict(row) for row in rows]


def fetch_one(sql, params=()):
    row = get_db().execute(sql, params).fetchone()
    if row is None:
        return None
    return dict(row)


def execute(sql, params=()):
    conn = get_db()
    try:
        conn.execute("BEGIN IMMEDIATE")
        cursor = conn.execute(sql, params)
        conn.commit()
        return cursor.lastrowid
    except Exception:
        conn.rollback()
        raise


def age_from_dob(dob):
    born = datetime.strptime(dob, "%Y-%m-%d").date()
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


def with_age(patient):
    data = dict(patient)
    data["name"] = f"{data['first_name']} {data['last_name']}"
    data["age"] = age_from_dob(data["dob"])
    return data


def list_patients():
    rows = fetch_all(
        """
        SELECT
          p.id, p.first_name, p.last_name, p.dob, p.email, p.phone,
          v.next_appointment_at, v.open_task_count,
          v.unread_message_count, v.new_result_count
        FROM patients p
        JOIN care_overview_view v ON v.patient_id = p.id
        ORDER BY p.last_name, p.first_name
        """
    )
    return [with_age(row) for row in rows]


def get_patient(patient_id):
    row = fetch_one("SELECT * FROM patients WHERE id = ?", (patient_id,))
    if row is None:
        return None
    return with_age(row)


def care_overview(patient_id):
    return fetch_one(
        "SELECT * FROM care_overview_view WHERE patient_id = ?",
        (patient_id,),
    )


def recent_visit(patient_id):
    return fetch_one(
        """
        SELECT
          a.id,
          a.starts_at,
          a.visit_type,
          a.location,
          pr.full_name AS provider_name,
          pr.role AS provider_role,
          pr.specialty AS provider_specialty,
          d.name AS department_name,
          vs.reason AS visit_reason,
          vs.summary,
          vs.instructions,
          vs.medication_changes,
          vs.follow_up_plan
        FROM appointments a
        JOIN visit_summaries vs ON vs.appointment_id = a.id
        JOIN providers pr ON pr.id = a.provider_id
        JOIN departments d ON d.id = a.department_id
        WHERE a.patient_id = ? AND a.status = 'completed'
        ORDER BY a.starts_at DESC
        LIMIT 1
        """,
        (patient_id,),
    )


def upcoming_appointment(patient_id):
    return fetch_one(
        """
        SELECT
          a.id,
          a.starts_at,
          a.visit_type,
          a.location,
          a.reason,
          a.status,
          a.check_in_status,
          a.prep_notes,
          pr.full_name AS provider_name,
          pr.role AS provider_role,
          d.name AS department_name
        FROM appointments a
        JOIN providers pr ON pr.id = a.provider_id
        JOIN departments d ON d.id = a.department_id
        WHERE a.patient_id = ?
          AND a.status = 'scheduled'
          AND a.starts_at > (SELECT datetime('now', 'localtime'))
        ORDER BY a.starts_at ASC
        LIMIT 1
        """,
        (patient_id,),
    )


def task_counts_by_priority(patient_id):
    return fetch_all(
        """
        SELECT priority, COUNT(*) AS task_count
        FROM follow_up_tasks
        WHERE patient_id = ? AND status = 'open'
        GROUP BY priority
        ORDER BY CASE priority WHEN 'high' THEN 0 WHEN 'normal' THEN 1 ELSE 2 END
        """,
        (patient_id,),
    )


def list_tasks(patient_id, open_only=False):
    return fetch_all(
        """
        SELECT
          t.*,
          a.starts_at AS visit_at,
          CASE
            WHEN t.status = 'open' AND date(t.due_at) < date('now', 'localtime') THEN 1
            ELSE 0
          END AS is_overdue
        FROM follow_up_tasks t
        LEFT JOIN visit_summaries vs ON vs.id = t.visit_summary_id
        LEFT JOIN appointments a ON a.id = vs.appointment_id
        WHERE t.patient_id = ?
          AND (? = 0 OR t.status = 'open')
        ORDER BY CASE t.status WHEN 'open' THEN 0 ELSE 1 END, t.due_at
        """,
        (patient_id, 1 if open_only else 0),
    )


def list_visit_summaries(patient_id):
    return fetch_all(
        """
        SELECT vs.id, a.starts_at, a.reason
        FROM visit_summaries vs
        JOIN appointments a ON a.id = vs.appointment_id
        WHERE a.patient_id = ?
        ORDER BY a.starts_at DESC
        """,
        (patient_id,),
    )


def get_task(task_id):
    return fetch_one("SELECT * FROM follow_up_tasks WHERE id = ?", (task_id,))


def create_task(patient_id, title, details, task_type, due_at, priority, visit_summary_id):
    return execute(
        """
        INSERT INTO follow_up_tasks (
          patient_id, visit_summary_id, title, details, task_type, due_at, status, priority
        ) VALUES (?, ?, ?, ?, ?, ?, 'open', ?)
        """,
        (patient_id, visit_summary_id, title, details, task_type, due_at, priority),
    )


def complete_task(task_id):
    task = get_task(task_id)
    if task is None:
        return None, "missing"
    if task["status"] != "open":
        return task, "already"
    execute(
        """
        UPDATE follow_up_tasks
        SET status = 'complete', completed_at = datetime('now', 'localtime')
        WHERE id = ? AND status = 'open'
        """,
        (task_id,),
    )
    return task, "complete"


def delete_task(task_id):
    task = get_task(task_id)
    if task is None:
        return None
    execute("DELETE FROM follow_up_tasks WHERE id = ?", (task_id,))
    return task


def list_providers():
    return fetch_all(
        """
        SELECT pr.id, pr.full_name, pr.role, pr.specialty, d.name AS department_name
        FROM providers pr
        JOIN departments d ON d.id = pr.department_id
        ORDER BY pr.full_name
        """
    )


def list_departments():
    return fetch_all("SELECT id, name FROM departments ORDER BY name")


def get_provider(provider_id):
    return fetch_one("SELECT * FROM providers WHERE id = ?", (provider_id,))


def get_department(department_id):
    return fetch_one("SELECT * FROM departments WHERE id = ?", (department_id,))


def visit_summary_for_patient(summary_id, patient_id):
    return fetch_one(
        """
        SELECT vs.id
        FROM visit_summaries vs
        JOIN appointments a ON a.id = vs.appointment_id
        WHERE vs.id = ? AND a.patient_id = ?
        """,
        (summary_id, patient_id),
    )


def list_appointments(patient_id):
    return fetch_all(
        """
        SELECT
          a.*,
          pr.full_name AS provider_name,
          pr.role AS provider_role,
          d.name AS department_name
        FROM appointments a
        JOIN providers pr ON pr.id = a.provider_id
        JOIN departments d ON d.id = a.department_id
        WHERE a.patient_id = ?
        ORDER BY
          CASE
            WHEN a.status = 'scheduled' AND a.starts_at > datetime('now', 'localtime') THEN 0
            ELSE 1
          END,
          a.starts_at DESC
        """,
        (patient_id,),
    )


def get_appointment(appointment_id):
    return fetch_one("SELECT * FROM appointments WHERE id = ?", (appointment_id,))


def create_appointment(
    patient_id, provider_id, department_id, starts_at, visit_type, location, reason, prep_notes
):
    check_in = "not_required" if visit_type == "telehealth" else "not_started"
    return execute(
        """
        INSERT INTO appointments (
          patient_id, provider_id, department_id, starts_at, visit_type, location,
          reason, status, check_in_status, prep_notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, 'scheduled', ?, ?)
        """,
        (
            patient_id,
            provider_id,
            department_id,
            starts_at,
            visit_type,
            location,
            reason,
            check_in,
            prep_notes,
        ),
    )


def cancel_appointment(appointment_id):
    appointment = get_appointment(appointment_id)
    if appointment is None:
        return None, "missing"
    if appointment["status"] != "scheduled":
        return appointment, "not_scheduled"
    execute(
        "UPDATE appointments SET status = 'cancelled' WHERE id = ? AND status = 'scheduled'",
        (appointment_id,),
    )
    return appointment, "cancelled"


def reschedule_appointment(appointment_id, starts_at):
    appointment = get_appointment(appointment_id)
    if appointment is None:
        return None, "missing"
    if appointment["status"] != "scheduled":
        return appointment, "not_scheduled"
    execute(
        "UPDATE appointments SET starts_at = ? WHERE id = ? AND status = 'scheduled'",
        (starts_at, appointment_id),
    )
    return appointment, "rescheduled"


def list_messages(patient_id):
    return fetch_all(
        """
        SELECT m.*, pr.full_name AS provider_name, pr.role AS provider_role
        FROM messages m
        JOIN providers pr ON pr.id = m.provider_id
        WHERE m.patient_id = ?
        ORDER BY m.sent_at DESC
        """,
        (patient_id,),
    )


def get_message(message_id):
    return fetch_one("SELECT * FROM messages WHERE id = ?", (message_id,))


def mark_message_read(message_id):
    message = get_message(message_id)
    if message is None:
        return None, "missing"
    if message["status"] != "unread":
        return message, "already"
    execute(
        """
        UPDATE messages
        SET status = 'read', read_at = datetime('now', 'localtime')
        WHERE id = ? AND status = 'unread'
        """,
        (message_id,),
    )
    return message, "read"


def list_results(patient_id):
    return fetch_all(
        """
        SELECT r.*, pr.full_name AS provider_name
        FROM test_results r
        JOIN providers pr ON pr.id = r.provider_id
        WHERE r.patient_id = ?
        ORDER BY r.released_at DESC
        """,
        (patient_id,),
    )


def get_result(result_id):
    return fetch_one("SELECT * FROM test_results WHERE id = ?", (result_id,))


def review_result(result_id):
    result = get_result(result_id)
    if result is None:
        return None
    if result["status"] != "new":
        return {
            "patient_id": result["patient_id"],
            "outcome": "already",
            "task_created": False,
        }

    conn = get_db()
    task_created = False
    try:
        conn.execute("BEGIN IMMEDIATE")
        notice = conn.execute(
            """
            SELECT severity
            FROM notifications
            WHERE source_type = 'test_result' AND source_id = ? AND status = 'open'
            ORDER BY CASE severity WHEN 'high' THEN 0 WHEN 'warning' THEN 1 ELSE 2 END
            LIMIT 1
            """,
            (result_id,),
        ).fetchone()
        conn.execute(
            """
            UPDATE test_results
            SET status = 'reviewed', reviewed_at = datetime('now', 'localtime')
            WHERE id = ? AND status = 'new'
            """,
            (result_id,),
        )
        conn.execute(
            """
            UPDATE notifications
            SET status = 'dismissed', dismissed_at = datetime('now', 'localtime')
            WHERE source_type = 'test_result' AND source_id = ? AND status = 'open'
            """,
            (result_id,),
        )
        if notice is not None and notice["severity"] in ("warning", "high"):
            title = f"Discuss {result['test_name']} with your care team"
            existing = conn.execute(
                """
                SELECT id FROM follow_up_tasks
                WHERE patient_id = ? AND title = ? AND status = 'open'
                """,
                (result["patient_id"], title),
            ).fetchone()
            if existing is None:
                conn.execute(
                    """
                    INSERT INTO follow_up_tasks (
                      patient_id, title, details, task_type, due_at, status, priority
                    ) VALUES (
                      ?, ?, ?, 'result_follow_up', date('now', 'localtime', '+7 days'), 'open', 'normal'
                    )
                    """,
                    (
                        result["patient_id"],
                        title,
                        "Added when this result was marked reviewed.",
                    ),
                )
                task_created = True
        conn.commit()
    except Exception:
        try:
            conn.rollback()
        except sqlite3.Error:
            pass
        raise

    return {
        "patient_id": result["patient_id"],
        "outcome": "reviewed",
        "task_created": task_created,
    }


def list_medications(patient_id):
    return fetch_all(
        """
        SELECT
          m.id,
          m.name,
          m.dosage,
          m.frequency,
          m.started_at,
          m.status,
          pr.pharmacy,
          pr.refills_remaining,
          pr.last_filled_at,
          pr.next_refill_at,
          pr.status AS refill_status,
          pv.full_name AS provider_name
        FROM medications m
        LEFT JOIN prescriptions pr ON pr.medication_id = m.id
        LEFT JOIN providers pv ON pv.id = pr.provider_id
        WHERE m.patient_id = ?
        ORDER BY CASE m.status WHEN 'active' THEN 0 WHEN 'paused' THEN 1 ELSE 2 END, m.name
        """,
        (patient_id,),
    )


def active_referrals(patient_id):
    return fetch_all(
        """
        SELECT r.reason, r.status, d.name AS department_name, pr.full_name AS provider_name
        FROM referrals r
        JOIN departments d ON d.id = r.department_id
        JOIN providers pr ON pr.id = r.provider_id
        WHERE r.patient_id = ? AND r.status IN ('pending', 'scheduled')
        ORDER BY r.created_at DESC
        """,
        (patient_id,),
    )


def open_notifications(patient_id):
    return fetch_all(
        """
        SELECT id, title, body, severity, created_at
        FROM notifications
        WHERE patient_id = ? AND status = 'open'
        ORDER BY created_at DESC
        """,
        (patient_id,),
    )


def get_notification(notification_id):
    return fetch_one("SELECT * FROM notifications WHERE id = ?", (notification_id,))


def dismiss_notification(notification_id):
    notice = get_notification(notification_id)
    if notice is None:
        return None, "missing"
    if notice["status"] != "open":
        return notice, "already"
    execute(
        """
        UPDATE notifications
        SET status = 'dismissed', dismissed_at = datetime('now', 'localtime')
        WHERE id = ? AND status = 'open'
        """,
        (notification_id,),
    )
    return notice, "dismissed"


def quick_links(patient_id):
    rows = fetch_all(
        """
        SELECT label, path
        FROM quick_access_items
        WHERE is_active = 1
        ORDER BY sort_order
        """
    )
    links = []
    for row in rows:
        links.append(
            {
                "label": row["label"],
                "path": row["path"].replace("{patient_id}", str(patient_id)),
            }
        )
    return links


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--init", action="store_true")
    args = parser.parse_args()
    if args.init:
        init_db(DEFAULT_DB)
    else:
        parser.print_help()
