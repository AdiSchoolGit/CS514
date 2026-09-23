const apiBase = window.CARE_OVERVIEW_API_BASE || "";
const storeKey = "care-overview-demo-state";

const seed = {
  patients: [
    {
      id: "p1",
      firstName: "Maya",
      lastName: "Reed",
      dob: "1971-04-18",
      context: "Managing follow-up care after a family medicine visit",
      team: "Family Medicine"
    },
    {
      id: "p2",
      firstName: "Leon",
      lastName: "Brooks",
      dob: "1988-11-02",
      context: "Reviewing new lab results and a refill reminder",
      team: "Primary Care"
    },
    {
      id: "p3",
      firstName: "Elena",
      lastName: "Park",
      dob: "1959-07-26",
      context: "Coordinating appointments across multiple departments",
      team: "Cardiology"
    }
  ],
  departments: [
    { id: "d1", name: "Family Medicine", phone: "555-0101" },
    { id: "d2", name: "Cardiology", phone: "555-0102" },
    { id: "d3", name: "Laboratory", phone: "555-0103" },
    { id: "d4", name: "Physical Therapy", phone: "555-0104" }
  ],
  providers: [
    { id: "pr1", departmentId: "d1", fullName: "Dr. Amina Patel", role: "Physician", specialty: "Primary care" },
    { id: "pr2", departmentId: "d2", fullName: "Dr. Marcus Chen", role: "Cardiologist", specialty: "Heart health" },
    { id: "pr3", departmentId: "d3", fullName: "Jamie Alvarez", role: "Lab coordinator", specialty: "Lab services" },
    { id: "pr4", departmentId: "d4", fullName: "Taylor Kim", role: "Physical therapist", specialty: "Mobility care" }
  ],
  appointments: [
    { id: "a1", patientId: "p1", providerId: "pr1", departmentId: "d1", startsAt: "2026-09-16T09:30", visitType: "Office visit", location: "Clinic A, Room 204", reason: "Medication follow-up", status: "completed", checkInStatus: "complete", prepNotes: "" },
    { id: "a2", patientId: "p1", providerId: "pr3", departmentId: "d3", startsAt: "2026-09-28T08:15", visitType: "Lab visit", location: "Main lab", reason: "Follow-up blood work", status: "scheduled", checkInStatus: "available", prepNotes: "Bring photo ID. Fasting is listed in the visit instructions." },
    { id: "a3", patientId: "p2", providerId: "pr1", departmentId: "d1", startsAt: "2026-09-12T14:00", visitType: "Telehealth", location: "Video visit", reason: "Results review", status: "completed", checkInStatus: "complete", prepNotes: "" },
    { id: "a4", patientId: "p2", providerId: "pr1", departmentId: "d1", startsAt: "2026-10-03T11:30", visitType: "Office visit", location: "Clinic B, Room 118", reason: "Medication check", status: "scheduled", checkInStatus: "not_started", prepNotes: "Bring current medication list." },
    { id: "a5", patientId: "p3", providerId: "pr2", departmentId: "d2", startsAt: "2026-09-10T10:00", visitType: "Office visit", location: "Heart center", reason: "Cardiology follow-up", status: "completed", checkInStatus: "complete", prepNotes: "" },
    { id: "a6", patientId: "p3", providerId: "pr4", departmentId: "d4", startsAt: "2026-09-30T15:45", visitType: "Office visit", location: "Rehab suite", reason: "Mobility evaluation", status: "scheduled", checkInStatus: "available", prepNotes: "Wear comfortable shoes." }
  ],
  visitSummaries: [
    { id: "v1", appointmentId: "a1", reason: "Medication follow-up", summary: "Reviewed blood pressure readings and current medications.", instructions: "Continue tracking home readings and complete follow-up lab work before the next appointment.", medicationChanges: "Morning dose timing was updated.", followUpPlan: "Complete lab work and review medication instructions." },
    { id: "v2", appointmentId: "a3", reason: "Results review", summary: "Discussed recently released lab summary and routine care plan.", instructions: "Review the care team message and schedule the next medication check.", medicationChanges: "No medication changes recorded.", followUpPlan: "Schedule office visit and review refill timing." },
    { id: "v3", appointmentId: "a5", reason: "Cardiology follow-up", summary: "Reviewed recent symptoms, activity level, and referral needs.", instructions: "Schedule physical therapy evaluation and complete pre-visit forms.", medicationChanges: "No medication changes recorded.", followUpPlan: "Keep cardiology follow-up and start therapy evaluation." }
  ],
  tasks: [
    { id: "t1", patientId: "p1", visitSummaryId: "v1", title: "Complete follow-up lab work", details: "Lab order is ready at the main lab.", type: "Lab", dueAt: "2026-09-28", status: "open", priority: "high" },
    { id: "t2", patientId: "p1", visitSummaryId: "v1", title: "Review updated medication instructions", details: "Check the visit summary before the next dose change.", type: "Medication", dueAt: "2026-09-25", status: "open", priority: "normal" },
    { id: "t3", patientId: "p2", visitSummaryId: "v2", title: "Schedule medication check", details: "Choose an appointment time in early October.", type: "Appointment", dueAt: "2026-09-29", status: "complete", priority: "normal" },
    { id: "t4", patientId: "p3", visitSummaryId: "v3", title: "Complete therapy intake forms", details: "Forms are available before the physical therapy visit.", type: "Form", dueAt: "2026-09-29", status: "open", priority: "normal" },
    { id: "t5", patientId: "p3", visitSummaryId: "v3", title: "Schedule referral appointment", details: "Referral is approved for physical therapy evaluation.", type: "Referral", dueAt: "2026-09-27", status: "open", priority: "high" }
  ],
  messages: [
    { id: "m1", patientId: "p1", providerId: "pr1", subject: "Medication instructions", body: "Please review the updated timing listed in your visit summary.", sentAt: "2026-09-20T13:10", status: "unread" },
    { id: "m2", patientId: "p1", providerId: "pr3", subject: "Lab appointment reminder", body: "Your lab order is ready. Please arrive 10 minutes early.", sentAt: "2026-09-21T09:45", status: "read" },
    { id: "m3", patientId: "p2", providerId: "pr1", subject: "Follow-up visit confirmed", body: "Your medication check is scheduled for October 3.", sentAt: "2026-09-19T16:30", status: "read" },
    { id: "m4", patientId: "p3", providerId: "pr2", subject: "Referral next step", body: "Your therapy referral is available for scheduling.", sentAt: "2026-09-20T11:15", status: "unread" }
  ],
  results: [
    { id: "r1", patientId: "p1", providerId: "pr1", testName: "Basic metabolic panel", category: "Lab", collectedAt: "2026-09-18", releasedAt: "2026-09-20", status: "new", valueSummary: "Released to patient portal. Review with care team if you have questions." },
    { id: "r2", patientId: "p2", providerId: "pr1", testName: "Lipid panel", category: "Lab", collectedAt: "2026-09-10", releasedAt: "2026-09-12", status: "reviewed", valueSummary: "Reviewed during telehealth visit." },
    { id: "r3", patientId: "p3", providerId: "pr2", testName: "Routine heart monitoring summary", category: "Report", collectedAt: "2026-09-09", releasedAt: "2026-09-12", status: "new", valueSummary: "Released to patient portal. Summary is available for review." }
  ],
  medications: [
    { id: "med1", patientId: "p1", name: "Lisinopril", dosage: "10 mg", frequency: "Once daily", startedAt: "2026-05-03", status: "active" },
    { id: "med2", patientId: "p1", name: "Vitamin D", dosage: "1000 IU", frequency: "Once daily", startedAt: "2026-06-14", status: "active" },
    { id: "med3", patientId: "p2", name: "Atorvastatin", dosage: "20 mg", frequency: "Once nightly", startedAt: "2026-07-02", status: "active" },
    { id: "med4", patientId: "p3", name: "Metoprolol", dosage: "25 mg", frequency: "Twice daily", startedAt: "2026-03-21", status: "active" }
  ],
  prescriptions: [
    { id: "rx1", medicationId: "med1", providerId: "pr1", pharmacy: "Campus Pharmacy", refillsRemaining: 2, lastFilledAt: "2026-09-02", nextRefillAt: "2026-09-30", status: "active" },
    { id: "rx2", medicationId: "med2", providerId: "pr1", pharmacy: "Campus Pharmacy", refillsRemaining: 1, lastFilledAt: "2026-08-18", nextRefillAt: "2026-09-24", status: "refill_due" },
    { id: "rx3", medicationId: "med3", providerId: "pr1", pharmacy: "Northside Pharmacy", refillsRemaining: 3, lastFilledAt: "2026-09-01", nextRefillAt: "2026-10-01", status: "active" },
    { id: "rx4", medicationId: "med4", providerId: "pr2", pharmacy: "Heart Center Pharmacy", refillsRemaining: 0, lastFilledAt: "2026-08-29", nextRefillAt: "2026-09-26", status: "refill_due" }
  ],
  referrals: [
    { id: "ref1", patientId: "p1", providerId: "pr1", departmentId: "d3", reason: "Follow-up lab work", status: "scheduled", createdAt: "2026-09-16", expiresAt: "2026-10-16" },
    { id: "ref2", patientId: "p3", providerId: "pr2", departmentId: "d4", reason: "Physical therapy evaluation", status: "pending", createdAt: "2026-09-10", expiresAt: "2026-10-10" }
  ],
  notifications: [
    { id: "n1", patientId: "p1", sourceType: "result", sourceId: "r1", title: "New test result", body: "A lab result was released.", severity: "info", status: "open" },
    { id: "n2", patientId: "p1", sourceType: "message", sourceId: "m1", title: "Unread provider message", body: "You have a message about medication instructions.", severity: "info", status: "open" },
    { id: "n3", patientId: "p3", sourceType: "message", sourceId: "m4", title: "Unread provider message", body: "You have a message about a referral.", severity: "info", status: "open" },
    { id: "n4", patientId: "p3", sourceType: "referral", sourceId: "ref2", title: "Referral needs scheduling", body: "Physical therapy referral is ready.", severity: "warning", status: "open" }
  ]
};

