# Care Overview Project Plan

## Product Decision

Build **Care Overview**, a database-driven simulated patient portal dashboard. The product is inspired by the problem that patient portal information is often split across appointments, test results, messages, medications, visit summaries, referrals, and follow-up tasks.

The app will not modify MyChart, connect to MyChart, copy real MyChart branding, or use real patient data. It will use fictional records to demonstrate how a care overview dashboard could organize existing patient information into one useful homepage.

## One-Sentence Problem Statement

Patients can miss important next steps because appointment details, provider messages, test results, medication updates, and follow-up tasks are spread across separate portal sections.

## Target Users

- Patients who are new to online health portals
- Older adults who need a clear summary of next steps
- Patients managing multiple appointments, providers, results, or medications
- Caregivers helping a patient keep track of follow-up actions

## Value Proposition

Care Overview gives patients one place to see what happened recently, what needs attention, what is coming next, and where to go for common portal actions.

## Product Scope

### In Scope

- Simulated patient selector or login screen
- Personalized dashboard for fictional patients
- Recent visit summary
- Next steps checklist
- Upcoming appointment card
- Important updates summary
- Quick access links
- App pages for appointments, messages, results, medications, and tasks
- SQLite database with normalized tables
- Working CRUD operations
- Joins, aggregates, subqueries, constraints, indexes, views, and a transaction
- Test data using fictional patients and providers
- README, technical documentation, testing notes, and AI-use disclosure

### Out of Scope

- Real MyChart integration
- Real patient records
- Real medical advice
- Diagnosis, treatment recommendations, or urgency classification
- Insurance claims or billing
- Production authentication
- Presentation slides
- Voice assistant features
- Full hospital system implementation

## Recommended Stack

Use a deliberately simple stack:

- Backend: Python Flask
- Database: SQLite
- Database access: Python `sqlite3` with parameterized SQL
- Frontend: Flask Jinja templates
- Styling: plain CSS
- JavaScript: small vanilla JS only where it improves interactions
- Testing: pytest
- Documentation: Markdown
- Version control: Git and GitHub CLI

## Why This Stack

Flask, SQLite, Jinja, and plain CSS are enough for the class project and easy for every teammate to run. Raw SQL keeps the database work visible, which helps with the CS 514 rubric. The code will be easier to explain than a heavier React, ORM, or full-stack framework setup.

Use React only if the team has a strong reason. The default plan should avoid it because the project is graded on database design and working database behavior, not frontend framework complexity.

## Code Style Rules

- No code comments unless a section is genuinely hard to understand without one
- Keep files short
- Keep functions small
- Use plain names
- Avoid over-abstracted service layers
- Avoid generated-looking boilerplate
- Prefer direct readable code over clever patterns
- Use parameterized SQL
- Keep business logic understandable enough for every teammate to explain
- Never commit real credentials
- Use `.env.example` if environment variables become necessary

The code should look like a student team wrote it carefully, not like a giant generated template.

## Repository Structure

Planned structure:

```text
CS514/
  app.py
  db.py
  schema.sql
  seed.sql
  queries.sql
  requirements.txt
  README.md
  PROJECT_PLAN.md
  DESIGN.md
  TESTING.md
  AI_USE.md
  docs/
    technical_product_document.md
    data_dictionary.md
    er_model_notes.md
  static/
    styles.css
    app.js
  templates/
    base.html
    patients.html
    dashboard.html
    appointments.html
    messages.html
    results.html
    medications.html
    tasks.html
    error.html
  tests/
    test_dashboard.py
    test_crud.py
    test_constraints.py
```

## Architecture

The app will follow a simple request-response structure:

```text
Browser
  -> Flask route
  -> parameterized SQL query through db.py
  -> SQLite database
  -> Python dictionary/list results
  -> Jinja template
  -> rendered HTML/CSS
```

Data should come from the database. Dashboard cards should not be hardcoded except for labels and layout.

## Main User Workflow

