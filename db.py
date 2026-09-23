import sqlite3
import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "care_overview.db"


def connect(path=DB_PATH):
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(path=DB_PATH):
    conn = connect(path)
    conn.executescript((BASE_DIR / "schema.sql").read_text())
    conn.executescript((BASE_DIR / "seed.sql").read_text())
    conn.close()


def fetch_one(conn, sql, params=()):
    row = conn.execute(sql, params).fetchone()
    return dict(row) if row else None


def fetch_all(conn, sql, params=()):
    return [dict(row) for row in conn.execute(sql, params).fetchall()]


def get_patients(conn):
    return fetch_all(conn, "SELECT id, first_name, last_name, dob FROM patients ORDER BY last_name")


def get_patient(conn, patient_id):
    return fetch_one(conn, "SELECT * FROM patients WHERE id = ?", (patient_id,))


def get_overview(conn, patient_id):
    return fetch_one(conn, "SELECT * FROM care_overview_view WHERE patient_id = ?", (patient_id,))


def get_recent_visit(conn, patient_id):
    return fetch_one(conn, """
        SELECT a.id, a.starts_at, pr.full_name AS provider, d.name AS department,
               vs.reason, vs.summary, vs.instructions, vs.medication_changes, vs.follow_up_plan
        FROM appointments a
        JOIN visit_summaries vs ON vs.appointment_id = a.id
        JOIN providers pr ON pr.id = a.provider_id
        JOIN departments d ON d.id = a.department_id
        WHERE a.patient_id = ? AND a.status = 'completed'
        ORDER BY a.starts_at DESC
        LIMIT 1
    """, (patient_id,))


def get_next_appointment(conn, patient_id):
    return fetch_one(conn, """
        SELECT a.id, a.starts_at, a.visit_type, a.location, a.reason, a.check_in_status,
               a.prep_notes, pr.full_name AS provider, d.name AS department
        FROM appointments a
        JOIN providers pr ON pr.id = a.provider_id
        JOIN departments d ON d.id = a.department_id
        WHERE a.id = (
            SELECT id FROM appointments
            WHERE patient_id = ? AND status = 'scheduled' AND starts_at > datetime('now')
            ORDER BY starts_at
            LIMIT 1
        )
    """, (patient_id,))


def get_open_tasks(conn, patient_id):
    return fetch_all(conn, """
        SELECT id, title, details, task_type, due_at, priority,
               due_at < datetime('now') AS is_overdue
        FROM follow_up_tasks
        WHERE patient_id = ? AND status = 'open'
        ORDER BY is_overdue DESC,
                 CASE priority WHEN 'high' THEN 1 WHEN 'normal' THEN 2 ELSE 3 END,
                 due_at
    """, (patient_id,))


def get_quick_access(conn):
    return fetch_all(conn, """
        SELECT label, path FROM quick_access_items WHERE is_active = 1 ORDER BY sort_order
    """)


def create_task(conn, patient_id, title, task_type, due_at=None, priority="normal", details=None):
    with conn:
        cur = conn.execute("""
            INSERT INTO follow_up_tasks (patient_id, title, task_type, due_at, priority, details)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (patient_id, title, task_type, due_at, priority, details))
    return cur.lastrowid


def complete_task(conn, task_id):
    with conn:
        conn.execute("""
            UPDATE follow_up_tasks SET status = 'complete', completed_at = datetime('now')
            WHERE id = ? AND status = 'open'
        """, (task_id,))
        dismiss_notifications(conn, "task", task_id)


def delete_task(conn, task_id):
    with conn:
        conn.execute("DELETE FROM follow_up_tasks WHERE id = ?", (task_id,))


def mark_message_read(conn, message_id):
    with conn:
        conn.execute("""
            UPDATE messages SET status = 'read', read_at = datetime('now')
            WHERE id = ? AND status = 'unread'
        """, (message_id,))
        dismiss_notifications(conn, "message", message_id)


def review_result(conn, result_id, needs_follow_up=False):
    with conn:
        result = fetch_one(conn, "SELECT patient_id, test_name FROM test_results WHERE id = ?", (result_id,))
        if result is None:
            raise ValueError(f"No test result with id {result_id}")
        conn.execute("""
            UPDATE test_results SET status = 'reviewed', reviewed_at = datetime('now')
            WHERE id = ?
        """, (result_id,))
        dismiss_notifications(conn, "test_result", result_id)
        if needs_follow_up:
            conn.execute("""
                INSERT INTO follow_up_tasks (patient_id, title, task_type, due_at, priority)
                VALUES (?, ?, 'message', datetime('now', '+7 days'), 'normal')
            """, (result["patient_id"], f"Ask your provider about {result['test_name']}"))


def dismiss_notifications(conn, source_type, source_id):
    conn.execute("""
        UPDATE notifications SET status = 'dismissed', dismissed_at = datetime('now')
        WHERE source_type = ? AND source_id = ? AND status = 'open'
    """, (source_type, source_id))


if __name__ == "__main__":
    if "--init" in sys.argv:
        init_db()
        print(f"Database created at {DB_PATH}")
    else:
        print("Usage: python db.py --init")