let state = loadState();
let activePatientId = state.patients[0].id;
let activeView = "overview";
let toastTimer;

const el = {
  patientSelect: document.querySelector("#patient-select"),
  patientName: document.querySelector("#patient-name"),
  patientContext: document.querySelector("#patient-context"),
  patientDob: document.querySelector("#patient-dob"),
  patientTeam: document.querySelector("#patient-team"),
  lastUpdated: document.querySelector("#last-updated"),
  dataSource: document.querySelector("#data-source"),
  recentVisit: document.querySelector("#recent-visit"),
  recentVisitDate: document.querySelector("#recent-visit-date"),
  nextAppointment: document.querySelector("#next-appointment"),
  taskList: document.querySelector("#task-list"),
  updatesList: document.querySelector("#updates-list"),
  appointmentsList: document.querySelector("#appointments-list"),
  messagesList: document.querySelector("#messages-list"),
  resultsList: document.querySelector("#results-list"),
  medicationsList: document.querySelector("#medications-list"),
  allTasksList: document.querySelector("#all-tasks-list"),
  countTasks: document.querySelector("#count-tasks"),
  countMessages: document.querySelector("#count-messages"),
  countResults: document.querySelector("#count-results"),
  countReferrals: document.querySelector("#count-referrals"),
  taskForm: document.querySelector("#task-form"),
  appointmentForm: document.querySelector("#appointment-form"),
  toast: document.querySelector("#toast")
};

