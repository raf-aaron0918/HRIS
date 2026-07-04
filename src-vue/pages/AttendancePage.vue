<template>
  <div>
    <BreadcrumbBar section="HR Modules" current="Time & Attendance" />

    <div class="row g-3">
      <div class="col-md-6 col-xl-3">
        <div class="card border-0 shadow-sm h-100">
          <div class="card-body">
            <small class="text-muted d-block mb-2">Present Today</small>
            <div class="d-flex align-items-end justify-content-between">
              <div>
                <h3 class="mb-1">{{ overview.presentCount }}</h3>
                <span class="text-muted small">Employees with valid logs</span>
              </div>
              <span class="badge bg-light-success text-success">Live</span>
            </div>
          </div>
        </div>
      </div>

      <div class="col-md-6 col-xl-3">
        <div class="card border-0 shadow-sm h-100">
          <div class="card-body">
            <small class="text-muted d-block mb-2">Late Cases</small>
            <div class="d-flex align-items-end justify-content-between">
              <div>
                <h3 class="mb-1">{{ overview.lateCount }}</h3>
                <span class="text-muted small">Need monitoring today</span>
              </div>
              <span class="badge bg-light-warning text-warning">Late</span>
            </div>
          </div>
        </div>
      </div>

      <div class="col-md-6 col-xl-3">
        <div class="card border-0 shadow-sm h-100">
          <div class="card-body">
            <small class="text-muted d-block mb-2">Correction Queue</small>
            <div class="d-flex align-items-end justify-content-between">
              <div>
                <h3 class="mb-1">{{ overview.correctionCount }}</h3>
                <span class="text-muted small">Pending supervisor action</span>
              </div>
              <span class="badge bg-light-info text-info">Queue</span>
            </div>
          </div>
        </div>
      </div>

      <div class="col-md-6 col-xl-3">
        <div class="card border-0 shadow-sm h-100">
          <div class="card-body">
            <small class="text-muted d-block mb-2">Premium Work</small>
            <div class="d-flex align-items-end justify-content-between">
              <div>
                <h3 class="mb-1">{{ overview.premiumCount }}</h3>
                <span class="text-muted small">OT, holiday, or night diff</span>
              </div>
              <span class="badge bg-light-danger text-danger">Payroll</span>
            </div>
          </div>
        </div>
      </div>

      <div class="col-lg-8">
        <div class="card h-100">
          <div class="card-header d-flex align-items-center justify-content-between">
            <div>
              <h5 class="mb-0">Attendance Entry</h5>
              <small class="text-muted">Record shift logs and corrections for payroll reconciliation.</small>
            </div>
            <span class="badge" :class="adjustmentBadge.class">{{ adjustmentBadge.label }}</span>
          </div>
          <div class="card-body">
            <form novalidate @submit.prevent="handleSubmit">
              <div class="d-flex align-items-center justify-content-between mb-3">
                <div>
                  <h6 class="mb-1">1. Employee and shift</h6>
                  <p class="text-muted mb-0 small">Select the employee, work date, and assigned schedule.</p>
                </div>
              </div>

              <div class="row">
                <div class="col-md-6 mb-3">
                  <label class="form-label" for="employeeSelect">Employee</label>
                  <select id="employeeSelect" v-model="form.employeeSelect" class="form-select" :class="fieldClass('employeeSelect')" required @change="handleEmployeeChange">
                    <option value="">Select employee</option>
                    <option v-for="employee in employeeOptions" :key="employee.employee_code" :value="employee.employee_code">
                      {{ employee.employee_code }} - {{ employee.name }}
                    </option>
                  </select>
                  <div class="invalid-feedback">{{ validationErrors.employeeSelect }}</div>
                </div>
                <div class="col-md-3 mb-3">
                  <label class="form-label" for="employeeId">Employee ID</label>
                  <input id="employeeId" :value="form.employeeSelect" type="text" class="form-control" placeholder="Auto-filled" readonly>
                </div>
                <div class="col-md-3 mb-3">
                  <label class="form-label" for="workDate">Date</label>
                  <input id="workDate" v-model="form.workDate" type="date" class="form-control" :class="fieldClass('workDate')" required @input="handleFormMutation('workDate')">
                  <div class="invalid-feedback">{{ validationErrors.workDate }}</div>
                </div>

                <div class="col-md-4 mb-3">
                  <label class="form-label" for="shiftSchedule">Shift Schedule</label>
                  <select id="shiftSchedule" v-model="form.shiftSchedule" class="form-select" @change="applyShiftPreset">
                    <option value="regular">Regular Day Shift</option>
                    <option value="night">Night Shift</option>
                    <option value="compressed">Compressed Schedule</option>
                    <option value="flexible">Flexible Schedule</option>
                  </select>
                </div>
                <div class="col-md-4 mb-3">
                  <label class="form-label" for="shiftStart">Shift Start</label>
                  <input id="shiftStart" v-model="form.shiftStart" type="time" class="form-control" :class="fieldClass('shiftStart')" required @input="handleFormMutation('shiftStart')">
                  <div class="invalid-feedback">{{ validationErrors.shiftStart }}</div>
                </div>
                <div class="col-md-4 mb-3">
                  <label class="form-label" for="shiftEnd">Shift End</label>
                  <input id="shiftEnd" v-model="form.shiftEnd" type="time" class="form-control" :class="fieldClass('shiftEnd')" required @input="handleFormMutation('shiftEnd')">
                  <div class="invalid-feedback">{{ validationErrors.shiftEnd }}</div>
                </div>
              </div>

              <div class="d-flex align-items-center justify-content-between mt-2 mb-3">
                <div>
                  <h6 class="mb-1">2. Time logs</h6>
                  <p class="text-muted mb-0 small">Clock in and clock out are paired so worked hours are easier to verify.</p>
                </div>
              </div>

              <div class="row">
                <div class="col-md-4 mb-3">
                  <label class="form-label" for="clockIn">Clock In</label>
                  <input id="clockIn" v-model="form.clockIn" type="time" class="form-control" :class="fieldClass('clockIn')" required @input="handleFormMutation('clockIn')">
                  <div class="invalid-feedback">{{ validationErrors.clockIn }}</div>
                </div>
                <div class="col-md-4 mb-3">
                  <label class="form-label" for="clockOut">Clock Out</label>
                  <input id="clockOut" v-model="form.clockOut" type="time" class="form-control" :class="fieldClass('clockOut')" required @input="handleFormMutation('clockOut')">
                  <div class="invalid-feedback">{{ validationErrors.clockOut }}</div>
                </div>
                <div class="col-md-4 mb-3">
                  <label class="form-label" for="source">Source / Device</label>
                  <select id="source" v-model="form.source" class="form-select" :class="fieldClass('source')" required @change="handleFormMutation('source')">
                    <option value="">Select source</option>
                    <option>Web</option>
                    <option>Mobile</option>
                    <option>Biometric</option>
                  </select>
                  <div class="invalid-feedback">{{ validationErrors.source }}</div>
                </div>
                <div class="col-md-4 mb-3">
                  <label class="form-label" for="breakOut">Break Out</label>
                  <input id="breakOut" v-model="form.breakOut" type="time" class="form-control">
                </div>
                <div class="col-md-4 mb-3">
                  <label class="form-label" for="breakIn">Break In</label>
                  <input id="breakIn" v-model="form.breakIn" type="time" class="form-control">
                </div>
                <div class="col-md-4 mb-3">
                  <label class="form-label" for="logAction">Entry Type</label>
                  <select id="logAction" v-model="form.logAction" class="form-select">
                    <option value="original">Original Log</option>
                    <option value="correction">Attendance Correction</option>
                  </select>
                </div>
              </div>

              <div class="row">
                <div class="col-md-6 mb-3">
                  <label class="form-label" for="restDayWork">Rest Day Work</label>
                  <select id="restDayWork" v-model="form.restDayWork" class="form-select">
                    <option value="no">No</option>
                    <option value="yes">Yes</option>
                  </select>
                </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label" for="holidayWork">Holiday Work</label>
                  <select id="holidayWork" v-model="form.holidayWork" class="form-select">
                    <option value="no">No</option>
                    <option value="yes">Yes</option>
                  </select>
                </div>
              </div>

              <div v-if="isCorrection" class="border rounded p-3 mb-3">
                <div class="d-flex align-items-center justify-content-between mb-3">
                  <div>
                    <h6 class="mb-1">Correction request</h6>
                    <p class="text-muted mb-0 small">Use this only for missing logs, wrong timestamps, or device issues.</p>
                  </div>
                  <span class="badge bg-light-warning text-warning">Pending</span>
                </div>
                <div class="row">
                  <div class="col-md-4 mb-3">
                    <label class="form-label" for="correctionType">Correction Type</label>
                    <select id="correctionType" v-model="form.correctionType" class="form-select" :class="fieldClass('correctionType')" @change="handleFormMutation('correctionType')">
                      <option value="">Select correction</option>
                      <option>Missing Clock In</option>
                      <option>Missing Clock Out</option>
                      <option>Wrong Time</option>
                      <option>Device Issue</option>
                    </select>
                    <div class="invalid-feedback">{{ validationErrors.correctionType }}</div>
                  </div>
                  <div class="col-md-8 mb-3">
                    <label class="form-label" for="adjustmentReason">Reason / Remarks</label>
                    <textarea id="adjustmentReason" v-model="form.adjustmentReason" class="form-control" :class="fieldClass('adjustmentReason')" rows="2" placeholder="Explain why this correction is needed." @input="handleFormMutation('adjustmentReason')"></textarea>
                    <div class="invalid-feedback">{{ validationErrors.adjustmentReason }}</div>
                  </div>
                </div>
              </div>

              <div class="d-flex flex-wrap gap-2 mt-2">
                <button type="button" class="btn btn-outline-primary" @click="saveDraft">Save Draft</button>
                <button type="submit" class="btn btn-primary">Save Attendance Log</button>
              </div>

              <div class="alert mt-3 mb-0" :class="alertState.class" role="alert">
                {{ alertState.message }}
              </div>
            </form>
          </div>
        </div>
      </div>

      <div class="col-lg-4">
        <div class="card h-100 border-0 shadow-sm">
          <div class="card-header bg-light-primary border-0">
            <h5 class="mb-0 text-primary">Attendance Summary</h5>
            <small class="text-muted">Read-only values calculated from the log.</small>
          </div>
          <div class="card-body">
            <div class="mb-3 p-3 rounded bg-light">
              <div class="d-flex justify-content-between align-items-center mb-2">
                <span class="text-muted">Log ID</span>
                <strong>{{ logIdDisplay }}</strong>
              </div>
              <div class="d-flex justify-content-between align-items-center mb-2">
                <span class="text-muted">Status</span>
                <span class="badge" :class="statusBadge.class">{{ statusBadge.label }}</span>
              </div>
              <div class="d-flex justify-content-between align-items-center mb-2">
                <span class="text-muted">Employee</span>
                <strong>{{ employeeSummary }}</strong>
              </div>
              <div class="d-flex justify-content-between align-items-center">
                <span class="text-muted">Schedule</span>
                <strong>{{ scheduleSummary }}</strong>
              </div>
            </div>

            <div class="row g-3">
              <div class="col-6">
                <div class="border rounded p-3 h-100">
                  <small class="text-muted d-block mb-1">Late</small>
                  <h4 class="mb-0 text-warning">{{ metrics.lateLabel }}</h4>
                </div>
              </div>
              <div class="col-6">
                <div class="border rounded p-3 h-100">
                  <small class="text-muted d-block mb-1">Undertime</small>
                  <h4 class="mb-0 text-danger">{{ metrics.undertimeLabel }}</h4>
                </div>
              </div>
              <div class="col-6">
                <div class="border rounded p-3 h-100">
                  <small class="text-muted d-block mb-1">Overtime</small>
                  <h4 class="mb-0 text-primary">{{ metrics.overtimeLabel }}</h4>
                </div>
              </div>
              <div class="col-6">
                <div class="border rounded p-3 h-100">
                  <small class="text-muted d-block mb-1">Night Diff</small>
                  <h4 class="mb-0 text-info">{{ metrics.nightDiffLabel }}</h4>
                </div>
              </div>
              <div class="col-6">
                <div class="border rounded p-3 h-100">
                  <small class="text-muted d-block mb-1">Worked Hours</small>
                  <h5 class="mb-0">{{ metrics.totalHours }}</h5>
                </div>
              </div>
              <div class="col-6">
                <div class="border rounded p-3 h-100">
                  <small class="text-muted d-block mb-1">Payable Hours</small>
                  <h5 class="mb-0 text-success">{{ metrics.payableHours }}</h5>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="col-lg-12">
        <div class="card">
          <div class="card-header d-flex flex-wrap gap-2 align-items-center justify-content-between">
            <div>
              <h5 class="mb-0">Recent Attendance Logs</h5>
              <small class="text-muted">Review live logs, premium work, and correction items in one list.</small>
            </div>
            <div class="d-flex flex-wrap align-items-center gap-2">
              <input v-model="attendanceSearch" type="search" class="form-control" placeholder="Search employee or log" style="min-width: 220px;">
              <span class="badge bg-light-secondary text-secondary">{{ attendanceCountLabel }}</span>
            </div>
          </div>
          <div class="card-body p-0">
            <div class="px-3 pt-3 d-flex flex-wrap gap-2">
              <button
                v-for="filter in attendanceFilters"
                :key="filter.value"
                type="button"
                class="btn btn-sm"
                :class="activeAttendanceFilter === filter.value ? 'btn-primary' : 'btn-outline-primary'"
                @click="activeAttendanceFilter = filter.value"
              >
                {{ filter.label }}
              </button>
            </div>
            <div class="table-responsive mt-3">
              <table class="table table-hover mb-0 align-middle">
                <thead class="table-light">
                  <tr>
                    <th>Log ID</th>
                    <th>Employee</th>
                    <th>Shift</th>
                    <th>Status</th>
                    <th>Late / OT</th>
                    <th>Payable</th>
                    <th>Source</th>
                    <th class="text-end">Action</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="row in filteredAttendanceRows" :key="row.logId">
                    <td>{{ row.logId }}</td>
                    <td>{{ row.employee }}</td>
                    <td>{{ row.shift }}</td>
                    <td><span class="badge" :class="row.statusClass">{{ row.statusLabel }}</span></td>
                    <td>{{ row.lateOt }}</td>
                    <td>{{ row.payable }}</td>
                    <td>{{ row.source }}</td>
                    <td class="text-end">
                      <a href="#" class="btn btn-sm btn-outline-primary" @click.prevent="loadAttendanceRecord(row)">View</a>
                    </td>
                  </tr>
                  <tr v-if="!filteredAttendanceRows.length">
                    <td colspan="8" class="text-center text-muted py-4">No attendance log matches the current search or filter.</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, reactive, ref, watch } from "vue";