1. The patient opens the simulated portal.
2. The patient selects a fictional profile.
3. The Care Overview dashboard loads.
4. The backend queries the database for the patient's recent visit.
5. The backend queries incomplete tasks and upcoming appointments.
6. The backend calculates unread messages and unreviewed test results.
7. The dashboard displays the patient's recent visit, next steps, next appointment, important updates, and quick links.
8. The patient opens a related section, such as messages or results.
9. The patient marks a message as read, marks a result as reviewed, or completes a task.
10. The database updates.
11. The dashboard counts and lists update on the next load.

## MVP Feature List

### Patient Selector

Purpose:

- Let the demo switch between fictional patients.
- Avoid building real login for Phase 1.

Features:

- List fictional patient profiles
- Show name, age or DOB, and small context label
- Link to dashboard
- Handle invalid patient IDs

### Dashboard

Purpose:

- Main product screen.
- Demonstrate that the database combines scattered records into one useful overview.

Sections:

- Patient header
- Recent Visit Summary
- Next Steps
- Upcoming Appointment
- Important Updates
- Quick Access

### Recent Visit Summary

Fields:

- Appointment date
- Provider
- Department
- Visit reason
- Visit summary
- Main instructions
- Medication changes
- Follow-up plan

Database behavior:

- Use a join between `appointments`, `visit_summaries`, `providers`, and `departments`.
- Pick the most recent completed appointment for the selected patient.

### Next Steps

Fields:

- Task title
- Task type
- Due date
- Priority
- Status
- Related visit when available

Actions:

- Create task
- Mark task complete
- Delete task

Database behavior:

- Use `follow_up_tasks`.
- Use status constraints.
- Use filtering for incomplete tasks.
- Use aggregate counts by status and priority.

### Upcoming Appointment

Fields:

- Date and time
- Provider
- Department
- Location or telehealth label
- Reason
- Check-in status
- Preparation notes

Actions:

- Create appointment
- Update appointment
- Cancel appointment

Database behavior:

- Use a subquery or ordered query to find the next scheduled appointment after the current time.
- Use joins to show provider and department.

### Important Updates

Items:

- Unread messages
- New or unreviewed test results
- Overdue tasks
- Active referrals
- Prescription refill reminders

Database behavior:

- Use aggregate counts.
- Use status fields and date comparisons.
- Use a view for dashboard summary.

### Quick Access

Links:

- Schedule appointment
- Message provider
- Request refill
- View test results
- Review medications
- View visit summaries

Database behavior:

- Quick links can be seeded in a `quick_access_items` table or rendered as stable portal links.
- If time is short, render them as stable navigation links.

## Database Schema Plan

### patients

Purpose:

- Stores fictional patient profiles.

Fields:

- `id` primary key
- `first_name`
- `last_name`
- `dob`
- `email`
- `phone`
- `created_at`

Constraints:

- `first_name` not null
- `last_name` not null
- `dob` not null
- `email` unique

### departments

Purpose:

- Stores clinical departments.

Fields:

- `id` primary key
- `name`
- `phone`

Constraints:

- `name` not null and unique

### providers

Purpose:

- Stores fictional doctors, nurses, specialists, and care team members.

Fields:

- `id` primary key
- `department_id` foreign key
- `full_name`
- `role`
- `specialty`

Constraints:

- `department_id` references `departments(id)`
- `full_name` not null
- `role` not null

### appointments

Purpose:

- Stores past and future appointments.

Fields:

- `id` primary key
- `patient_id` foreign key
- `provider_id` foreign key
- `department_id` foreign key
- `starts_at`
- `visit_type`
- `location`
- `reason`
- `status`
- `check_in_status`
- `prep_notes`
- `created_at`

Constraints:

- `patient_id` references `patients(id)`
- `provider_id` references `providers(id)`
- `department_id` references `departments(id)`
- `status` check in `scheduled`, `completed`, `cancelled`, `missed`
- `check_in_status` check in `not_started`, `available`, `complete`, `not_required`

### visit_summaries

Purpose:

