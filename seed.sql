--sample departments used by the fictional care team
INSERT INTO departments (id, name, phone) VALUES
  (1, 'Family Medicine', '555-0101'),
  (2, 'Cardiology', '555-0102'),
  (3, 'Endocrinology', '555-0103'),
  (4, 'Rehabilitation', '555-0104'),
  (5, 'Laboratory', '555-0105');

--providers connected to each department
INSERT INTO providers (id, department_id, full_name, role, specialty) VALUES
  (1, 1, 'Amira Patel', 'Physician', 'Family Medicine'),
  (2, 2, 'Luis Ortega', 'Physician', 'Cardiology'),
  (3, 3, 'Naomi Brooks', 'Physician', 'Endocrinology'),
  (4, 4, 'Jordan Kim', 'Physical Therapist', 'Rehabilitation'),
  (5, 5, 'Riley Nguyen', 'Clinical Lab Scientist', 'Laboratory');

--fictional patient records used for testing and demos
INSERT INTO patients (id, first_name, last_name, dob, email, phone) VALUES
  (1, 'Maya', 'Chen', '1988-04-12', 'maya.chen@example.com', '555-0142'),
  (2, 'Jordan', 'Hale', '2001-11-03', 'jordan.hale@example.com', '555-0177'),
  (3, 'Elena', 'Vasquez', '1956-07-22', 'elena.vasquez@example.com', '555-0194');

--past and upcoming appointments for sample patients
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

--summaries connected to complete appointments
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

--open and complete tasks shown on the dashboard
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

--messsages with both unread and read examples
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

--test results used to demo new and reviewed statuses
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

--medication records for the sample patients
INSERT INTO medications (id, patient_id, name, dosage, frequency, started_at, status) VALUES
  (1, 1, 'Lisinopril', '10 mg', 'Once daily', date('now', 'localtime', '-400 days'), 'active'),
  (2, 1, 'Atorvastatin', '20 mg', 'Nightly', date('now', 'localtime', '-200 days'), 'active'),
  (3, 1, 'Vitamin D', '1000 IU', 'Once daily', date('now', 'localtime', '-100 days'), 'paused'),
  (4, 2, 'Cetirizine', '10 mg', 'Once daily', date('now', 'localtime', '-50 days'), 'stopped'),
  (5, 3, 'Metformin', '500 mg', 'Twice daily', date('now', 'localtime', '-500 days'), 'active'),
  (6, 3, 'Metoprolol', '25 mg', 'Twice daily', date('now', 'localtime', '-300 days'), 'active'),
  (7, 3, 'Ibuprofen', '200 mg', 'As needed', date('now', 'localtime', '-20 days'), 'stopped');

--prescriptions and refill info connected to the medications
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

--sample referrals with different statuses and expiration dates
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

--dashboard notifications created from sample events
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

--shortcut links shown on the dashboard
INSERT INTO quick_access_items (id, label, path, sort_order, is_active) VALUES
  (1, 'Schedule appointment', '/appointments/{patient_id}', 1, 1),
  (2, 'Message provider', '/messages/{patient_id}', 2, 1),
  (3, 'Request refill', '/medications/{patient_id}', 3, 1),
  (4, 'View test results', '/results/{patient_id}', 4, 1),
  (5, 'Review medications', '/medications/{patient_id}', 5, 1),
  (6, 'View visit summaries', '/dashboard/{patient_id}#recent-visit', 6, 1);

INSERT INTO patients (id, first_name, last_name, dob, email, phone) VALUES
  (4, 'Priya', 'Nair', '1992-02-17', 'priya.nair@example.com', '555-0211'),
  (5, 'Marcus', 'Webb', '1948-09-03', 'marcus.webb@example.com', '555-0238');

