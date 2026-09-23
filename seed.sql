PRAGMA foreign_keys = ON;

INSERT INTO patients (id, first_name, last_name, dob, email, phone) VALUES
    (1, 'Maria', 'Alvarez', '1958-04-12', 'maria.alvarez@example.com', '555-0101'),
    (2, 'James', 'Okafor', '1996-11-03', 'james.okafor@example.com', '555-0102'),
    (3, 'Linda', 'Chen', '1971-07-28', 'linda.chen@example.com', '555-0103');

INSERT INTO departments (id, name, phone) VALUES
    (1, 'Family Medicine', '555-0200'),
    (2, 'Cardiology', '555-0201'),
    (3, 'Laboratory', '555-0202'),
    (4, 'Physical Therapy', '555-0203'),
    (5, 'Endocrinology', '555-0204');

INSERT INTO providers (id, department_id, full_name, role, specialty) VALUES
    (1, 1, 'Dr. Sarah Patel', 'Physician', 'Family Medicine'),
    (2, 2, 'Dr. Michael Grant', 'Physician', 'Cardiology'),
    (3, 3, 'Tom Reyes', 'Lab Technician', 'Laboratory'),
    (4, 4, 'Anna Kowalski', 'Physical Therapist', 'Orthopedic Rehab'),
    (5, 5, 'Dr. Helen Brooks', 'Physician', 'Endocrinology'),
    (6, 1, 'Kevin Moore', 'Nurse', 'Family Medicine');

INSERT INTO appointments
    (id, patient_id, provider_id, department_id, starts_at, visit_type, location, reason, status, check_in_status, prep_notes)
VALUES
    (1, 1, 1, 1, datetime('now', '-60 days', 'start of day', '+9 hours'), 'in_person', 'Main Clinic, Room 204', 'Annual checkup', 'completed', 'complete', NULL),
    (2, 1, 2, 2, datetime('now', '-7 days', 'start of day', '+14 hours'), 'in_person', 'Heart Center, Suite 3', 'Blood pressure follow-up', 'completed', 'complete', NULL),
    (3, 1, 2, 2, datetime('now', '+10 days', 'start of day', '+10 hours', '+30 minutes'), 'in_person', 'Heart Center, Suite 3', 'Cardiology follow-up', 'scheduled', 'available', 'Bring your home blood pressure log. Arrive 15 minutes early.'),
    (4, 1, 3, 3, datetime('now', '+3 days', 'start of day', '+8 hours'), 'in_person', 'Lab, 1st Floor', 'Lab work', 'scheduled', 'not_required', 'Do not eat or drink anything except water for 8 hours before.'),
    (5, 2, 1, 1, datetime('now', '-20 days', 'start of day', '+11 hours'), 'telehealth', 'Video visit', 'Seasonal allergies', 'completed', 'complete', NULL),
    (6, 3, 5, 5, datetime('now', '-14 days', 'start of day', '+13 hours'), 'in_person', 'Specialty Clinic, Floor 2', 'Diabetes check-in', 'completed', 'complete', NULL),
    (7, 3, 4, 4, datetime('now', '-30 days', 'start of day', '+15 hours'), 'in_person', 'Rehab Center', 'Knee pain', 'completed', 'complete', NULL),
    (8, 3, 5, 5, datetime('now', '+21 days', 'start of day', '+9 hours'), 'telehealth', 'Video visit', 'Diabetes follow-up', 'scheduled', 'not_started', 'Have your glucose readings ready.'),
    (9, 3, 1, 1, datetime('now', '+5 days', 'start of day', '+16 hours'), 'in_person', 'Main Clinic, Room 110', 'Flu shot', 'cancelled', 'not_started', NULL);

INSERT INTO visit_summaries
    (id, appointment_id, reason, summary, instructions, medication_changes, follow_up_plan)