- Stores summary details for completed visits.

Fields:

- `id` primary key
- `appointment_id` foreign key
- `reason`
- `summary`
- `instructions`
- `medication_changes`
- `follow_up_plan`
- `created_at`

Constraints:

- `appointment_id` references `appointments(id)`
- `appointment_id` unique if each appointment has one summary
- `summary` not null

### follow_up_tasks

Purpose:

- Stores next steps assigned after visits or from referrals/results.

Fields:

- `id` primary key
- `patient_id` foreign key
- `visit_summary_id` nullable foreign key
- `title`
- `details`
- `task_type`
- `due_at`
- `status`
- `priority`
- `completed_at`
- `created_at`

Constraints:

- `patient_id` references `patients(id)`
- `visit_summary_id` references `visit_summaries(id)`
- `status` check in `open`, `complete`, `dismissed`
- `priority` check in `low`, `normal`, `high`

### messages

Purpose:

- Stores fictional provider messages.

Fields:

- `id` primary key
- `patient_id` foreign key
- `provider_id` foreign key
- `subject`
- `body`
- `sent_at`
- `read_at`
- `status`

Constraints:

- `patient_id` references `patients(id)`
- `provider_id` references `providers(id)`
- `subject` not null
- `body` not null
- `status` check in `unread`, `read`, `archived`

### test_results

Purpose:

- Stores fictional lab or imaging result summaries.

Fields:

- `id` primary key
- `patient_id` foreign key
- `provider_id` foreign key
- `test_name`
- `category`
- `collected_at`
- `released_at`
- `status`
- `value_summary`
- `reviewed_at`

Constraints:

- `patient_id` references `patients(id)`
- `provider_id` references `providers(id)`
- `status` check in `new`, `reviewed`, `archived`
- No independent medical interpretation

### medications

Purpose:

- Stores current and past medications.

Fields:

- `id` primary key
- `patient_id` foreign key
- `name`
- `dosage`
- `frequency`
- `started_at`
- `status`

Constraints:

- `patient_id` references `patients(id)`
- `name` not null
- `status` check in `active`, `paused`, `stopped`

### prescriptions

Purpose:

- Stores refill-related information for medications.

Fields:

- `id` primary key
- `medication_id` foreign key
- `provider_id` foreign key
- `pharmacy`
- `refills_remaining`
- `last_filled_at`
- `next_refill_at`
- `status`

Constraints:

- `medication_id` references `medications(id)`
- `provider_id` references `providers(id)`
- `refills_remaining` must be greater than or equal to zero
- `status` check in `active`, `refill_due`, `expired`

### referrals

Purpose:

- Stores referrals to departments or specialists.

Fields:

- `id` primary key
- `patient_id` foreign key
- `provider_id` foreign key
- `department_id` foreign key
- `reason`
- `status`
- `created_at`
- `expires_at`

Constraints:

- `patient_id` references `patients(id)`
- `provider_id` references `providers(id)`
- `department_id` references `departments(id)`
- `status` check in `pending`, `scheduled`, `complete`, `expired`

### notifications

Purpose:

- Stores dashboard notification records.

Fields:

- `id` primary key
- `patient_id` foreign key
- `source_type`
- `source_id`
- `title`
- `body`
- `severity`
- `status`
- `created_at`
- `dismissed_at`

Constraints:

- `patient_id` references `patients(id)`
- `severity` check in `info`, `warning`, `high`
- `status` check in `open`, `dismissed`

### quick_access_items

Purpose:

- Stores portal shortcut labels and paths if the team wants quick links to be data-driven.

Fields:

- `id` primary key
- `label`
- `path`
- `sort_order`
- `is_active`

Constraints:

- `label` not null
- `path` not null
- `sort_order` not null

## Index Plan

Create indexes for common dashboard queries:

```text
appointments(patient_id, starts_at)
appointments(patient_id, status)
follow_up_tasks(patient_id, status, due_at)
messages(patient_id, status, sent_at)
test_results(patient_id, status, released_at)
medications(patient_id, status)
prescriptions(status, next_refill_at)
referrals(patient_id, status)
notifications(patient_id, status, created_at)
```