INSERT INTO appointments (
  id, patient_id, provider_id, department_id, starts_at, visit_type, location, reason, status, check_in_status, prep_notes
) VALUES
  (
    7, 4, 3, 3,
    datetime('now', 'localtime', '-12 days', 'start of day', '+10 hours'),
    'office', 'Endocrinology Room 3', 'Thyroid follow-up', 'completed', 'complete', NULL
  ),
  (
    8, 4, 5, 5,
    datetime('now', 'localtime', '+6 days', 'start of day', '+8 hours'),
    'lab', 'Main lab', 'Lab draw', 'scheduled', 'available',
    'Bring your photo ID and arrive 10 minutes early.'
  ),
  (
    9, 5, 1, 1,
    datetime('now', 'localtime', '-25 days', 'start of day', '+9 hours'),
    'office', 'Clinic Room 1', 'Annual visit', 'completed', 'complete', NULL
  ),
  (
    10, 5, 2, 2,
    datetime('now', 'localtime', '-9 days', 'start of day', '+13 hours'),
    'office', 'Heart Clinic Room 2', 'Blood pressure check', 'completed', 'complete', NULL
  ),
  (
    11, 5, 2, 2,
    datetime('now', 'localtime', '+18 days', 'start of day', '+11 hours'),
    'office', 'Heart Clinic Room 2', 'Follow-up visit', 'scheduled', 'not_started',
    'Bring your home blood pressure log.'
  );

INSERT INTO visit_summaries (
  id, appointment_id, reason, summary, instructions, medication_changes, follow_up_plan
) VALUES
  (
    4, 7, 'Thyroid follow-up',
    'The note covers the current medication and the lab order for the next visit.',
    'Take the medication in the morning and complete the lab draw before the next visit.',
    'No medication changes were recorded at this visit.',
    'Complete the lab draw and keep the next appointment.'
  ),
  (
    5, 9, 'Annual visit',
    'The note covers routine vitals and the current medication list.',
    'Continue the medications already on your list.',
    'No medication changes were recorded at this visit.',
    'Return in one year.'
  ),
  (
    6, 10, 'Blood pressure check',
    'The note covers the home blood pressure log reviewed at the clinic.',
    'Keep logging your blood pressure each morning.',
    'No medication changes were recorded at this visit.',
    'Keep the follow-up visit on the calendar.'
  );

INSERT INTO follow_up_tasks (
  id, patient_id, visit_summary_id, title, details, task_type, due_at, status, priority, completed_at
) VALUES
  (
    8, 4, 4, 'Complete lab draw',
    'Go to the main lab for the tests ordered at the last visit.',
    'lab', date('now', 'localtime', '+5 days'), 'open', 'high', NULL
  ),
  (
    9, 4, 4, 'Pick up prescription',
    'The refill is ready at your pharmacy.',
    'medication', date('now', 'localtime', '-3 days'), 'open', 'normal', NULL
  ),
  (
    10, 5, 6, 'Bring home blood pressure log',
    'Bring the log to the follow-up cardiology visit.',
    'general', date('now', 'localtime', '-6 days'), 'complete', 'normal',
    datetime('now', 'localtime', '-8 days')
  ),
  (
    11, 5, 5, 'Read visit instructions',
    'Read the instructions on the annual visit summary.',
    'general', date('now', 'localtime', '-20 days'), 'complete', 'low',
    datetime('now', 'localtime', '-22 days')
  );

INSERT INTO messages (id, patient_id, provider_id, subject, body, sent_at, read_at, status) VALUES
  (
    6, 4, 3, 'Visit follow-up',
    'A note from your thyroid follow-up is available on the overview page.',
    datetime('now', 'localtime', '-2 days'), NULL, 'unread'
  ),
  (
    7, 4, 5, 'Lab prep instructions',
    'The lab draw is scheduled. Your appointment page lists the time and what to bring.',
    datetime('now', 'localtime', '-1 days'), NULL, 'unread'
  ),
  (
    8, 5, 1, 'Visit summary available',
    'The summary from your annual visit is ready on the overview page.',
    datetime('now', 'localtime', '-24 days'),
    datetime('now', 'localtime', '-23 days'),
    'read'
  ),
  (
    9, 5, 2, 'Follow-up visit scheduled',
    'Your follow-up cardiology visit is on the calendar.',
    datetime('now', 'localtime', '-9 days'),
    datetime('now', 'localtime', '-8 days'),
    'read'
  );