import BreadcrumbBar from "@/components/BreadcrumbBar.vue";
import { ApiError, apiRequest } from "@/lib/api";
import { useAuthStore } from "@/stores/auth";

const authStore = useAuthStore();

const employeeData = ref({});
const employeeOptions = ref([]);

const shiftPresets = {
  regular: { start: "09:00", end: "18:00", label: "Regular Day Shift" },
  night: { start: "22:00", end: "06:00", label: "Night Shift" },
  compressed: { start: "08:00", end: "19:00", label: "Compressed Schedule" },
  flexible: { start: "10:00", end: "19:00", label: "Flexible Schedule" },
};

const attendanceRows = ref([]);

const attendanceFilters = [
  { value: "all", label: "All" },
  { value: "late", label: "Late" },
  { value: "correction", label: "Correction" },
  { value: "night", label: "Night Shift" },
  { value: "premium", label: "Premium Work" },
];

const alertState = reactive({
  class: "alert-light-primary border-primary",
  message: "Enter clock in and clock out to calculate late, undertime, overtime, night differential, and payable hours.",
});
const validationErrors = reactive({});

const form = reactive({
  employeeSelect: "",
  workDate: "",
  shiftSchedule: "regular",
  shiftStart: "09:00",
  shiftEnd: "18:00",
  clockIn: "",
  clockOut: "",
  source: "",
  breakOut: "",
  breakIn: "",
  logAction: "original",
  restDayWork: "no",
  holidayWork: "no",
  correctionType: "",
  adjustmentReason: "",
});

