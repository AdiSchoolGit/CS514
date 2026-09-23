-- Recent visit: most recent completed appointment with its summary, provider, and department
SELECT a.id, a.starts_at, pr.full_name AS provider, d.name AS department,
       vs.reason, vs.summary, vs.instructions, vs.medication_changes, vs.follow_up_plan
FROM appointments a
JOIN visit_summaries vs ON vs.appointment_id = a.id
JOIN providers pr ON pr.id = a.provider_id
JOIN departments d ON d.id = a.department_id
WHERE a.patient_id = :patient_id AND a.status = 'completed'
ORDER BY a.starts_at DESC
LIMIT 1;

-- Upcoming appointment: next scheduled appointment, found with a subquery
SELECT a.id, a.starts_at, a.visit_type, a.location, a.reason, a.check_in_status, a.prep_notes,
       pr.full_name AS provider, d.name AS department
FROM appointments a
JOIN providers pr ON pr.id = a.provider_id
JOIN departments d ON d.id = a.department_id
WHERE a.id = (
    SELECT id FROM appointments
    WHERE patient_id = :patient_id AND status = 'scheduled' AND starts_at > datetime('now')
    ORDER BY starts_at
    LIMIT 1
);

-- Next steps: open tasks, overdue and high priority first
SELECT id, title, details, task_type, due_at, priority,
       due_at < datetime('now') AS is_overdue
FROM follow_up_tasks
WHERE patient_id = :patient_id AND status = 'open'
ORDER BY is_overdue DESC,
         CASE priority WHEN 'high' THEN 1 WHEN 'normal' THEN 2 ELSE 3 END,
         due_at;

-- Important updates: dashboard counts from the view
SELECT * FROM care_overview_view WHERE patient_id = :patient_id;

-- Task priority: open tasks grouped by priority
SELECT priority, COUNT(*) AS task_count
FROM follow_up_tasks
WHERE patient_id = :patient_id AND status = 'open'
GROUP BY priority;

-- Medication refills: active medications with prescription and prescriber
SELECT m.name, m.dosage, m.frequency, rx.pharmacy, rx.refills_remaining,
       rx.next_refill_at, rx.status AS refill_status, pr.full_name AS prescriber
FROM medications m
JOIN prescriptions rx ON rx.medication_id = m.id
JOIN providers pr ON pr.id = rx.provider_id
WHERE m.patient_id = :patient_id AND m.status = 'active'
ORDER BY rx.next_refill_at;

-- Patients with more unread messages than the average patient (subquery in HAVING)
SELECT p.id, p.first_name, p.last_name, COUNT(m.id) AS unread_count
FROM patients p
JOIN messages m ON m.patient_id = p.id AND m.status = 'unread'
GROUP BY p.id
HAVING COUNT(m.id) > (
    SELECT AVG(cnt) FROM (
        SELECT COUNT(*) AS cnt FROM messages WHERE status = 'unread' GROUP BY patient_id
    )
);
