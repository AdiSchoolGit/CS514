# Care Overview plan

Patient portals spread your stuff across a bunch of tabs: appointments here, messages there, results somewhere else. Care Overview is a fake portal homepage that pulls it into one screen and tells you what to do next. Everything is made-up data. It doesn't touch MyChart or any real records.

## Stack

Flask, SQLite, Jinja templates and plain CSS. Raw SQL through `sqlite3`, so every query is easy to point at and explain. Tests are pytest. No React or ORM, since the point is the database.

## Tables

patients, departments, providers, appointments, visit_summaries, follow_up_tasks, messages, test_results, medications, prescriptions, referrals, notifications, quick_access_items.

`care_overview_view` rolls them up into one row per patient for the dashboard counts. `schema.sql` is the source of truth and `docs/er_diagram.png` shows how they connect.

## What the app does

- pick a fictional patient
- dashboard with the next thing to do, tasks, upcoming appointment, last visit
- pages for appointments, tasks, messages, results and medications
- add and cancel appointments, add, complete and delete tasks, mark messages read, mark results reviewed
- reviewing a result is one transaction: mark it reviewed, clear its notification, maybe add a follow-up task

It never interprets a test result or says anything is urgent. It only shows what's in the records.

## Class checklist

- [x] ER diagram and relational schema
- [x] primary keys, foreign keys, constraints, indexes
- [x] insert, select, update, delete from the Flask app
- [x] joins, aggregates, subqueries
- [x] a view
- [x] a transaction
- [x] seed data for 3 patients, including one with almost nothing
- [ ] data dictionary
- [ ] technical write-up with screenshots

## UI checks

- [ ] Dashboard looks correct on desktop
- [ ] Dashboard works on mobile width
- [ ] No text overlaps
- [ ] All buttons fit
- [ ] Empty states are understandable
- [ ] Error states are visible
- [ ] Keyboard tab order is usable

## Dates

- Sept 23 to Oct 3: schema, backend, CRUD, first UI
- Oct 4 to 6: stop adding features, run tests, fix bugs
- Oct 7 to 10: docs
- Oct 11 and 12: fresh clone test, screenshots, cleanup

## Docs

README for setup, TESTING.md for checks, DESIGN.md for the look, a data dictionary and a technical write-up in `docs/`, and `AI_USE.md` for where AI helped.
