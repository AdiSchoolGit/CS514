INSERT INTO departments (id, name, phone) VALUES
  (1, 'Family Medicine', '555-0101'),
  (2, 'Cardiology', '555-0102'),
  (3, 'Endocrinology', '555-0103'),
  (4, 'Rehabilitation', '555-0104'),
  (5, 'Laboratory', '555-0105');

INSERT INTO providers (id, department_id, full_name, role, specialty) VALUES
  (1, 1, 'Amira Patel', 'Physician', 'Family Medicine'),
  (2, 2, 'Luis Ortega', 'Physician', 'Cardiology'),
  (3, 3, 'Naomi Brooks', 'Physician', 'Endocrinology'),
  (4, 4, 'Jordan Kim', 'Physical Therapist', 'Rehabilitation'),
  (5, 5, 'Riley Nguyen', 'Clinical Lab Scientist', 'Laboratory');

INSERT INTO patients (id, first_name, last_name, dob, email, phone) VALUES
  (1, 'Maya', 'Chen', '1988-04-12', 'maya.chen@example.com', '555-0142'),
  (2, 'Jordan', 'Hale', '2001-11-03', 'jordan.hale@example.com', '555-0177'),
  (3, 'Elena', 'Vasquez', '1956-07-22', 'elena.vasquez@example.com', '555-0194');

INSERT INTO appointments (
  id, patient_id, provider_id, department_id, starts_at, visit_type, location, reason, status, check_in_status, prep_notes
) VALUES
  (
    1, 1, 1, 1,
    datetime('now', 'localtime', '-18 days', 'start of day', '+9 hours'),
    'office', 'Clinic Room 2', 'Annual visit', 'completed', 'complete', NULL
  ),
  (
    2, 1, 1, 1,
    datetime('now', 'localtime', '+12 days', 'start of day', '+10 hours', '+30 minutes'),
    'office', 'Clinic Room 2', 'Follow-up visit', 'scheduled', 'not_started',
    'Arrive 15 minutes early and bring your medication list.'
  ),
  (
    3, 3, 2, 2,
    datetime('now', 'localtime', '-30 days', 'start of day', '+14 hours'),
    'office', 'Heart Clinic Room 4', 'Cardiology follow-up', 'completed', 'complete', NULL
  ),
  (
    4, 3, 4, 4,
    datetime('now', 'localtime', '-10 days', 'start of day', '+11 hours'),
    'office', 'Therapy Room B', 'Physical therapy visit', 'completed', 'complete', NULL
  ),
  (
    5, 3, 3, 3,
    datetime('now', 'localtime', '+20 days', 'start of day', '+15 hours'),
    'telehealth', 'Video visit', 'Endocrinology follow-up', 'scheduled', 'not_required',
    'Join the video visit a few minutes before the start time.'
  ),
  (
    6, 3, 2, 2,
    datetime('now', 'localtime', '+40 days', 'start of day', '+13 hours', '+30 minutes'),
    'office', 'Heart Clinic Room 4', 'Cardiology follow-up', 'scheduled', 'not_started',
    'Bring the home blood pressure log.'
  );

INSERT INTO visit_summaries (
  id, appointment_id, reason, summary, instructions, medication_changes, follow_up_plan
) VALUES
  (
    1, 1, 'Annual visit',
    'The note covers home blood pressure readings and routine lab work.',
    'Continue the medications already on your list and come back for the follow-up visit.',
    'No medication changes were recorded at this visit.',
    'Complete lab work and keep the follow-up appointment.'
  ),
  (
    2, 3, 'Cardiology follow-up',
    'The note covers the heart clinic visit and the home blood pressure log.',
    'Bring the home blood pressure log to the next visit.',
    'No medication changes were recorded at this visit.',
    'Keep the next cardiology appointment.'
  ),
  (
    3, 4, 'Physical therapy visit',
    'The note covers the therapy exercises reviewed at this visit.',
    'Continue the home exercises listed by the therapist.',
    'No medication changes were recorded at this visit.',
    'Keep the therapy schedule already on file.'
  );

