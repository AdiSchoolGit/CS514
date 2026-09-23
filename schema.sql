PRAGMA foreign_keys = ON;

CREATE TABLE patients (
  id INTEGER PRIMARY KEY,
  first_name TEXT NOT NULL,
  last_name TEXT NOT NULL,
  dob TEXT NOT NULL,
  email TEXT NOT NULL UNIQUE,
  phone TEXT,
  created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
);

CREATE TABLE departments (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL UNIQUE,
  phone TEXT
);

CREATE TABLE providers (
  id INTEGER PRIMARY KEY,
  department_id INTEGER NOT NULL REFERENCES departments(id),
  full_name TEXT NOT NULL,
  role TEXT NOT NULL,
  specialty TEXT
);

CREATE TABLE appointments (
  id INTEGER PRIMARY KEY,
  patient_id INTEGER NOT NULL REFERENCES patients(id),
  provider_id INTEGER NOT NULL REFERENCES providers(id),
  department_id INTEGER NOT NULL REFERENCES departments(id),
  starts_at TEXT NOT NULL,
  visit_type TEXT NOT NULL,
  location TEXT NOT NULL,
  reason TEXT NOT NULL,
  status TEXT NOT NULL CHECK (status IN ('scheduled', 'completed', 'cancelled', 'missed')),
  check_in_status TEXT NOT NULL CHECK (check_in_status IN ('not_started', 'available', 'complete', 'not_required')),
  prep_notes TEXT,
  created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
);

CREATE TABLE visit_summaries (
  id INTEGER PRIMARY KEY,
  appointment_id INTEGER NOT NULL UNIQUE REFERENCES appointments(id),
  reason TEXT NOT NULL,
  summary TEXT NOT NULL,
  instructions TEXT,
  medication_changes TEXT,
  follow_up_plan TEXT,
  created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
);

CREATE TABLE follow_up_tasks (
  id INTEGER PRIMARY KEY,
  patient_id INTEGER NOT NULL REFERENCES patients(id),
  visit_summary_id INTEGER REFERENCES visit_summaries(id),
  title TEXT NOT NULL,
  details TEXT,
  task_type TEXT NOT NULL,
  due_at TEXT,
  status TEXT NOT NULL CHECK (status IN ('open', 'complete', 'dismissed')),
  priority TEXT NOT NULL CHECK (priority IN ('low', 'normal', 'high')),
  completed_at TEXT,
  created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
);

CREATE TABLE messages (
  id INTEGER PRIMARY KEY,
  patient_id INTEGER NOT NULL REFERENCES patients(id),
  provider_id INTEGER NOT NULL REFERENCES providers(id),
  subject TEXT NOT NULL,
  body TEXT NOT NULL,
  sent_at TEXT NOT NULL,
  read_at TEXT,
  status TEXT NOT NULL CHECK (status IN ('unread', 'read', 'archived'))
);

CREATE TABLE test_results (
  id INTEGER PRIMARY KEY,
  patient_id INTEGER NOT NULL REFERENCES patients(id),
  provider_id INTEGER NOT NULL REFERENCES providers(id),
  test_name TEXT NOT NULL,
  category TEXT NOT NULL,
  collected_at TEXT NOT NULL,
  released_at TEXT NOT NULL,
  status TEXT NOT NULL CHECK (status IN ('new', 'reviewed', 'archived')),
  value_summary TEXT NOT NULL,
  reviewed_at TEXT
);

CREATE TABLE medications (
  id INTEGER PRIMARY KEY,
  patient_id INTEGER NOT NULL REFERENCES patients(id),
  name TEXT NOT NULL,
  dosage TEXT,
  frequency TEXT,
  started_at TEXT,
  status TEXT NOT NULL CHECK (status IN ('active', 'paused', 'stopped'))
);

CREATE TABLE prescriptions (
  id INTEGER PRIMARY KEY,
  medication_id INTEGER NOT NULL REFERENCES medications(id),
  provider_id INTEGER NOT NULL REFERENCES providers(id),
  pharmacy TEXT,
  refills_remaining INTEGER NOT NULL CHECK (refills_remaining >= 0),
  last_filled_at TEXT,
  next_refill_at TEXT,
  status TEXT NOT NULL CHECK (status IN ('active', 'refill_due', 'expired'))
);