const attendanceSearch = ref("");
const activeAttendanceFilter = ref("all");
const logId = ref("Pending");
const lastSubmission = ref(null);

function setAlert(type, message) {
  alertState.class = `alert-light-${type} border-${type}`;
  alertState.message = message;
}

function clearValidationErrors() {
  Object.keys(validationErrors).forEach((key) => {
    delete validationErrors[key];
  });
}

function clearFieldError(fieldName) {
  if (fieldName && validationErrors[fieldName]) {
    delete validationErrors[fieldName];
  }
}

function fieldClass(fieldName) {
  return validationErrors[fieldName] ? "is-invalid" : "";
}

function handleFormMutation(fieldName = "") {
  clearFieldError(fieldName);
}

function toMinutes(timeValue) {
  if (!timeValue) return null;
  const parts = timeValue.split(":").map(Number);
  return parts[0] * 60 + parts[1];
}

function normalizeEnd(startMin, endMin) {
  if (startMin === null || endMin === null) return null;
  return endMin < startMin ? endMin + 24 * 60 : endMin;
}

function minutesToLabel(value) {
  return `${Math.max(0, Math.round(value || 0))} min`;
}

function minutesToHours(value) {
  return (Math.max(0, value || 0) / 60).toFixed(2);
}

function calculateNightDifferential(startMin, endMin) {
  if (startMin === null || endMin === null) return 0;
  let total = 0;
  for (let minute = startMin; minute < endMin; minute += 1) {
    const hour = Math.floor(minute / 60) % 24;
    if (hour >= 22 || hour < 6) total += 1;
  }
  return total;
}

