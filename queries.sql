-- Recent visit: join appointments, visit summaries, providers, and departments.
-- Returns the most recent completed visit for one patient.
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
WHERE a.patient_id = ?
  AND a.status = 'completed'
ORDER BY a.starts_at DESC
LIMIT 1;

-- Upcoming appointment: subquery filters to appointments after the current time.
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
  d.name AS department_name
FROM appointments a
JOIN providers pr ON pr.id = a.provider_id
JOIN departments d ON d.id = a.department_id
WHERE a.patient_id = ?
  AND a.status = 'scheduled'
  AND a.starts_at > (SELECT datetime('now', 'localtime'))
ORDER BY a.starts_at ASC
LIMIT 1;

-- Important updates: aggregate counts from care_overview_view.
SELECT
  patient_id,
  patient_name,
  open_task_count,
  overdue_task_count,
  unread_message_count,
  new_result_count,
  active_referral_count,
  refill_due_count,
  open_notification_count
FROM care_overview_view
WHERE patient_id = ?;

-- Task priority: group open tasks by priority.
SELECT priority, COUNT(*) AS task_count
FROM follow_up_tasks
WHERE patient_id = ? AND status = 'open'
GROUP BY priority
ORDER BY CASE priority WHEN 'high' THEN 0 WHEN 'normal' THEN 1 ELSE 2 END;

-- Medication refill: join medications, prescriptions, and providers.
SELECT
  m.name,
  m.dosage,
  m.frequency,
  m.status AS medication_status,
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
ORDER BY CASE m.status WHEN 'active' THEN 0 WHEN 'paused' THEN 1 ELSE 2 END, m.name;

-- Review result transaction.
-- Run these statements in one transaction and roll back if any step fails.
-- Insert the follow-up task only when the related notification severity is warning or high.
UPDATE test_results
SET status = 'reviewed', reviewed_at = datetime('now', 'localtime')
WHERE id = ? AND status = 'new';

UPDATE notifications
SET status = 'dismissed', dismissed_at = datetime('now', 'localtime')
WHERE source_type = 'test_result' AND source_id = ? AND status = 'open';

INSERT INTO follow_up_tasks (
  patient_id, title, details, task_type, due_at, status, priority
) VALUES (
  ?, ?, ?, 'result_follow_up', date('now', 'localtime', '+7 days'), 'open', 'normal'
);