INSERT INTO follow_up_tasks (
  id, patient_id, visit_summary_id, title, details, task_type, due_at, status, priority, completed_at
) VALUES
  (
    1, 1, 1, 'Complete lab work',
    'Go to the lab listed for the tests ordered at the last visit.',
    'lab', date('now', 'localtime', '+3 days'), 'open', 'high', NULL
  ),
  (
    2, 1, 1, 'Schedule follow-up',
    'Keep the follow-up visit already on the appointment list, or add one if it is missing.',
    'appointment', date('now', 'localtime', '+7 days'), 'open', 'normal', NULL
  ),
  (
    3, 1, NULL, 'Update pharmacy information',
    'Check that the pharmacy name on your medications page is current.',
    'medication', date('now', 'localtime', '-2 days'), 'open', 'low', NULL
  ),
  (
    4, 1, 1, 'Read visit instructions',
    'Read the instructions on the recent visit summary.',
    'general', date('now', 'localtime', '-20 days'), 'complete', 'normal',
    datetime('now', 'localtime', '-16 days')
  ),
  (
    5, 3, 2, 'Bring home blood pressure log',
    'Bring the log to the next cardiology visit.',
    'general', date('now', 'localtime', '+5 days'), 'open', 'high', NULL
  ),
  (
    6, 3, 3, 'Continue therapy exercises',
    'Follow the home exercise list from the therapy visit.',
    'referral', date('now', 'localtime', '+15 days'), 'open', 'normal', NULL
  ),
  (
    7, 3, NULL, 'Confirm specialist visit',
    'Check the time of the upcoming video visit.',
    'appointment', date('now', 'localtime', '+18 days'), 'open', 'low', NULL
  );

INSERT INTO messages (id, patient_id, provider_id, subject, body, sent_at, read_at, status) VALUES
  (
    1, 1, 1, 'Lab visit reminder',
    'The lab can draw the ordered tests before your follow-up visit. This message is a reminder only.',
    datetime('now', 'localtime', '-1 days'), NULL, 'unread'
  ),
  (
    2, 1, 1, 'Visit summary available',
    'The summary from your family medicine visit is ready on the overview page.',
    datetime('now', 'localtime', '-17 days'),
    datetime('now', 'localtime', '-16 days'),
    'read'
  ),
  (
    3, 3, 2, 'Cardiology visit note',
    'A note from your heart clinic visit is available.',
    datetime('now', 'localtime', '-9 days'), NULL, 'unread'
  ),
  (
    4, 3, 3, 'Upcoming video visit',
    'Your endocrinology visit is a video visit. The appointment page lists the time.',
    datetime('now', 'localtime', '-2 days'), NULL, 'unread'
  ),
  (
    5, 3, 4, 'Therapy visit summary',
    'The physical therapy visit summary is available.',
    datetime('now', 'localtime', '-9 days'),
    datetime('now', 'localtime', '-8 days'),
    'read'
  );

INSERT INTO test_results (
  id, patient_id, provider_id, test_name, category, collected_at, released_at, status, value_summary, reviewed_at
) VALUES
  (
    1, 1, 5, 'Lipid panel', 'lab',
    datetime('now', 'localtime', '-3 days'),
    datetime('now', 'localtime', '-1 days'),
    'new',
    'The care team released this result. The portal stores the summary only and does not add an interpretation.',
    NULL
  ),
  (
    2, 1, 5, 'Complete blood count', 'lab',
    datetime('now', 'localtime', '-20 days'),
    datetime('now', 'localtime', '-18 days'),
    'reviewed',
    'The care team released this result. The portal stores the summary only and does not add an interpretation.',
    datetime('now', 'localtime', '-16 days')
  ),
  (
    3, 3, 5, 'Basic metabolic panel', 'lab',
    datetime('now', 'localtime', '-4 days'),
    datetime('now', 'localtime', '-1 days'),
    'new',
    'The care team released this result. The portal stores the summary only and does not add an interpretation.',
    NULL
  ),
  (
    4, 3, 2, 'Heart imaging report', 'imaging',
    datetime('now', 'localtime', '-32 days'),
    datetime('now', 'localtime', '-29 days'),
    'reviewed',
    'The care team released this result. The portal stores the summary only and does not add an interpretation.',
    datetime('now', 'localtime', '-28 days')
  );