function getBreakMinutes(clockInMin) {
  const breakOutMin = toMinutes(form.breakOut);
  const breakInMin = toMinutes(form.breakIn);
  if (breakOutMin === null && breakInMin === null) return 0;
  if (breakOutMin === null || breakInMin === null) return null;
  const normalizedBreakOut = breakOutMin < clockInMin ? breakOutMin + 24 * 60 : breakOutMin;
  const normalizedBreakIn = breakInMin < normalizedBreakOut ? breakInMin + 24 * 60 : breakInMin;
  return normalizedBreakIn - normalizedBreakOut;
}

function generateLogId() {
  const date = new Date();
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  const randomPart = Math.random().toString(36).slice(2, 6).toUpperCase();
  return `LOG-${year}${month}${day}-${randomPart}`;
}

function ensureLogId() {
  if (logId.value === "Pending") {
    logId.value = generateLogId();
  }
}

function applyShiftPreset() {
  const preset = shiftPresets[form.shiftSchedule];
  if (!preset) return;
  clearFieldError("shiftStart");
  clearFieldError("shiftEnd");
  form.shiftStart = preset.start;
  form.shiftEnd = preset.end;
}

function handleEmployeeChange() {
  clearFieldError("employeeSelect");
  if (!form.employeeSelect) {
    if (logId.value === "Pending") {
      return;
    }
  }
}