const api = {
  async getData() {
    if (apiBase) {
      const res = await fetch(`${apiBase}/api/care-overview`);
      if (!res.ok) throw new Error("Could not load care overview");
      return res.json();
    }
    return clone(state);
  },
  async saveData(nextState) {
    if (apiBase) {
      const res = await fetch(`${apiBase}/api/care-overview`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(nextState)
      });
      if (!res.ok) throw new Error("Could not save care overview");
      return res.json();
    }
    state = clone(nextState);
    localStorage.setItem(storeKey, JSON.stringify(state));
    return clone(state);
  }
};

function clone(value) {
  return JSON.parse(JSON.stringify(value));
}

function loadState() {
  const stored = localStorage.getItem(storeKey);
  if (!stored) return clone(seed);
  try {
    return JSON.parse(stored);
  } catch {
    localStorage.removeItem(storeKey);
    return clone(seed);
  }
}

function save() {
  return api.saveData(state);
}

function byId(list, id) {
  return list.find((item) => item.id === id);
}

function patientItems(list) {
  return list.filter((item) => item.patientId === activePatientId);
}

function providerName(id) {
  return byId(state.providers, id)?.fullName || "Care team";
}

function departmentName(id) {
  return byId(state.departments, id)?.name || "Department";
}

function formatDate(value) {
  if (!value) return "Not set";
  return new Intl.DateTimeFormat("en-US", { month: "short", day: "numeric", year: "numeric" }).format(new Date(value));
}

