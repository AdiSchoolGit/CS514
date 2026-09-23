import os
import sqlite3
from datetime import datetime

from flask import Flask, abort, flash, jsonify, redirect, render_template, request, url_for

import db

LABELS = {
    "scheduled": "Scheduled",
    "completed": "Completed",
    "cancelled": "Cancelled",
    "missed": "Missed",
    "not_started": "Not started",
    "available": "Available",
    "complete": "Complete",
    "not_required": "Not required",
    "open": "Open",
    "dismissed": "Dismissed",
    "unread": "Unread",
    "read": "Read",
    "archived": "Archived",
    "new": "New",
    "reviewed": "Reviewed",
    "active": "Active",
    "paused": "Paused",
    "stopped": "Stopped",
    "refill_due": "Refill due",
    "expired": "Expired",
    "pending": "Pending",
    "low": "Low",
    "normal": "Normal",
    "high": "High",
    "office": "Office visit",
    "telehealth": "Telehealth",
    "lab": "Lab",
    "info": "Info",
    "warning": "Warning",
    "appointment": "Appointment",
    "medication": "Medication",
    "referral": "Referral",
    "general": "General",
    "result_follow_up": "Result follow-up",
    "imaging": "Imaging",
}

KNOWN_MISSING = {
    "Patient not found.",
    "Appointment not found.",
    "Task not found.",
    "Message not found.",
    "Result not found.",
}


def clean(value):
    return (value or "").strip()