function validateForm() {
  clearValidationErrors();

  if (!form.employeeSelect) validationErrors.employeeSelect = "Employee is required.";
  if (!form.workDate) validationErrors.workDate = "Date is required.";
  if (!form.shiftStart) validationErrors.shiftStart = "Shift start is required.";
  if (!form.shiftEnd) validationErrors.shiftEnd = "Shift end is required.";
  if (!form.clockIn) validationErrors.clockIn = "Clock in is required.";
  if (!form.clockOut) validationErrors.clockOut = "Clock out is required.";
  if (!form.source) validationErrors.source = "Source is required.";

  if (isCorrection.value) {
    if (!form.correctionType) validationErrors.correctionType = "Correction type is required.";
    if (!form.adjustmentReason.trim()) validationErrors.adjustmentReason = "Reason is required.";
  }

  if (Object.keys(validationErrors).length) {
    setAlert("danger", "Please complete the highlighted required fields. Optional blank fields can be skipped.");
    return false;
  }

  return true;
}

const isCorrection = computed(() => form.logAction === "correction");

const employeeSummary = computed(() =>
  form.employeeSelect ? `${employeeData.value[form.employeeSelect] || "Unknown Employee"} (${form.employeeSelect})` : "No employee selected"
);

const scheduleSummary = computed(() => `${form.shiftStart || "--:--"} - ${form.shiftEnd || "--:--"}`);