function formatDateTime(value) {
  if (!value) return "Not set";
  return new Intl.DateTimeFormat("en-US", { month: "short", day: "numeric", hour: "numeric", minute: "2-digit" }).format(new Date(value));
}

function todayIso() {
  return new Date().toISOString().slice(0, 10);
}

function statusClass(status) {
  if (["complete", "completed", "reviewed", "read", "scheduled", "active"].includes(status)) return "success";
  if (["open", "new", "unread", "pending", "available", "refill_due"].includes(status)) return "warning";
  if (["cancelled", "missed", "expired"].includes(status)) return "error";
  return "neutral";
}

function cleanStatus(status) {
  return String(status).replaceAll("_", " ");
}

function setText(node, value) {
  node.textContent = value;
}

function emptyState(title, detail) {
  return `<div class="empty"><strong>${title}</strong><p>${detail}</p></div>`;
}

function itemTemplate(title, detail, meta, status, actions = "") {
  return `
    <article class="item">
      <div class="item-main">
        <div>
          <h4>${title}</h4>
          <p>${detail}</p>
        </div>
        <span class="status ${statusClass(status)}">${cleanStatus(status)}</span>
      </div>
      <p>${meta}</p>
      ${actions ? `<div class="item-actions">${actions}</div>` : ""}
    </article>
  `;
}

function overviewCounts() {
  const tasks = patientItems(state.tasks).filter((task) => task.status === "open");
  const messages = patientItems(state.messages).filter((message) => message.status === "unread");
  const results = patientItems(state.results).filter((result) => result.status === "new");
  const referrals = patientItems(state.referrals).filter((referral) => ["pending", "scheduled"].includes(referral.status));
  return { tasks, messages, results, referrals };
}

function recentVisit() {
  const visits = state.appointments
    .filter((appointment) => appointment.patientId === activePatientId && appointment.status === "completed")
    .sort((a, b) => new Date(b.startsAt) - new Date(a.startsAt));
  const appointment = visits[0];
  if (!appointment) return null;
  const summary = state.visitSummaries.find((visit) => visit.appointmentId === appointment.id);
  return { appointment, summary };
}

function nextAppointment() {
  const now = new Date("2026-09-23T12:00");
  return state.appointments
    .filter((appointment) => appointment.patientId === activePatientId && appointment.status === "scheduled" && new Date(appointment.startsAt) >= now)
    .sort((a, b) => new Date(a.startsAt) - new Date(b.startsAt))[0];
}

function renderPatientPicker() {
  el.patientSelect.innerHTML = state.patients.map((patient) => {
    const name = `${patient.firstName} ${patient.lastName}`;
    return `<option value="${patient.id}">${name}</option>`;
  }).join("");
  el.patientSelect.value = activePatientId;
}

function renderShell() {
  const patient = byId(state.patients, activePatientId);
  setText(el.patientName, `${patient.firstName} ${patient.lastName}`);
  setText(el.patientContext, patient.context);
  setText(el.patientDob, formatDate(patient.dob));
  setText(el.patientTeam, patient.team);
  setText(el.lastUpdated, new Intl.DateTimeFormat("en-US", { hour: "numeric", minute: "2-digit", month: "short", day: "numeric" }).format(new Date()));
  setText(el.dataSource, apiBase ? "Backend API mode" : "Local frontend mode");
}

function renderCounts() {
  const counts = overviewCounts();
  setText(el.countTasks, counts.tasks.length);
  setText(el.countMessages, counts.messages.length);
  setText(el.countResults, counts.results.length);
  setText(el.countReferrals, counts.referrals.length);
}

