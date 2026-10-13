# Care Overview

Care Overview is a CS 514 database project built around a fictional patient portal. It organizes appointments, messages, test results, medications, and follow-up tasks in one dashboard.

The project uses fictional patients, providers, and medical records. It does not connect to MyChart or any real healthcare system.

## Features

- Select a fictional patient
- View recent visits and upcoming appointments
- View and manage follow-up tasks
- View messages and mark them as read
- View test results and mark them as reviewed
- View current medications
- Add and cancel appointments
- Add, complete, and delete tasks
- Update dashboard counts after changes

## Technology

- Python and Flask
- SQLite
- Jinja templates
- HTML, CSS, and JavaScript
- pytest for automated testing

## Setup

Create and activate a virtual environment:

```text
python3 -m venv .venv
source .venv/bin/activate
```

Install the required packages:

```text
python -m pip install -r requirements.txt -r requirements-test.txt
```

Initialize the database:

```text
python db.py --init
```

Start the application:

```text
python app.py
```

Open the application at:

```text
http://127.0.0.1:5000
```

The database uses sample data for three fictional patients. Running `python db.py --init` again resets the database to the original sample data.

## Run the Tests

```text
python -m pytest
```

The current test suite contains 67 tests. The tests check database constraints, queries, CRUD operations, dashboard counts, and transaction behavior.

## Project Structure

- `app.py` contains the Flask routes and application logic.
- `db.py` contains the database connection and helper functions.
- `schema.sql` creates the tables, relationships, constraints, indexes, and dashboard view.
- `seed.sql` inserts fictional patients and sample records.
- `queries.sql` contains example SQL queries.
- `templates/` contains the Flask HTML templates.
- `static/` contains the CSS and JavaScript used by the Flask application.
- `frontend/` contains the separate static frontend prototype.
- `tests/` contains the automated tests.
- `DESIGN.md` describes the interface design.
- `TESTING.md` describes the testing process.
- `docs/` contains the ER diagrams and related database files.

## Database Features

The project demonstrates:

- Primary keys and foreign keys
- Required fields and unique constraints
- Check constraints
- Indexes
- Joins and aggregate queries
- A database view named `care_overview_view`
- Insert, select, update, and delete operations
- A transaction for reviewing test results

## Limitations

This project uses fictional data and is intended for demonstration purposes only. Authentication is simulated, and the application does not provide medical advice, interpret test results, or connect to real patient records.