const metrics = computed(() => {
  const shiftStartMin = toMinutes(form.shiftStart);
  const shiftEndMin = normalizeEnd(shiftStartMin, toMinutes(form.shiftEnd));
  const clockInMin = toMinutes(form.clockIn);
  const clockOutMinRaw = toMinutes(form.clockOut);
  const clockOutMin =
    clockInMin !== null && clockOutMinRaw !== null ? normalizeEnd(clockInMin, clockOutMinRaw) : null;
  const breakMinutes = clockInMin !== null ? getBreakMinutes(clockInMin) : 0;

  if (
    shiftStartMin === null ||
    shiftEndMin === null ||
    clockInMin === null ||
    clockOutMin === null ||
    breakMinutes === null ||
    breakMinutes < 0
  ) {
    return {
      valid: false,
      breakInvalid: breakMinutes === null || breakMinutes < 0,
      lateMinutes: 0,
      undertimeMinutes: 0,
      overtimeMinutes: 0,
      nightDiffMinutes: 0,
      workedMinutes: 0,
      payableMinutes: 0,
      lateLabel: "0 min",
      undertimeLabel: "0 min",
      overtimeLabel: "0 min",
      nightDiffLabel: "0 min",
      totalHours: "0.00",
      payableHours: "0.00",
      sameDayInvalid: false,
    };
  }

  const scheduledMinutes = Math.max(0, shiftEndMin - shiftStartMin);
  const workedMinutes = Math.max(0, clockOutMin - clockInMin - breakMinutes);
  const lateMinutes = clockInMin > shiftStartMin ? clockInMin - shiftStartMin : 0;
  const undertimeMinutes = clockOutMin < shiftEndMin ? shiftEndMin - clockOutMin : 0;
  const overtimeMinutes = clockOutMin > shiftEndMin ? clockOutMin - shiftEndMin : 0;
  const nightDiffMinutes = calculateNightDifferential(clockInMin, clockOutMin);
  const payableMinutes = Math.max(0, Math.min(workedMinutes, scheduledMinutes) + overtimeMinutes);
  const sameDayInvalid = clockOutMinRaw < clockInMin && shiftEndMin > shiftStartMin;

  return {
    valid: true,
    breakInvalid: false,
    lateMinutes,
    undertimeMinutes,
    overtimeMinutes,
    nightDiffMinutes,
    workedMinutes,
    payableMinutes,
    lateLabel: minutesToLabel(lateMinutes),
    undertimeLabel: minutesToLabel(undertimeMinutes),
    overtimeLabel: minutesToLabel(overtimeMinutes),
    nightDiffLabel: minutesToLabel(nightDiffMinutes),
    totalHours: minutesToHours(workedMinutes),
    payableHours: minutesToHours(payableMinutes),
    sameDayInvalid,
  };
});

const statusBadge = computed(() => {
  if (!metrics.value.valid) {
    return { label: isCorrection.value ? "Pending Correction" : "Draft", class: isCorrection.value ? "bg-light-warning text-warning" : "bg-light-primary text-primary" };
  }
  if (isCorrection.value) return { label: "Pending Correction", class: "bg-light-warning text-warning" };
  if (metrics.value.sameDayInvalid) return { label: "Invalid", class: "bg-light-danger text-danger" };
  if (
    lastSubmission.value &&
    lastSubmission.value.employeeId === form.employeeSelect &&
    lastSubmission.value.clockIn === form.clockIn &&
    lastSubmission.value.clockOut === form.clockOut &&
    lastSubmission.value.workDate === form.workDate
  ) {
    return { label: "Duplicate Check", class: "bg-light-warning text-warning" };
  }
  if (metrics.value.lateMinutes > 0) return { label: "Late", class: "bg-light-warning text-warning" };
  if (metrics.value.undertimeMinutes > 0) return { label: "Undertime", class: "bg-light-danger text-danger" };
  if (metrics.value.overtimeMinutes > 0 || form.restDayWork === "yes" || form.holidayWork === "yes") {
    return { label: "For Payroll Review", class: "bg-light-info text-info" };
  }
  if (metrics.value.nightDiffMinutes > 0) return { label: "Night Differential", class: "bg-light-info text-info" };
  return { label: "Present", class: "bg-light-success text-success" };
});

const adjustmentBadge = computed(() =>
  isCorrection.value
    ? { label: "Pending Correction", class: "bg-light-warning text-warning" }
    : { label: "Original", class: "bg-light-primary text-primary" }
);

const logIdDisplay = computed(() => logId.value);

const filteredAttendanceRows = computed(() => {
  const query = attendanceSearch.value.trim().toLowerCase();
  return attendanceRows.value.filter((row) => {
    const haystack = `${row.logId} ${row.employee} ${row.shift} ${row.statusLabel} ${row.source}`.toLowerCase();
    const searchPass = !query || haystack.includes(query);
    if (!searchPass) return false;
    if (activeAttendanceFilter.value === "all") return true;
    if (activeAttendanceFilter.value === "late") return row.status === "late";
    if (activeAttendanceFilter.value === "correction") return row.status === "correction";
    if (activeAttendanceFilter.value === "night") return row.shiftFilter === "night";
    if (activeAttendanceFilter.value === "premium") return row.premium === "yes";
    return true;
  });
});