function renderRecentVisit() {
  const visit = recentVisit();
  if (!visit) {
    el.recentVisitDate.textContent = "No visit";
    el.recentVisit.innerHTML = emptyState("No completed visits", "Completed visit summaries will appear here.");
    return;
  }
  const { appointment, summary } = visit;
  el.recentVisitDate.textContent = formatDate(appointment.startsAt);
  el.recentVisit.innerHTML = `
    <div class="summary-stack">
      <div class="summary-line">
        <strong>${providerName(appointment.providerId)} - ${departmentName(appointment.departmentId)}</strong>
        <p>${appointment.reason}</p>
      </div>
      <div class="summary-line">
        <strong>What happened</strong>
        <p>${summary?.summary || "No summary entered."}</p>
      </div>
      <div class="summary-line">
        <strong>Main instructions</strong>
        <p>${summary?.instructions || "No instructions entered."}</p>
      </div>
      <div class="summary-line">
        <strong>Medication changes</strong>
        <p>${summary?.medicationChanges || "No medication changes recorded."}</p>
      </div>
      <div class="summary-line">
        <strong>Follow-up plan</strong>
        <p>${summary?.followUpPlan || "No follow-up plan entered."}</p>
      </div>
    </div>
  `;
}

function renderNextAppointment() {
  const appointment = nextAppointment();
  if (!appointment) {
    el.nextAppointment.innerHTML = emptyState("No upcoming appointment", "Scheduled appointments will appear here.");
    return;
  }
  el.nextAppointment.innerHTML = `
    <div class="summary-stack">
      <div class="summary-line">
        <strong>${formatDateTime(appointment.startsAt)}</strong>
        <p>${providerName(appointment.providerId)}</p>
      </div>
      <div class="summary-line">
        <strong>${departmentName(appointment.departmentId)}</strong>
        <p>${appointment.location}</p>
      </div>
      <div class="summary-line">
        <strong>Reason</strong>
        <p>${appointment.reason}</p>
      </div>
      <div class="summary-line">
        <strong>Before you go</strong>
        <p>${appointment.prepNotes || "No preparation instructions listed."}</p>
      </div>
    </div>
  `;
}

function renderTaskPreview() {
  const tasks = patientItems(state.tasks)
    .filter((task) => task.status === "open")
    .sort((a, b) => new Date(a.dueAt) - new Date(b.dueAt))
    .slice(0, 4);
  if (!tasks.length) {
    el.taskList.innerHTML = emptyState("No open tasks", "Follow-up tasks from your care team will appear here.");
    return;
  }
  el.taskList.innerHTML = tasks.map((task) => itemTemplate(
    task.title,
    task.details || "No details entered.",
    `${task.type} - Due ${formatDate(task.dueAt)} - ${task.priority} priority`,
    task.priority === "high" ? "open" : "neutral",
    `<button class="button secondary" type="button" data-action="complete-task" data-id="${task.id}">Mark complete</button>`
  )).join("");
}

function renderUpdates() {
  const counts = overviewCounts();
  const updates = [
    ...counts.messages.map((message) => ({ title: message.subject, detail: `Message from ${providerName(message.providerId)}`, meta: formatDateTime(message.sentAt), status: message.status, action: "read-message", id: message.id, label: "Mark read" })),
    ...counts.results.map((result) => ({ title: result.testName, detail: result.valueSummary, meta: `Released ${formatDate(result.releasedAt)}`, status: result.status, action: "review-result", id: result.id, label: "Mark reviewed" })),
    ...counts.referrals.map((referral) => ({ title: departmentName(referral.departmentId), detail: referral.reason, meta: `Expires ${formatDate(referral.expiresAt)}`, status: referral.status }))
  ];
  if (!updates.length) {
    el.updatesList.innerHTML = emptyState("No updates need review", "Unread messages, new results, and referrals will appear here.");
    return;
  }
  el.updatesList.innerHTML = updates.map((update) => itemTemplate(
    update.title,
    update.detail,
    update.meta,
    update.status,
    update.action ? `<button class="button secondary" type="button" data-action="${update.action}" data-id="${update.id}">${update.label}</button>` : ""
  )).join("");
}