## Database View Plan

Create `care_overview_view`.

Purpose:

- Combine the main dashboard counts and patient summary into one queryable object.

Possible fields:

```text
patient_id
patient_name
last_completed_appointment_id
last_visit_at
next_appointment_id
next_appointment_at
open_task_count
overdue_task_count
unread_message_count
new_result_count
active_referral_count
refill_due_count
open_notification_count
```

This view should be used on the dashboard and documented in the technical product document.

## Transaction Plan

Implement at least one meaningful transaction.

Recommended transaction:

```text
Mark test result as reviewed
Dismiss related notification
Insert a follow-up task if the result requires review follow-up
Commit all changes together
Rollback if any step fails
```

This demonstrates correctness and database programming.

## Required CRUD Operations

### Create

- Create follow-up task
- Create appointment
- Create message or seeded message

### Read

- Read dashboard overview
- Read recent visit
- Read upcoming appointment
- Read messages
- Read test results
- Read medications

### Update

- Mark task complete
- Mark message read
- Mark result reviewed
- Cancel or reschedule appointment

### Delete

- Delete a follow-up task
- Dismiss notification
- Cancel appointment as a soft delete through status if preferred

Soft delete is safer for healthcare-style records. For the class CRUD requirement, at least one true delete can be demonstrated on a low-risk table such as `follow_up_tasks`.

## SQL Concept Checklist

The project must visibly include:

- Entity-relationship modeling
- Relational schema
- Primary keys
- Foreign keys
- Normalization
- `SELECT`
- `INSERT`
- `UPDATE`
- `DELETE`
- Joins
- Aggregate functions
- Subqueries
- Constraints
- Views
- Transactions
- Database programming from Flask

## Key Queries To Implement

### Recent Visit Query

Use joins across:

```text
appointments
visit_summaries
providers
departments
```

Goal:

- Return the most recent completed visit for the selected patient.

### Upcoming Appointment Query

Use a subquery or ordered filtered query.

Goal:

- Return the next scheduled appointment after the current time.

### Important Updates Query

Use aggregates.

Goal:

- Count unread messages, new results, incomplete tasks, overdue tasks, and open notifications.

### Task Priority Query

Use grouping.

Goal:

- Count open tasks by priority.

### Medication Refill Query

Use joins across:

```text
medications
prescriptions
providers
```

Goal:

- Show active medications with refill status.

## Backend Route Plan

### Patient Routes

```text
GET /
GET /patients
GET /dashboard/<patient_id>
```

### Appointment Routes

```text
GET /appointments/<patient_id>
POST /appointments
POST /appointments/<appointment_id>/cancel
```

### Task Routes

```text
GET /tasks/<patient_id>
POST /tasks
POST /tasks/<task_id>/complete
POST /tasks/<task_id>/delete
```

### Message Routes

```text
GET /messages/<patient_id>
POST /messages/<message_id>/read
```

### Result Routes

```text
GET /results/<patient_id>
POST /results/<result_id>/review
```

### Medication Routes

```text
GET /medications/<patient_id>
```

### API Route

```text
GET /api/care-overview/<patient_id>
```

The API route is optional but useful for proving that the backend can return the overview as structured data.

## Frontend Page Plan

### `patients.html`

Purpose:

- Let reviewers choose a fictional patient.

Content:

- Patient name
- DOB or age
- Short care context
- Dashboard link

### `dashboard.html`

Purpose:

- Main product screen.

Content:

- Patient header
- Care Overview section
- Recent Visit Summary
- Next Steps
- Upcoming Appointment
- Important Updates
- Quick Access

### `appointments.html`

Purpose:

- Show scheduled and past appointments.

Actions:

- Add appointment
- Cancel appointment

### `tasks.html`

Purpose:

- Show next steps.

Actions:

- Add task
- Complete task
- Delete task