VALUES
    (1, 1, 'Annual checkup', 'Routine yearly exam. Vitals recorded and care plan reviewed.', 'Continue daily walks.', NULL, 'Return in one year.'),
    (2, 2, 'Blood pressure follow-up', 'Reviewed home blood pressure readings with the care team.', 'Check blood pressure each morning and write it down.', 'Lisinopril dose changed from 10 mg to 20 mg.', 'Complete lab work before the next cardiology visit.'),
    (3, 5, 'Seasonal allergies', 'Discussed seasonal allergy symptoms by video.', 'Use the nasal spray as directed.', 'Started fluticasone nasal spray.', 'Message the office if symptoms continue.'),
    (4, 6, 'Diabetes check-in', 'Reviewed glucose log and current medications.', 'Keep logging glucose before breakfast.', 'No changes.', 'Get A1C lab drawn before the next visit.'),
    (5, 7, 'Knee pain', 'Physical therapy evaluation for right knee.', 'Do the home exercise sheet three times a week.', NULL, 'Schedule four more therapy sessions.');

INSERT INTO follow_up_tasks
    (id, patient_id, visit_summary_id, title, details, task_type, due_at, status, priority, completed_at)
VALUES
    (1, 1, 2, 'Complete lab work', 'Fasting lab work ordered by Dr. Grant.', 'lab', datetime('now', '+3 days'), 'open', 'high', NULL),
    (2, 1, 2, 'Pick up updated prescription', 'Lisinopril 20 mg is ready at your pharmacy.', 'prescription', datetime('now', '-1 days'), 'open', 'high', NULL),
    (3, 1, NULL, 'Review new test result', 'A new result was released to your chart.', 'review_result', datetime('now', '+7 days'), 'open', 'normal', NULL),
    (4, 1, 1, 'Fill out health history form', NULL, 'form', datetime('now', '-50 days'), 'complete', 'low', datetime('now', '-55 days')),
    (5, 3, 5, 'Schedule physical therapy sessions', 'Four more sessions recommended.', 'schedule', datetime('now', '-2 days'), 'open', 'normal', NULL),
    (6, 3, 4, 'Get A1C lab drawn', NULL, 'lab', datetime('now', '+14 days'), 'open', 'normal', NULL),
    (7, 3, NULL, 'Complete endocrinology referral', 'Referral is waiting to be scheduled.', 'referral', datetime('now', '+30 days'), 'open', 'low', NULL);

INSERT INTO messages (id, patient_id, provider_id, subject, body, sent_at, read_at, status) VALUES
    (1, 1, 2, 'Your lab order', 'Hi Maria, your lab order is in. Please remember to fast before your lab appointment.', datetime('now', '-2 days'), NULL, 'unread'),
    (2, 1, 1, 'Result released', 'A new result has been released to your chart. Please review it and message us with any questions.', datetime('now', '-1 days'), NULL, 'unread'),
    (3, 1, 6, 'Appointment reminder', 'This is a reminder about your upcoming cardiology visit.', datetime('now', '-10 days'), datetime('now', '-9 days'), 'read'),
    (4, 2, 1, 'Following up', 'Hi James, just checking in after your video visit.', datetime('now', '-18 days'), datetime('now', '-17 days'), 'read'),
    (5, 3, 5, 'Glucose log', 'Thanks for sending your glucose log. We will review it at your next visit.', datetime('now', '-3 days'), NULL, 'unread');

INSERT INTO test_results
    (id, patient_id, provider_id, test_name, category, collected_at, released_at, status, value_summary, reviewed_at)
VALUES
    (1, 1, 2, 'Basic Metabolic Panel', 'lab', datetime('now', '-8 days'), datetime('now', '-1 days'), 'new', 'Results available. See provider comments.', NULL),
    (2, 1, 1, 'Lipid Panel', 'lab', datetime('now', '-62 days'), datetime('now', '-58 days'), 'reviewed', 'Results available. See provider comments.', datetime('now', '-57 days')),
    (3, 3, 5, 'Hemoglobin A1C', 'lab', datetime('now', '-15 days'), datetime('now', '-12 days'), 'new', 'Results available. See provider comments.', NULL),
    (4, 3, 4, 'Right Knee X-Ray', 'imaging', datetime('now', '-31 days'), datetime('now', '-29 days'), 'reviewed', 'Report available. See provider comments.', datetime('now', '-28 days'));