const attendanceCountLabel = computed(() => {
  const count = filteredAttendanceRows.value.length;
  return `${count} record${count === 1 ? "" : "s"}`;
});

const overview = computed(() => ({
  presentCount: attendanceRows.value.filter((row) => row.status === "present").length,
  lateCount: attendanceRows.value.filter((row) => row.status === "late").length,
  correctionCount: attendanceRows.value.filter((row) => row.status === "correction").length,
  premiumCount: attendanceRows.value.filter((row) => row.premium === "yes").length,
}));

function syncAlertFromMetrics() {
  if (!metrics.value.valid) {
    if (metrics.value.breakInvalid) {
      setAlert("danger", "Break Out and Break In must be completed together in the correct order.");
    } else {
      setAlert("primary", "Enter clock in and clock out to calculate late, undertime, overtime, night differential, and payable hours.");
    }
    return;
  }

  if (isCorrection.value) {
    setAlert("warning", "Correction request will need supervisor approval before payroll can use it.");
    return;
  }

  if (metrics.value.sameDayInvalid) {
    setAlert("danger", "Clock Out cannot be earlier than Clock In for a same-day shift.");
    return;
  }

  if (
    lastSubmission.value &&
    lastSubmission.value.employeeId === form.employeeSelect &&
    lastSubmission.value.clockIn === form.clockIn &&
    lastSubmission.value.clockOut === form.clockOut &&
    lastSubmission.value.workDate === form.workDate
  ) {
    setAlert("warning", "This submission looks like a duplicate inside the same minute. Review before saving.");
    return;
  }

  if (metrics.value.lateMinutes > 0) {
    setAlert("warning", `Late arrival detected. ${metrics.value.lateLabel} will affect payable hours.`);
    return;
  }

  if (metrics.value.undertimeMinutes > 0) {
    setAlert("warning", `Undertime detected. ${metrics.value.undertimeLabel} will reduce payable hours.`);
    return;
  }

  if (metrics.value.overtimeMinutes > 0 || form.restDayWork === "yes" || form.holidayWork === "yes") {
    setAlert("info", "Premium work detected. Overtime, rest day, or holiday tags are ready for payroll review.");
    return;
  }

  if (metrics.value.nightDiffMinutes > 0) {
    setAlert("info", "Night differential detected for work inside the 10:00 PM to 6:00 AM window.");
    return;
  }

  setAlert("success", "Attendance log looks valid and ready for payroll reconciliation.");
}

function saveDraft() {
  syncAlertFromMetrics();
  setAlert("primary", "Attendance draft saved locally.");
}

function buildAttendancePayload(statusLabel) {
  return {
    log_id: logId.value,
    employee_code: form.employeeSelect,
    employee_name: employeeData.value[form.employeeSelect] || "Unknown Employee",
    work_date: form.workDate,
    shift_schedule: form.shiftSchedule,
    shift_start: form.shiftStart,
    shift_end: form.shiftEnd,
    clock_in: form.clockIn,
    clock_out: form.clockOut,
    source: form.source,
    break_out: form.breakOut || null,
    break_in: form.breakIn || null,
    log_action: form.logAction,
    rest_day_work: form.restDayWork,
    holiday_work: form.holidayWork,
    correction_type: form.correctionType || null,
    adjustment_reason: form.adjustmentReason.trim() || null,
    status: statusLabel,
    payable_hours: Number(metrics.value.payableHours || 0),
    notes: `${shiftPresets[form.shiftSchedule]?.label || form.shiftSchedule} via ${form.source}`,
  };
}

function normalizeAttendanceRow(log) {
  const status = String(log.status || "saved").toLowerCase();
  return {
    logId: log.log_id,
    employeeId: log.employee_code,
    employee: log.employee_name,
    shift: shiftPresets[log.shift_schedule]?.label || log.shift_schedule || "Shift",
    status,
    shiftFilter: log.shift_schedule === "night" ? "night" : "day",
    premium: log.rest_day_work === "yes" || log.holiday_work === "yes" ? "yes" : "no",
    statusLabel: log.status || "Saved",
    statusClass:
      status.includes("late")
        ? "bg-light-warning text-warning"
        : status.includes("correction")
          ? "bg-light-info text-info"
          : status.includes("present") || status.includes("saved")
            ? "bg-light-success text-success"
            : "bg-light-primary text-primary",
    lateOt: "-",
    payable: `${Number(log.payable_hours || 0).toFixed(2)} hrs`,
    source: log.source,
    raw: log,
  };
}