INSERT INTO test_results (
  id, patient_id, provider_id, test_name, category, collected_at, released_at, status, value_summary, reviewed_at
) VALUES
  (
    5, 4, 3, 'Thyroid panel', 'lab',
    datetime('now', 'localtime', '-3 days'),
    datetime('now', 'localtime', '-1 days'),
    'new',
    'The care team released this result. The portal stores the summary only and does not add an interpretation.',
    NULL
  ),
  (
    6, 4, 1, 'Vitamin D level', 'lab',
    datetime('now', 'localtime', '-40 days'),
    datetime('now', 'localtime', '-38 days'),
    'reviewed',
    'The care team released this result. The portal stores the summary only and does not add an interpretation.',
    datetime('now', 'localtime', '-37 days')
  ),
  (
    7, 5, 2, 'Basic metabolic panel', 'lab',
    datetime('now', 'localtime', '-12 days'),
    datetime('now', 'localtime', '-10 days'),
    'reviewed',
    'The care team released this result. The portal stores the summary only and does not add an interpretation.',
    datetime('now', 'localtime', '-9 days')
  );

INSERT INTO medications (id, patient_id, name, dosage, frequency, started_at, status) VALUES
  (8, 4, 'Levothyroxine', '50 mcg', 'Once daily', date('now', 'localtime', '-300 days'), 'active'),
  (9, 4, 'Vitamin D', '2000 IU', 'Once daily', date('now', 'localtime', '-45 days'), 'active'),
  (10, 5, 'Amlodipine', '5 mg', 'Once daily', date('now', 'localtime', '-600 days'), 'active'),
  (11, 5, 'Aspirin', '81 mg', 'Once daily', date('now', 'localtime', '-700 days'), 'active');

INSERT INTO prescriptions (
  id, medication_id, provider_id, pharmacy, refills_remaining, last_filled_at, next_refill_at, status
) VALUES
  (
    5, 8, 3, 'Northside Pharmacy', 0,
    date('now', 'localtime', '-30 days'),
    date('now', 'localtime', '-1 days'),
    'refill_due'
  ),
  (
    6, 9, 1, 'Northside Pharmacy', 2,
    date('now', 'localtime', '-10 days'),
    date('now', 'localtime', '+35 days'),
    'active'
  ),
  (
    7, 10, 2, 'River City Pharmacy', 4,
    date('now', 'localtime', '-15 days'),
    date('now', 'localtime', '+45 days'),
    'active'
  ),
  (
    8, 11, 1, 'River City Pharmacy', 3,
    date('now', 'localtime', '-5 days'),
    date('now', 'localtime', '+60 days'),
    'active'
  );

INSERT INTO referrals (
  id, patient_id, provider_id, department_id, reason, status, created_at, expires_at
) VALUES
  (
    5, 4, 3, 5, 'Laboratory work', 'pending',
    datetime('now', 'localtime', '-12 days'),
    date('now', 'localtime', '+30 days')
  );

INSERT INTO notifications (
  id, patient_id, source_type, source_id, title, body, severity, status, created_at
) VALUES
  (
    6, 4, 'message', 6, 'Unread message',
    'You have a message from Naomi Brooks.',
    'info', 'open', datetime('now', 'localtime', '-2 days')
  ),
  (
    7, 4, 'test_result', 5, 'New test result',
    'A thyroid panel result is ready to review.',
    'info', 'open', datetime('now', 'localtime', '-1 days')
  ),
  (
    8, 4, 'task', 9, 'Overdue task',
    'Pick up prescription is past the due date.',
    'info', 'open', datetime('now', 'localtime', '-1 days')
  );

INSERT INTO patients (id, first_name, last_name, dob, email, phone) VALUES
  (6, 'Graham', 'Abbott', '1979-06-24', 'graham.abbott@example.com', '555-0256');

INSERT INTO appointments (
  id, patient_id, provider_id, department_id, starts_at, visit_type, location, reason, status, check_in_status, prep_notes
) VALUES
  (
    12, 6, 1, 1,
    datetime('now', 'localtime', '-14 days', 'start of day', '+9 hours'),
    'office', 'Clinic Room 3', 'Annual visit', 'completed', 'complete', NULL
  ),
  (
    13, 6, 2, 2,
    datetime('now', 'localtime', '+4 days', 'start of day', '+14 hours'),
    'office', 'Heart Clinic Room 1', 'Cardiology follow-up', 'scheduled', 'available',
    'Bring your medication list and home blood pressure log.'
  );

INSERT INTO visit_summaries (
  id, appointment_id, reason, summary, instructions, medication_changes, follow_up_plan
) VALUES
  (
    7, 12, 'Annual visit',
    'The note covers routine vitals, the medication list, and several follow-up items.',
    'Complete the lab work, return the forms, and book the follow-up visits listed in your tasks.',
    'The refill for the blood pressure medication was updated.',
    'Work through the open tasks before the cardiology visit.'
  );

