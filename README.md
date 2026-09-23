# Care Overview

## Quick Summary

Care Overview is a school project for CS 514. Right now, this repo has a frontend-only prototype of a fake patient portal dashboard. It shows how a healthcare app could organize important information in one place.

The idea is simple: instead of making a patient click through many different pages to find appointments, messages, test results, medications, and follow-up tasks, the app gives them one clear overview. A patient can quickly see their most recent visit, what they need to do next, their next appointment, unread messages, new test results, and useful shortcut links.

This project does not use real patient data and does not connect to the real MyChart app. Everything will be made with fictional patients, fictional doctors, and sample records. The main goal is to show strong database design and a working database-driven product.

The frontend works without a backend by using local demo data in the browser. It is also set up so a backend can be added later without rebuilding the whole interface.

This repository is for the product only. Presentation slides and speaking notes are intentionally out of scope.

## Open The Frontend

Open this file in a browser:

```text
frontend/index.html
```

The page works as a static frontend. No server, database, or install step is required for the current prototype.

## Documents

- [PROJECT_PLAN.md](PROJECT_PLAN.md) - full implementation plan, schema plan, milestones, testing, and deliverables
- [DESIGN.md](DESIGN.md) - UI direction and rules for avoiding generic generated-looking design

## Current Frontend

The prototype includes:

- Patient selector with fictional patients
- Care Overview dashboard
- Recent visit summary
- Next steps checklist
- Upcoming appointment card
- Important updates section
- Appointment, message, result, medication, and task views
- Local update actions like mark task complete, mark message read, mark result reviewed, add task, and add appointment

## Backend Handoff

The frontend currently uses local demo data. Later, the backend can connect at the data layer in `frontend/app.js`.

Future backend target:

```text
window.CARE_OVERVIEW_API_BASE = "http://localhost:5000"
```

Expected API shape:

```text
GET /api/care-overview
PUT /api/care-overview
```

The current frontend data model already uses patient, provider, department, appointment, visit summary, task, message, result, medication, prescription, referral, and notification records.

## Product Direction

The app should feel like a practical healthcare portal, not a startup landing page. The database should drive the dashboard, and the UI should make patient next steps easy to scan.

## Current Stack

- Frontend: static HTML, plain CSS, vanilla JavaScript
- Demo data: local browser state
- Backend-ready spot: data layer in `frontend/app.js`
- Version control: Git and GitHub CLI
