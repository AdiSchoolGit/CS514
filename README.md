# Care Overview

## Quick Summary

Care Overview is a school project for CS 514. It is a fake patient portal dashboard that shows how a healthcare app could organize important information in one place.

The idea is simple: instead of making a patient click through many different pages to find appointments, messages, test results, medications, and follow-up tasks, the app gives them one clear overview. A patient can quickly see their most recent visit, what they need to do next, their next appointment, unread messages, new test results, and useful shortcut links.

This project does not use real patient data and does not connect to the real MyChart app. Everything will be made with fictional patients, fictional doctors, and sample records. The main goal is to show strong database design and a working database-driven product.

Care Overview is a CS 514 database product prototype for a simulated patient portal dashboard. It organizes fictional appointment, visit, message, test result, medication, referral, and task records into one clear homepage summary.

This repository is for the product only. Presentation slides and speaking notes are intentionally out of scope.

## Documents

- [PROJECT_PLAN.md](PROJECT_PLAN.md) - full implementation plan, schema plan, milestones, testing, and deliverables
- [DESIGN.md](DESIGN.md) - UI direction and rules for avoiding generic generated-looking design

## Product Direction

The app should feel like a practical healthcare portal, not a startup landing page. The database should drive the dashboard, and the UI should make patient next steps easy to scan.

## Initial Stack

- Backend: Python Flask
- Database: SQLite
- Frontend: Jinja templates, plain CSS, small vanilla JavaScript
- Tests: pytest
- Version control: Git and GitHub CLI

## Setup

```text
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python db.py --init
python app.py
```

Open http://127.0.0.1:5000 and choose a fictional patient.

`python app.py` creates the database if it is missing. Run `python db.py --init` again to reset it.

Run tests with `pytest`.

Routes match the backend route plan:

```text
GET /
GET /patients
GET /dashboard/<patient_id>
GET /appointments/<patient_id>
POST /appointments
POST /appointments/<appointment_id>/cancel
GET /tasks/<patient_id>
POST /tasks
POST /tasks/<task_id>/complete
POST /tasks/<task_id>/delete
GET /messages/<patient_id>
POST /messages/<message_id>/read
GET /results/<patient_id>
POST /results/<result_id>/review
GET /medications/<patient_id>
GET /api/care-overview/<patient_id>
```