### `messages.html`

Purpose:

- Show provider messages.

Actions:

- Mark message read

### `results.html`

Purpose:

- Show test result summaries.

Actions:

- Mark result reviewed

Important:

- The app must not interpret test results medically.

### `medications.html`

Purpose:

- Show current medications and refill reminders.

Actions:

- View active and paused/stopped medications
- Show refill status

## UI Plan

Follow [DESIGN.md](DESIGN.md).

The app should look like a real utility:

- Dashboard first
- No landing page
- No purple gradient
- No glassmorphism
- No decorative blobs
- No generic AI SaaS slogans
- No identical three-card feature grid
- No oversized hero text
- No fake premium styling

The interface should use:

- Left navigation on desktop
- Single-column flow on mobile
- Clear section labels
- Calm healthcare palette
- Compact cards for dashboard groups
- Visible focus states
- Plain patient-facing language
- Real empty, error, and success states

## Accessibility Plan

Minimum accessibility requirements:

- Semantic headings
- Labels for form fields
- Visible keyboard focus
- Sufficient color contrast
- Buttons for actions, links for navigation
- Error messages near the relevant form
- Touch targets large enough on mobile
- No information conveyed only through color

## Seed Data Plan

Create at least 3 fictional patients:

1. A patient with a recent completed visit, upcoming appointment, unread messages, new results, active medications, and tasks.
2. A patient with fewer records to test empty states.
3. A patient with multiple providers and departments to prove joins and relationships.

Use fictional names and safe generic medical context. Avoid real names, real chart numbers, real phone numbers, or sensitive real-world data.

Example fictional records:

- Family medicine visit
- Cardiology follow-up
- Lab work task
- Medication refill reminder
- Physical therapy referral
- Unread provider message
- Released test result summary

## Testing Plan

### Database Tests

Test:

- Tables are created
- Seed data loads
- Foreign keys are enforced
- Required fields reject null values
- Invalid statuses fail check constraints
- Duplicate unique fields fail where expected
- Care overview view returns expected counts

### Backend Tests

Test:

- Patient list loads
- Dashboard loads for valid patient
- Invalid patient ID shows an error
- Appointment creation works
- Appointment cancellation works
- Task creation works
- Task completion updates dashboard count
- Message read action updates unread count
- Result review transaction updates result and notification

### UI Tests

Manual tests:

- Dashboard looks correct on desktop
- Dashboard works on mobile width
- No text overlaps
- All buttons fit
- Empty states are understandable
- Error states are visible
- Keyboard tab order is usable

### Data Cases

Test:

- Valid data
- Empty fields
- Duplicate email
- Invalid status
- Missing foreign key
- Patient with no upcoming appointment
- Patient with no unread messages
- Patient with no test results

## Documentation Plan

Create these documents:

### `README.md`

Include:

- Project overview
- Setup instructions
- How to run
- How to reset database
- How to run tests
- Feature list
- Team notes

### `docs/technical_product_document.md`

Include:

- Problem statement
- Target users
- Product overview
- Architecture
- ER model
- Relational schema
- Data dictionary
- CRUD operations
- SQL queries
- Course concepts
- Screenshots
- Testing results
- Known limitations
- Future improvements
- AI-use disclosure summary

### `docs/data_dictionary.md`

Include:

- Every table
- Every column
- Data type
- Meaning
- Constraints
- Relationships

### `TESTING.md`

Include:

- Test checklist
- How tests were run
- Manual test cases
- Known defects
- Limitations

### `AI_USE.md`

Include:

- Where AI helped
- What the team reviewed
- What the team changed
- What was written or verified by team members
- Statement that the team can explain all submitted work

## AI Use Boundary

AI may be used for:

- Brainstorming
- Planning
- Debugging
- SQL review
- Documentation drafts
- UI critique
- Test case ideas

AI should not be used as an unquestioned source for:

- Medical advice
- Patient urgency
- Diagnosis
- Treatment recommendation
- Real medical interpretation