def parse_int(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def normalize_datetime(value):
    text = clean(value).replace("T", " ")
    if len(text) == 16:
        text += ":00"
    try:
        datetime.strptime(text, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return None
    return text


def normalize_date(value):
    text = clean(value)
    try:
        datetime.strptime(text, "%Y-%m-%d")
    except ValueError:
        return None
    return text


def format_when(value):
    if not value:
        return ""
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            parsed = datetime.strptime(value, fmt)
        except ValueError:
            continue
        if fmt == "%Y-%m-%d":
            return f"{parsed.strftime('%b')} {parsed.day}, {parsed.year}"
        hour = parsed.strftime("%I").lstrip("0") or "0"
        return (
            f"{parsed.strftime('%b')} {parsed.day}, {parsed.year}"
            f" · {hour}:{parsed.strftime('%M')} {parsed.strftime('%p')}"
        )
    return value


def label_text(value):
    if value is None or value == "":
        return ""
    return LABELS.get(value, str(value).replace("_", " ").capitalize())


def visit_label(value):
    if value == "lab":
        return "Lab visit"
    return label_text(value)


def require_patient(patient_id):
    patient = db.get_patient(patient_id)
    if patient is None:
        abort(404, description="Patient not found.")
    return patient


def show_appointments(patient, errors=None, form=None, status_code=200):
    return (
        render_template(
            "appointments.html",
            patient=patient,
            appointments=db.list_appointments(patient["id"]),
            providers=db.list_providers(),
            departments=db.list_departments(),
            errors=errors or [],
            form=form or {},
        ),
        status_code,
    )


def show_tasks(patient, errors=None, form=None, status_code=200):
    return (
        render_template(
            "tasks.html",
            patient=patient,
            tasks=db.list_tasks(patient["id"]),
            summaries=db.list_visit_summaries(patient["id"]),
            errors=errors or [],
            form=form or {},
        ),
        status_code,
    )


def create_app(db_path=None):
    path = str(db_path or db.DEFAULT_DB)
    if not os.path.exists(path):
        db.init_db(path, quiet=True)

    app = Flask(__name__)
    app.config["DB_PATH"] = path
    app.secret_key = "care-overview-dev"

    app.template_filter("when")(format_when)
    app.template_filter("label")(label_text)
    app.template_filter("visit_label")(visit_label)

    @app.before_request
    def open_connection():
        db.connect(app.config["DB_PATH"])

    @app.teardown_appcontext
    def close_connection(exc):
        db.close(exc)

    @app.errorhandler(404)
    def not_found(error):
        description = getattr(error, "description", "") or ""
        if description in KNOWN_MISSING:
            message = description
        else:
            message = "That page does not exist."
        return render_template("error.html", message=message), 404

    @app.get("/")
    def home():
        return render_template("patients.html", patients=db.list_patients())

    @app.get("/patients")
    def patients():
        return render_template("patients.html", patients=db.list_patients())

    @app.get("/dashboard/<int:patient_id>")
    def dashboard(patient_id):
        patient = require_patient(patient_id)
        overview = db.care_overview(patient_id)
        return render_template(
            "dashboard.html",
            patient=patient,
            overview=overview,
            recent_visit=db.recent_visit(patient_id),
            upcoming=db.upcoming_appointment(patient_id),
            tasks=db.list_tasks(patient_id, open_only=True),
            priorities=db.task_counts_by_priority(patient_id),
            referrals=db.active_referrals(patient_id),
            notifications=db.open_notifications(patient_id),
            quick_links=db.quick_links(patient_id),
        )

    @app.get("/appointments/<int:patient_id>")
    def appointments(patient_id):
        patient = require_patient(patient_id)
        return show_appointments(patient)

    @app.post("/appointments")
    def create_appointment():
        form = {
            "patient_id": clean(request.form.get("patient_id")),
            "provider_id": clean(request.form.get("provider_id")),
            "department_id": clean(request.form.get("department_id")),
            "starts_at": clean(request.form.get("starts_at")),
            "visit_type": clean(request.form.get("visit_type")),
            "location": clean(request.form.get("location")),
            "reason": clean(request.form.get("reason")),
            "prep_notes": clean(request.form.get("prep_notes")),
        }
        patient_id = parse_int(form["patient_id"])
        if patient_id is None:
            abort(404, description="Patient not found.")
        patient = require_patient(patient_id)

        errors = []
        provider_id = parse_int(form["provider_id"])
        department_id = parse_int(form["department_id"])
        starts_at = normalize_datetime(form["starts_at"])
        if provider_id is None or db.get_provider(provider_id) is None:
            errors.append("Choose a provider.")
        if department_id is None or db.get_department(department_id) is None:
            errors.append("Choose a department.")
        if not form["starts_at"]:
            errors.append("Date and time are required.")
        elif starts_at is None:
            errors.append("Enter a valid date and time.")
        if not form["visit_type"]:
            errors.append("Visit type is required.")
        if not form["location"]:
            errors.append("Location is required.")
        if not form["reason"]:
            errors.append("Reason is required.")
        if errors:
            return show_appointments(patient, errors, form, 400)

        try:
            db.create_appointment(
                patient_id,
                provider_id,
                department_id,
                starts_at,
                form["visit_type"],
                form["location"],
                form["reason"],
                form["prep_notes"] or None,
            )
        except sqlite3.IntegrityError:
            errors.append("That appointment could not be saved.")
            return show_appointments(patient, errors, form, 400)

        flash("Appointment added.", "success")
        return redirect(url_for("appointments", patient_id=patient_id))

    @app.post("/appointments/<int:appointment_id>/cancel")
    def cancel_appointment(appointment_id):
        appointment, outcome = db.cancel_appointment(appointment_id)
        if appointment is None:
            abort(404, description="Appointment not found.")
        if outcome == "not_scheduled":
            flash("Only scheduled appointments can be cancelled.", "error")
        else:
            flash("Appointment cancelled.", "success")
        return redirect(url_for("appointments", patient_id=appointment["patient_id"]))

    @app.get("/tasks/<int:patient_id>")
    def tasks(patient_id):
        patient = require_patient(patient_id)
        return show_tasks(patient)

    @app.post("/tasks")
    def create_task():
        form = {
            "patient_id": clean(request.form.get("patient_id")),
            "title": clean(request.form.get("title")),
            "details": clean(request.form.get("details")),
            "task_type": clean(request.form.get("task_type")),
            "due_at": clean(request.form.get("due_at")),
            "priority": clean(request.form.get("priority")),
            "visit_summary_id": clean(request.form.get("visit_summary_id")),
        }
        patient_id = parse_int(form["patient_id"])
        if patient_id is None:
            abort(404, description="Patient not found.")
        patient = require_patient(patient_id)

        errors = []
        due_at = normalize_date(form["due_at"])
        summary_id = None
        if not form["title"]:
            errors.append("Title is required.")
        if not form["task_type"]:
            errors.append("Task type is required.")
        if not form["due_at"]:
            errors.append("Due date is required.")
        elif due_at is None:
            errors.append("Enter a valid due date.")
        if form["priority"] not in ("low", "normal", "high"):
            errors.append("Choose a priority.")
        if form["visit_summary_id"]:
            summary_id = parse_int(form["visit_summary_id"])
            if summary_id is None or db.visit_summary_for_patient(summary_id, patient_id) is None:
                errors.append("That visit summary does not belong to this patient.")
        if errors:
            return show_tasks(patient, errors, form, 400)

        try:
            db.create_task(
                patient_id,
                form["title"],
                form["details"] or None,
                form["task_type"],
                due_at,
                form["priority"],
                summary_id,
            )
        except sqlite3.IntegrityError:
            errors.append("That task could not be saved.")
            return show_tasks(patient, errors, form, 400)

        flash("Task added.", "success")
        return redirect(url_for("tasks", patient_id=patient_id))

    @app.post("/tasks/<int:task_id>/complete")
    def complete_task(task_id):
        task, outcome = db.complete_task(task_id)
        if task is None:
            abort(404, description="Task not found.")
        if outcome == "already":
            flash("Task is already complete.", "error")
        else:
            flash("Task marked complete.", "success")
        return redirect(url_for("tasks", patient_id=task["patient_id"]))

    @app.post("/tasks/<int:task_id>/delete")
    def delete_task(task_id):
        task = db.delete_task(task_id)
        if task is None:
            abort(404, description="Task not found.")
        flash("Task deleted.", "success")
        return redirect(url_for("tasks", patient_id=task["patient_id"]))

    @app.get("/messages/<int:patient_id>")
    def messages(patient_id):
        patient = require_patient(patient_id)
        return render_template(
            "messages.html",
            patient=patient,
            messages=db.list_messages(patient_id),
        )

    @app.post("/messages/<int:message_id>/read")
    def read_message(message_id):
        message, outcome = db.mark_message_read(message_id)
        if message is None:
            abort(404, description="Message not found.")
        if outcome == "already":
            flash("Message is already read.", "error")
        else:
            flash("Message marked read.", "success")
        return redirect(url_for("messages", patient_id=message["patient_id"]))

    @app.get("/results/<int:patient_id>")
    def results(patient_id):
        patient = require_patient(patient_id)
        return render_template(
            "results.html",
            patient=patient,
            results=db.list_results(patient_id),
        )

    @app.post("/results/<int:result_id>/review")
    def review_result(result_id):
        existing = db.get_result(result_id)
        if existing is None:
            abort(404, description="Result not found.")
        try:
            outcome = db.review_result(result_id)
        except sqlite3.IntegrityError:
            flash("The result could not be reviewed.", "error")
            return redirect(url_for("results", patient_id=existing["patient_id"]))
        if outcome["outcome"] == "already":
            flash("Result is already reviewed.", "error")
        elif outcome["task_created"]:
            flash("Result marked reviewed. A follow-up task was added.", "success")
        else:
            flash("Result marked reviewed.", "success")
        return redirect(url_for("results", patient_id=outcome["patient_id"]))

    @app.get("/medications/<int:patient_id>")
    def medications(patient_id):
        patient = require_patient(patient_id)
        return render_template(
            "medications.html",
            patient=patient,
            medications=db.list_medications(patient_id),
        )

    @app.get("/api/care-overview/<int:patient_id>")
    def care_overview_api(patient_id):
        if db.get_patient(patient_id) is None:
            return jsonify({"error": "Patient not found."}), 404
        return jsonify(
            {
                "overview": db.care_overview(patient_id),
                "recent_visit": db.recent_visit(patient_id),
                "upcoming_appointment": db.upcoming_appointment(patient_id),
                "tasks_by_priority": db.task_counts_by_priority(patient_id),
            }
        )

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