async function fetchEmployees() {
  if (!authStore.accessToken) return;

  try {
    const response = await apiRequest("/employees", {
      token: authStore.accessToken,
    });
    employeeOptions.value = response.items.map((employee) => ({
      employee_code: employee.employee_code,
      name: `${employee.first_name} ${employee.last_name}`,
    }));
    employeeData.value = Object.fromEntries(
      employeeOptions.value.map((employee) => [employee.employee_code, employee.name])
    );
  } catch {
    employeeOptions.value = [];
    employeeData.value = {};
  }
}

async function fetchAttendanceLogs() {
  if (!authStore.accessToken) return;

  try {
    const response = await apiRequest("/attendance", {
      token: authStore.accessToken,
    });
    attendanceRows.value = response.items.map(normalizeAttendanceRow);
  } catch {
    attendanceRows.value = [];
  }
}

async function saveAttendanceToApi(payload) {
  try {
    return await apiRequest("/attendance", {
      method: "POST",
      token: authStore.accessToken,
      body: JSON.stringify(payload),
    });
  } catch (error) {
    if (error instanceof ApiError && error.status === 409) {
      const { log_id: _logId, ...updatePayload } = payload;
      return apiRequest(`/attendance/${encodeURIComponent(payload.log_id)}`, {
        method: "PUT",
        token: authStore.accessToken,
        body: JSON.stringify(updatePayload),
      });
    }

    throw error;
  }
}

async function handleSubmit() {
  syncAlertFromMetrics();

  if (!validateForm()) {
    return;
  }

  ensureLogId();
  lastSubmission.value = {
    employeeId: form.employeeSelect,
    clockIn: form.clockIn,
    clockOut: form.clockOut,
    workDate: form.workDate,
  };

  const statusLabel = isCorrection.value ? "Pending Correction" : statusBadge.value.label;

  try {
    await saveAttendanceToApi(buildAttendancePayload(statusLabel));
    await fetchAttendanceLogs();
    if (isCorrection.value) {
      setAlert("warning", `${logId.value.trim()} submitted for supervisor approval.`);
      return;
    }

    setAlert("success", `${logId.value.trim()} saved to the HRIS API. Payroll can reconcile the record against the shift schedule.`);
  } catch (error) {
    if (error instanceof ApiError && error.status === 401) {
      setAlert("danger", "Your session expired. Please sign in again.");
      authStore.logout();
    } else {
      setAlert("danger", "Could not save the attendance log to the API. Please make sure FastAPI is running.");
    }
  }
}

function loadAttendanceRecord(row) {
  clearValidationErrors();
  const record = row.raw;
  if (!record) return;

  form.employeeSelect = record.employee_code;
  form.workDate = record.work_date;
  form.source = record.source;
  form.logAction = record.log_action || "original";
  form.restDayWork = record.rest_day_work || "no";
  form.holidayWork = record.holiday_work || "no";
  form.shiftSchedule = record.shift_schedule || "regular";
  form.shiftStart = record.shift_start;
  form.shiftEnd = record.shift_end;
  form.clockIn = record.clock_in;
  form.clockOut = record.clock_out;
  form.breakOut = record.break_out || "";
  form.breakIn = record.break_in || "";
  form.correctionType = record.correction_type || "";
  form.adjustmentReason = record.adjustment_reason || "";
  logId.value = record.log_id;
  syncAlertFromMetrics();
  setAlert("info", `${record.log_id} loaded into the attendance form.`);
}

watch(
  () => form.logAction,
  (value) => {
    if (value !== "correction") {
      clearFieldError("correctionType");
      clearFieldError("adjustmentReason");
      form.correctionType = "";
      form.adjustmentReason = "";
    }
    syncAlertFromMetrics();
  }
);

watch(
  () => [
    form.employeeSelect,
    form.workDate,
    form.shiftSchedule,
    form.shiftStart,
    form.shiftEnd,
    form.clockIn,
    form.clockOut,
    form.source,
    form.breakOut,
    form.breakIn,
    form.restDayWork,
    form.holidayWork,
    form.correctionType,
    form.adjustmentReason,
  ],
  () => {
    syncAlertFromMetrics();
  },
  { deep: true }
);

syncAlertFromMetrics();

onMounted(() => {
  fetchEmployees();
  fetchAttendanceLogs();
});
</script>