If a generated summary feature is added, it must only summarize existing fictional database records. It must not diagnose, interpret results independently, recommend care, or decide urgency.

## Stretch Feature

Only after the MVP works:

Add a plain-language overview generated from database records.

Example:

```text
Since your last appointment, you have 2 open tasks, 1 unread message, and 1 new test result. Your next appointment is September 18 at 10:30 AM with Dr. Patel.
```

Implementation:

- Start with a template-based summary.
- Do not use a live AI API unless the team has time to document and defend it.
- Keep the summary factual and limited to existing records.

## Team Role Plan

Suggested roles:

- Database lead: schema, seed data, queries, ER diagram, constraints
- Backend lead: Flask routes, validation, transactions, app flow
- Frontend lead: templates, CSS, responsive design, accessibility
- Documentation lead: README, technical document, data dictionary, AI-use notes
- QA/integration lead: tests, screenshots, setup verification, GitHub cleanup

Every team member should still contribute technically. Roles are ownership areas, not silos.

## Git Workflow

Use `main` as the stable branch.

Suggested branch names:

```text
feature/schema
feature/dashboard
feature/tasks
feature/messages-results
feature/docs
```

Commit style:

```text
Add initial database schema
Seed fictional patient records
Build dashboard overview query
Add task completion flow
Document testing checklist
```

Avoid vague commits:

```text
updates
stuff
fix
final
```

## Fresh Setup Goal

A teammate should be able to run:

```text
git clone https://github.com/AdiSchoolGit/CS514.git
cd CS514
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Then open the local app and see the patient selector.

If the app needs a database init command, document it clearly:

```text
python db.py --init
```

## Milestones From September 23, 2026

### September 23-24: Foundation

Required result:

- Repo connected
- Plan committed
- Stack chosen
- Initial folder structure created
- Schema draft complete
- ER model draft started

### September 25-26: Database Build

Required result:

- `schema.sql` complete
- `seed.sql` complete
- Database init works
- Constraints and foreign keys enabled
- Sample queries return correct data

### September 27-28: Backend Core

Required result:

- Flask app starts
- Patient selector works
- Dashboard route works
- Recent visit query works
- Upcoming appointment query works
- Important updates counts work

### September 29-October 1: CRUD Features

Required result:

- Appointment create/cancel flow works
- Task create/complete/delete flow works
- Message read flow works
- Result review transaction works
- Medication page works

### October 2-3: UI and Integration

Required result:

- Dashboard UI follows `DESIGN.md`
- Mobile layout works
- Empty states exist
- Error states exist
- Navigation is consistent
- No generated-looking UI patterns remain

### October 4-6: Testing and Feature Freeze

Required result:

- Stop adding optional features
- Run fresh setup
- Run tests
- Record bugs
- Fix critical issues
- Capture screenshots

### October 7-10: Documentation

Required result:

- README finished
- Technical document draft finished
- Data dictionary finished
- Testing document finished
- AI-use document finished
- GitHub repo cleaned

### October 11-12: Final Product Polish

Required result:

- Fresh clone works
- App runs without manual guessing
- Database can be reset
- Screenshots match current app
- Known limitations documented
- All links and files checked

## Definition of Done

The product is done when:

- A user can run the app locally from the README
- The database initializes cleanly
- Fictional patient data is loaded
- Dashboard data comes from SQL queries
- CRUD operations work
- Joins, aggregates, subqueries, constraints, views, and transactions are documented
- The UI follows `DESIGN.md`
- Tests or documented manual checks pass
- No real patient data exists
- AI use is disclosed
- Every team member can explain the schema, workflow, and their contribution

## Final Verification Checklist

- `git status` is clean
- README setup steps work from a fresh clone
- Database file can be recreated
- No `.env` or secrets committed
- No real medical data committed
- No broken links in docs
- No unused giant generated files
- No code comments unless truly needed
- No hardcoded dashboard data pretending to be database-driven
- No generic AI-looking UI patterns
- All required CS 514 product deliverables are represented