function renderAppointments() {
  const providerOptions = state.providers.map((provider) => `<option value="${provider.id}">${provider.fullName}</option>`).join("");
  el.appointmentForm.elements.providerId.innerHTML = providerOptions;
  const appointments = patientItems(state.appointments).sort((a, b) => new Date(b.startsAt) - new Date(a.startsAt));
  if (!appointments.length) {
    el.appointmentsList.innerHTML = emptyState("No appointments", "Appointments you add will appear here.");
    return;
  }
  el.appointmentsList.innerHTML = appointments.map((appointment) => itemTemplate(
    appointment.reason,
    `${formatDateTime(appointment.startsAt)} - ${appointment.visitType}`,
    `${providerName(appointment.providerId)} - ${departmentName(appointment.departmentId)} - ${appointment.location}`,
    appointment.status,
    appointment.status === "scheduled" ? `<button class="button danger" type="button" data-action="cancel-appointment" data-id="${appointment.id}">Cancel appointment</button>` : ""
  )).join("");
}

function renderMessages() {
  const messages = patientItems(state.messages).sort((a, b) => new Date(b.sentAt) - new Date(a.sentAt));
  if (!messages.length) {
    el.messagesList.innerHTML = emptyState("No messages", "Messages from fictional providers will appear here.");
    return;
  }
  el.messagesList.innerHTML = messages.map((message) => itemTemplate(
    message.subject,
    message.body,
    `${providerName(message.providerId)} - ${formatDateTime(message.sentAt)}`,
    message.status,
    message.status === "unread" ? `<button class="button secondary" type="button" data-action="read-message" data-id="${message.id}">Mark read</button>` : ""
  )).join("");
}

function renderResults() {
  const results = patientItems(state.results).sort((a, b) => new Date(b.releasedAt) - new Date(a.releasedAt));
  if (!results.length) {
    el.resultsList.innerHTML = emptyState("No released results", "Released test result summaries will appear here.");
    return;
  }
  el.resultsList.innerHTML = results.map((result) => itemTemplate(
    result.testName,
    result.valueSummary,
    `${result.category} - Collected ${formatDate(result.collectedAt)} - Released ${formatDate(result.releasedAt)}`,
    result.status,
    result.status === "new" ? `<button class="button secondary" type="button" data-action="review-result" data-id="${result.id}">Mark reviewed</button>` : ""
  )).join("");
}

function renderMedications() {
  const medications = patientItems(state.medications);
  if (!medications.length) {
    el.medicationsList.innerHTML = emptyState("No medications listed", "Active medications and refill reminders will appear here.");
    return;
  }
  el.medicationsList.innerHTML = medications.map((medication) => {
    const rx = state.prescriptions.find((prescription) => prescription.medicationId === medication.id);
    const detail = `${medication.dosage} - ${medication.frequency}`;
    const meta = rx ? `${rx.pharmacy} - ${rx.refillsRemaining} refills left - Next refill ${formatDate(rx.nextRefillAt)}` : "No prescription details listed";
    return itemTemplate(medication.name, detail, meta, rx?.status || medication.status);
  }).join("");
}

function renderTasks() {
  const tasks = patientItems(state.tasks).sort((a, b) => new Date(a.dueAt) - new Date(b.dueAt));
  if (!tasks.length) {
    el.allTasksList.innerHTML = emptyState("No tasks", "Tasks you add will appear here.");
    return;
  }
  el.allTasksList.innerHTML = tasks.map((task) => itemTemplate(
    task.title,
    task.details || "No details entered.",
    `${task.type} - Due ${formatDate(task.dueAt)} - ${task.priority} priority`,
    task.status,
    `
      ${task.status === "open" ? `<button class="button secondary" type="button" data-action="complete-task" data-id="${task.id}">Mark complete</button>` : ""}
      <button class="button danger" type="button" data-action="delete-task" data-id="${task.id}">Delete</button>
    `
  )).join("");
}

function render() {
  renderPatientPicker();
  renderShell();
  renderCounts();
  renderRecentVisit();
  renderNextAppointment();
  renderTaskPreview();
  renderUpdates();
  renderAppointments();
  renderMessages();
  renderResults();
  renderMedications();
  renderTasks();
}

function setView(view) {
  activeView = view;
  document.querySelectorAll(".view").forEach((node) => node.classList.toggle("is-visible", node.id === `view-${view}`));
  document.querySelectorAll(".nav-item").forEach((node) => node.classList.toggle("is-active", node.dataset.view === view));
  document.querySelector("#main").focus({ preventScroll: true });
}

function showToast(message) {
  clearTimeout(toastTimer);
  el.toast.textContent = message;
  el.toast.classList.add("is-visible");
  toastTimer = setTimeout(() => el.toast.classList.remove("is-visible"), 2600);
}

