# Testing

## How to Run Tests

Create and activate the virtual environment:

```text
python3 -m venv .venv
source .venv/bin/activate
```

Install the project and testing packages:

```text
python -m pip install -r requirements.txt -r requirements-test.txt
```

Run the test suite:

```text
python -m pytest
```

The current test suite contains 67 tests.

## What Is Tested

The automated tests cover:

- Database initialization and seed data
- Primary key, foreign key, unique, check, and NOT NULL constraints
- Patient and dashboard queries
- Appointment, task, message, and result actions
- Task completion and deletion
- Marking messages as read
- Reviewing test results
- Dashboard count updates
- Empty states and unknown record IDs
- Query ordering and filtering
- Transaction rollback behavior

## Manual UI Checks

The frontend should also be checked manually for:

- Correct dashboard layout on desktop
- Usability at a smaller mobile width
- Readable empty states
- Visible error messages
- Buttons that fit correctly
- Working patient selection
- Working appointment, task, message, and result actions
- Usable keyboard tab order

The static frontend is not fully tested by pytest.

## Limitations

The project uses fictional patient data and does not connect to real medical records. Authentication is simulated, and the application does not provide medical advice or interpret test results.