INSERT INTO medications (id, patient_id, name, dosage, frequency, started_at, status) VALUES
    (1, 1, 'Lisinopril', '20 mg', 'Once daily', date('now', '-7 days'), 'active'),
    (2, 1, 'Atorvastatin', '10 mg', 'Once daily at bedtime', date('now', '-400 days'), 'active'),
    (3, 1, 'Lisinopril', '10 mg', 'Once daily', date('now', '-400 days'), 'stopped'),
    (4, 2, 'Fluticasone nasal spray', '50 mcg', 'One spray each nostril daily', date('now', '-20 days'), 'active'),
    (5, 3, 'Metformin', '500 mg', 'Twice daily with meals', date('now', '-800 days'), 'active'),
    (6, 3, 'Ibuprofen', '400 mg', 'As needed for pain', date('now', '-30 days'), 'paused');

INSERT INTO prescriptions
    (id, medication_id, provider_id, pharmacy, refills_remaining, last_filled_at, next_refill_at, status)
VALUES
    (1, 1, 2, 'Main Street Pharmacy', 3, NULL, date('now'), 'active'),
    (2, 2, 1, 'Main Street Pharmacy', 0, date('now', '-28 days'), date('now', '+2 days'), 'refill_due'),
    (3, 4, 1, 'Campus Pharmacy', 2, date('now', '-20 days'), date('now', '+10 days'), 'active'),
    (4, 5, 5, 'Riverside Pharmacy', 1, date('now', '-25 days'), date('now', '+5 days'), 'refill_due');

INSERT INTO referrals (id, patient_id, provider_id, department_id, reason, status, created_at, expires_at) VALUES
    (1, 3, 1, 4, 'Physical therapy for right knee', 'scheduled', datetime('now', '-35 days'), date('now', '+55 days')),
    (2, 3, 1, 5, 'Endocrinology care', 'pending', datetime('now', '-5 days'), date('now', '+85 days')),
    (3, 1, 1, 2, 'Cardiology follow-up', 'complete', datetime('now', '-40 days'), date('now', '+50 days'));

INSERT INTO notifications (id, patient_id, source_type, source_id, title, body, severity, status, created_at, dismissed_at) VALUES
    (1, 1, 'test_result', 1, 'New test result', 'Basic Metabolic Panel is ready to review.', 'info', 'open', datetime('now', '-1 days'), NULL),
    (2, 1, 'message', 1, 'New message from Dr. Grant', 'Your lab order', 'info', 'open', datetime('now', '-2 days'), NULL),
    (3, 1, 'task', 2, 'Overdue: pick up prescription', 'Lisinopril 20 mg is ready at your pharmacy.', 'warning', 'open', datetime('now'), NULL),
    (4, 1, 'prescription', 2, 'Refill due soon', 'Atorvastatin has no refills left.', 'warning', 'open', datetime('now'), NULL),
    (5, 3, 'test_result', 3, 'New test result', 'Hemoglobin A1C is ready to review.', 'info', 'open', datetime('now', '-12 days'), NULL),
    (6, 3, 'referral', 2, 'Referral needs scheduling', 'Endocrinology referral is pending.', 'info', 'open', datetime('now', '-5 days'), NULL),
    (7, 1, 'test_result', 2, 'New test result', 'Lipid Panel is ready to review.', 'info', 'dismissed', datetime('now', '-58 days'), datetime('now', '-57 days'));

INSERT INTO quick_access_items (id, label, path, sort_order, is_active) VALUES
    (1, 'Schedule an appointment', '/appointments', 1, 1),
    (2, 'Message a provider', '/messages', 2, 1),
    (3, 'Request a refill', '/medications', 3, 1),
    (4, 'View test results', '/results', 4, 1),
    (5, 'Review medications', '/medications', 5, 1),
    (6, 'View visit summaries', '/appointments', 6, 1);