INSERT INTO follow_up_tasks (
  id, patient_id, visit_summary_id, title, details, task_type, due_at, status, priority, completed_at
) VALUES
  (
    12, 6, 7, 'Schedule cardiology follow-up',
    'Choose a time that works for the follow-up visit.',
    'appointment', date('now', 'localtime', '-5 days'), 'open', 'high', NULL
  ),
  (
    13, 6, 7, 'Complete fasting lab work',
    'Go to the main lab with nothing to eat or drink except water.',
    'lab', date('now', 'localtime', '+2 days'), 'open', 'high', NULL
  ),
  (
    14, 6, 7, 'Refill blood pressure medication',
    'The updated refill is ready to request.',
    'medication', date('now', 'localtime', '-2 days'), 'open', 'high', NULL
  ),
  (
    15, 6, 7, 'Return signed consent form',
    'The form was sent with the visit summary.',
    'general', date('now', 'localtime', '-9 days'), 'open', 'normal', NULL
  ),
  (
    16, 6, NULL, 'Update insurance information',
    'Check that the insurance details on file are current.',
    'general', date('now', 'localtime', '+6 days'), 'open', 'normal', NULL
  ),
  (
    17, 6, 7, 'Book physical therapy evaluation',
    'The referral is ready to schedule.',
    'referral', date('now', 'localtime', '+10 days'), 'open', 'normal', NULL
  ),
  (
    18, 6, 7, 'Review new medication instructions',
    'Read the updated instructions in the visit summary.',
    'medication', date('now', 'localtime', '+3 days'), 'open', 'normal', NULL
  ),
  (
    19, 6, NULL, 'Complete pre-visit questionnaire',
    'The form is available before the cardiology visit.',
    'general', date('now', 'localtime', '+4 days'), 'open', 'low', NULL
  ),
  (
    20, 6, 7, 'Send home blood pressure log',
    'Upload or bring the log to the cardiology visit.',
    'general', date('now', 'localtime', '+8 days'), 'open', 'low', NULL
  );

INSERT INTO messages (id, patient_id, provider_id, subject, body, sent_at, read_at, status) VALUES
  (
    10, 6, 1, 'Lab order ready',
    'The lab order from your annual visit is ready. Your task list has the details.',
    datetime('now', 'localtime', '-3 days'), NULL, 'unread'
  ),
  (
    11, 6, 2, 'Follow-up visit',
    'Your cardiology follow-up is on the calendar.',
    datetime('now', 'localtime', '-1 days'), NULL, 'unread'
  );

INSERT INTO test_results (
  id, patient_id, provider_id, test_name, category, collected_at, released_at, status, value_summary, reviewed_at
) VALUES
  (
    8, 6, 1, 'Lipid panel', 'lab',
    datetime('now', 'localtime', '-13 days'),
    datetime('now', 'localtime', '-10 days'),
    'new',
    'The care team released this result. The portal stores the summary only and does not add an interpretation.',
    NULL
  );

INSERT INTO medications (id, patient_id, name, dosage, frequency, started_at, status) VALUES
  (12, 6, 'Lisinopril', '10 mg', 'Once daily', date('now', 'localtime', '-500 days'), 'active');

INSERT INTO prescriptions (
  id, medication_id, provider_id, pharmacy, refills_remaining, last_filled_at, next_refill_at, status
) VALUES
  (
    9, 12, 2, 'River City Pharmacy', 0,
    date('now', 'localtime', '-32 days'),
    date('now', 'localtime', '-2 days'),
    'refill_due'
  );

INSERT INTO referrals (
  id, patient_id, provider_id, department_id, reason, status, created_at, expires_at
) VALUES
  (
    6, 6, 1, 4, 'Physical therapy evaluation', 'pending',
    datetime('now', 'localtime', '-14 days'),
    date('now', 'localtime', '+45 days')
  );

INSERT INTO notifications (
  id, patient_id, source_type, source_id, title, body, severity, status, created_at
) VALUES
  (
    9, 6, 'message', 10, 'Unread message',
    'You have a message from Amira Patel.',
    'info', 'open', datetime('now', 'localtime', '-3 days')
  ),
  (
    10, 6, 'test_result', 8, 'New test result',
    'A lipid panel result is ready to review.',
    'info', 'open', datetime('now', 'localtime', '-10 days')
  );