INSERT INTO medications (id, patient_id, name, dosage, frequency, started_at, status) VALUES
  (1, 1, 'Lisinopril', '10 mg', 'Once daily', date('now', 'localtime', '-400 days'), 'active'),
  (2, 1, 'Atorvastatin', '20 mg', 'Nightly', date('now', 'localtime', '-200 days'), 'active'),
  (3, 1, 'Vitamin D', '1000 IU', 'Once daily', date('now', 'localtime', '-100 days'), 'paused'),
  (4, 2, 'Cetirizine', '10 mg', 'Once daily', date('now', 'localtime', '-50 days'), 'stopped'),
  (5, 3, 'Metformin', '500 mg', 'Twice daily', date('now', 'localtime', '-500 days'), 'active'),
  (6, 3, 'Metoprolol', '25 mg', 'Twice daily', date('now', 'localtime', '-300 days'), 'active'),
  (7, 3, 'Ibuprofen', '200 mg', 'As needed', date('now', 'localtime', '-20 days'), 'stopped');

INSERT INTO prescriptions (
  id, medication_id, provider_id, pharmacy, refills_remaining, last_filled_at, next_refill_at, status
) VALUES
  (
    1, 1, 1, 'River City Pharmacy', 2,
    date('now', 'localtime', '-20 days'),
    date('now', 'localtime', '+40 days'),
    'active'
  ),
  (
    2, 2, 1, 'River City Pharmacy', 0,
    date('now', 'localtime', '-35 days'),
    date('now', 'localtime', '-2 days'),
    'refill_due'
  ),
  (
    3, 5, 3, 'Northside Pharmacy', 3,
    date('now', 'localtime', '-15 days'),
    date('now', 'localtime', '+30 days'),
    'active'
  ),
  (
    4, 6, 2, 'Northside Pharmacy', 1,
    date('now', 'localtime', '-40 days'),
    date('now', 'localtime', '+2 days'),
    'refill_due'
  );

INSERT INTO referrals (
  id, patient_id, provider_id, department_id, reason, status, created_at, expires_at
) VALUES
  (
    1, 1, 1, 4, 'Physical therapy evaluation', 'pending',
    datetime('now', 'localtime', '-18 days'),
    date('now', 'localtime', '+60 days')
  ),
  (
    2, 3, 2, 5, 'Laboratory follow-up', 'pending',
    datetime('now', 'localtime', '-30 days'),
    date('now', 'localtime', '+30 days')
  ),
  (
    3, 3, 1, 4, 'Rehabilitation visit', 'complete',
    datetime('now', 'localtime', '-40 days'),
    date('now', 'localtime', '+10 days')
  ),
  (
    4, 3, 2, 2, 'Cardiology follow-up', 'scheduled',
    datetime('now', 'localtime', '-30 days'),
    date('now', 'localtime', '+50 days')
  );

INSERT INTO notifications (
  id, patient_id, source_type, source_id, title, body, severity, status, created_at
) VALUES
  (
    1, 1, 'message', 1, 'Unread message',
    'You have a message from Amira Patel.',
    'info', 'open', datetime('now', 'localtime', '-1 days')
  ),
  (
    2, 1, 'test_result', 1, 'New test result',
    'A lipid panel result is ready to review.',
    'warning', 'open', datetime('now', 'localtime', '-1 days')
  ),
  (
    3, 1, 'task', 3, 'Overdue task',
    'Update pharmacy information is past the due date.',
    'info', 'open', datetime('now', 'localtime', '-1 days')
  ),
  (
    4, 3, 'test_result', 3, 'New test result',
    'A basic metabolic panel result is ready to review.',
    'info', 'open', datetime('now', 'localtime', '-1 days')
  ),
  (
    5, 3, 'appointment', 5, 'Upcoming appointment',
    'You have a video visit with Naomi Brooks.',
    'info', 'open', datetime('now', 'localtime', '-2 days')
  );

INSERT INTO quick_access_items (id, label, path, sort_order, is_active) VALUES
  (1, 'Schedule appointment', '/appointments/{patient_id}', 1, 1),
  (2, 'Message provider', '/messages/{patient_id}', 2, 1),
  (3, 'Request refill', '/medications/{patient_id}', 3, 1),
  (4, 'View test results', '/results/{patient_id}', 4, 1),
  (5, 'Review medications', '/medications/{patient_id}', 5, 1),
  (6, 'View visit summaries', '/dashboard/{patient_id}#recent-visit', 6, 1);