async function completeTask(id) {
  const task = byId(state.tasks, id);
  if (!task) return;
  task.status = "complete";
  task.completedAt = todayIso();
  await save();
  render();
  showToast("Task marked complete.");
}

async function deleteTask(id) {
  state.tasks = state.tasks.filter((task) => task.id !== id);
  await save();
  render();
  showToast("Task deleted.");
}

async function readMessage(id) {
  const message = byId(state.messages, id);
  if (!message) return;
  message.status = "read";
  message.readAt = new Date().toISOString();
  state.notifications.forEach((notification) => {
    if (notification.sourceType === "message" && notification.sourceId === id) {
      notification.status = "dismissed";
      notification.dismissedAt = new Date().toISOString();
    }
  });
  await save();
  render();
  showToast("Message marked read.");
}

async function reviewResult(id) {
  const result = byId(state.results, id);
  if (!result) return;
  result.status = "reviewed";
  result.reviewedAt = new Date().toISOString();
  state.notifications.forEach((notification) => {
    if (notification.sourceType === "result" && notification.sourceId === id) {
      notification.status = "dismissed";
      notification.dismissedAt = new Date().toISOString();
    }
  });
  await save();
  render();
  showToast("Result marked reviewed.");
}

async function cancelAppointment(id) {
  const appointment = byId(state.appointments, id);
  if (!appointment) return;
  appointment.status = "cancelled";
  await save();
  render();
  showToast("Appointment cancelled.");
}

function newId(prefix, list) {
  return `${prefix}${list.length + 1}-${Date.now().toString(36)}`;
}

async function addTask(event) {
  event.preventDefault();
  const form = new FormData(el.taskForm);
  state.tasks.push({
    id: newId("t", state.tasks),
    patientId: activePatientId,
    visitSummaryId: null,
    title: form.get("title").trim(),
    details: form.get("details").trim(),
    type: form.get("type"),
    dueAt: form.get("dueAt"),
    status: "open",
    priority: form.get("priority")
  });
  el.taskForm.reset();
  await save();
  render();
  showToast("Task added.");
}

async function addAppointment(event) {
  event.preventDefault();
  const form = new FormData(el.appointmentForm);
  const provider = byId(state.providers, form.get("providerId"));
  state.appointments.push({
    id: newId("a", state.appointments),
    patientId: activePatientId,
    providerId: provider.id,
    departmentId: provider.departmentId,
    startsAt: form.get("startsAt"),
    visitType: form.get("visitType"),
    location: form.get("visitType") === "Telehealth" ? "Video visit" : "Clinic scheduling pending",
    reason: form.get("reason").trim(),
    status: "scheduled",
    checkInStatus: "not_started",
    prepNotes: form.get("prepNotes").trim()
  });
  el.appointmentForm.reset();
  await save();
  render();
  showToast("Appointment added.");
}

async function resetDemo() {
  state = clone(seed);
  activePatientId = state.patients[0].id;
  localStorage.removeItem(storeKey);
  await save();
  render();
  setView("overview");
  showToast("Demo data reset.");
}

document.addEventListener("click", (event) => {
  const actionNode = event.target.closest("[data-action]");
  const jumpNode = event.target.closest("[data-jump]");
  const navNode = event.target.closest("[data-view]");
  if (actionNode) {
    const { action, id } = actionNode.dataset;
    if (action === "complete-task") completeTask(id);
    if (action === "delete-task") deleteTask(id);
    if (action === "read-message") readMessage(id);
    if (action === "review-result") reviewResult(id);
    if (action === "cancel-appointment") cancelAppointment(id);
  }
  if (jumpNode) setView(jumpNode.dataset.jump);
  if (navNode) setView(navNode.dataset.view);
});

el.patientSelect.addEventListener("change", (event) => {
  activePatientId = event.target.value;
  render();
  setView(activeView);
});

el.taskForm.addEventListener("submit", addTask);
el.appointmentForm.addEventListener("submit", addAppointment);
document.querySelector("#reset-demo").addEventListener("click", resetDemo);

api.getData()
  .then((data) => {
    state = data;
    activePatientId = state.patients[0].id;
    render();
    setView("overview");
  })
  .catch(() => {
    state = clone(seed);
    render();
    setView("overview");
    showToast("Using local demo data.");
  });