CREATE TABLE referrals (
  id INTEGER PRIMARY KEY,
  patient_id INTEGER NOT NULL REFERENCES patients(id),
  provider_id INTEGER NOT NULL REFERENCES providers(id),
  department_id INTEGER NOT NULL REFERENCES departments(id),
  reason TEXT NOT NULL,
  status TEXT NOT NULL CHECK (status IN ('pending', 'scheduled', 'complete', 'expired')),
  created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
  expires_at TEXT
);

CREATE TABLE notifications (
  id INTEGER PRIMARY KEY,
  patient_id INTEGER NOT NULL REFERENCES patients(id),
  source_type TEXT NOT NULL,
  source_id INTEGER NOT NULL,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  severity TEXT NOT NULL CHECK (severity IN ('info', 'warning', 'high')),
  status TEXT NOT NULL CHECK (status IN ('open', 'dismissed')),
  created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
  dismissed_at TEXT
);

CREATE TABLE quick_access_items (
  id INTEGER PRIMARY KEY,
  label TEXT NOT NULL,
  path TEXT NOT NULL,
  sort_order INTEGER NOT NULL,
  is_active INTEGER NOT NULL CHECK (is_active IN (0, 1))
);

CREATE INDEX idx_appointments_patient_starts ON appointments(patient_id, starts_at);
CREATE INDEX idx_appointments_patient_status ON appointments(patient_id, status);
CREATE INDEX idx_tasks_patient_status_due ON follow_up_tasks(patient_id, status, due_at);
CREATE INDEX idx_messages_patient_status_sent ON messages(patient_id, status, sent_at);
CREATE INDEX idx_results_patient_status_released ON test_results(patient_id, status, released_at);
CREATE INDEX idx_medications_patient_status ON medications(patient_id, status);
CREATE INDEX idx_prescriptions_status_refill ON prescriptions(status, next_refill_at);
CREATE INDEX idx_referrals_patient_status ON referrals(patient_id, status);
CREATE INDEX idx_notifications_patient_status_created ON notifications(patient_id, status, created_at);

CREATE VIEW care_overview_view AS
SELECT
  p.id AS patient_id,
  p.first_name || ' ' || p.last_name AS patient_name,
  (
    SELECT a.id
    FROM appointments a
    JOIN visit_summaries vs ON vs.appointment_id = a.id
    WHERE a.patient_id = p.id AND a.status = 'completed'
    ORDER BY a.starts_at DESC
    LIMIT 1
  ) AS last_completed_appointment_id,
  (
    SELECT a.starts_at
    FROM appointments a
    JOIN visit_summaries vs ON vs.appointment_id = a.id
    WHERE a.patient_id = p.id AND a.status = 'completed'
    ORDER BY a.starts_at DESC
    LIMIT 1
  ) AS last_visit_at,
  (
    SELECT a.id
    FROM appointments a
    WHERE a.patient_id = p.id
      AND a.status = 'scheduled'
      AND a.starts_at > datetime('now', 'localtime')
    ORDER BY a.starts_at ASC
    LIMIT 1
  ) AS next_appointment_id,
  (
    SELECT a.starts_at
    FROM appointments a
    WHERE a.patient_id = p.id
      AND a.status = 'scheduled'
      AND a.starts_at > datetime('now', 'localtime')
    ORDER BY a.starts_at ASC
    LIMIT 1
  ) AS next_appointment_at,
  (
    SELECT COUNT(*)
    FROM follow_up_tasks t
    WHERE t.patient_id = p.id AND t.status = 'open'
  ) AS open_task_count,
  (
    SELECT COUNT(*)
    FROM follow_up_tasks t
    WHERE t.patient_id = p.id
      AND t.status = 'open'
      AND date(t.due_at) < date('now', 'localtime')
  ) AS overdue_task_count,
  (
    SELECT COUNT(*)
    FROM messages m
    WHERE m.patient_id = p.id AND m.status = 'unread'
  ) AS unread_message_count,
  (
    SELECT COUNT(*)
    FROM test_results r
    WHERE r.patient_id = p.id AND r.status = 'new'
  ) AS new_result_count,
  (
    SELECT COUNT(*)
    FROM referrals rf
    WHERE rf.patient_id = p.id AND rf.status IN ('pending', 'scheduled')
  ) AS active_referral_count,
  (
    SELECT COUNT(*)
    FROM prescriptions pr
    JOIN medications med ON med.id = pr.medication_id
    WHERE med.patient_id = p.id AND pr.status = 'refill_due'
  ) AS refill_due_count,
  (
    SELECT COUNT(*)
    FROM notifications n
    WHERE n.patient_id = p.id AND n.status = 'open'
  ) AS open_notification_count
FROM patients p;
