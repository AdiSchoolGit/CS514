# Testing

## How to run tests

```text
pip install -r requirements.txt -r requirements-test.txt
pytest
```

With coverage:

```text
pytest --cov=. --cov-report=term-missing
```

## What's covered

`tests/test_database.py`

- Seed data loads
- Foreign keys enforced
- NOT NULL, unique, and check constraints
- `care_overview_view` counts, including a patient with sparse data
- Recent visit query, next-appointment query (skips cancelled)
- Task completion, message read, and result-review flows update dashboard counts
- Result-review transaction rolls back on failure
- Task delete

`tests/test_gaps.py`

- `get_patients` / `get_patient` read helpers, including unknown-id case
- `get_open_tasks` ordering (overdue first, then priority)
- `get_quick_access` filters inactive items and respects sort order
- `get_recent_visit` / `get_next_appointment` empty-state behavior
- `review_result` raises `ValueError` for an unknown result id
- Idempotency: completing an already-complete task, marking an already-read
  message read, and deleting an unknown task are all no-ops rather than errors
- `create_task` with only the required arguments
- Check constraints on `appointments.visit_type`, `test_results.category`,
  `medications.status`, `notifications.severity`, `quick_access_items.is_active`
- Foreign key enforcement on `referrals.department_id`
- Uniqueness on `departments.name` and `visit_summaries.appointment_id`

## Manual UI checks

Frontend is static HTML/CSS/JS, not covered by pytest. Checked manually per
`PROJECT_PLAN.md`:

- [ ] Dashboard looks correct on desktop
- [ ] Dashboard works on mobile width
- [ ] No text overlaps
- [ ] All buttons fit
- [ ] Empty states are understandable
- [ ] Error states are visible
- [ ] Keyboard tab order is usable

## Known defects

None recorded yet.

## Limitations

None recorded yet.
