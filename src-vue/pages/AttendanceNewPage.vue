<template>
  <div>
    <BreadcrumbBar section="HR Modules / Time & Attendance" :current="pageTitle" />

    <div class="row g-3">
      <div class="col-12">
        <div class="card h-100 border-0 shadow-sm premium-panel">
          <div class="card-header d-flex align-items-center justify-content-between bg-white border-bottom-0 pt-4 pb-0 premium-panel-header">
            <div class="d-flex align-items-center gap-3">
              <button
                class="btn btn-sm btn-outline-secondary d-flex align-items-center justify-content-center premium-back"
                @click="goBack"
                title="Back to Attendance"
              >
                <i class="ti ti-arrow-left"></i>
              </button>
              <div>
                <h5 class="mb-0">{{ pageTitle }}</h5>
                <small class="text-muted">{{ pageSubtitle }}</small>
              </div>
            </div>
          </div>

          <div class="card-body premium-panel-body">
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
                  <EmployeeSearchSelect
                    v-model="form.employeeSelect"
                    input-id="employeeSelect"
                    :options="employeeOptions"
                    input-class="premium-input"
                    :invalid="Boolean(validationErrors.employeeSelect)"
                    placeholder="Type name or employee code"
                    :disabled="isEditMode"
                    required
                    @change="handleEmployeeChange"
                  />
                  <div class="invalid-feedback">{{ validationErrors.employeeSelect }}</div>
                </div>
                <div class="col-md-3 mb-3">
                  <label class="form-label" for="employeeId">Employee ID</label>
                  <input id="employeeId" :value="form.employeeSelect" type="text" class="form-control premium-input" placeholder="Auto-filled" readonly />
                </div>
                <div class="col-md-3 mb-3">
                  <label class="form-label" for="workDate">Date</label>
                  <input
                    id="workDate"
                    v-model="form.workDate"
                    type="date"
                    class="form-control premium-input"
                    :class="fieldClass('workDate')"
                    :disabled="isEditMode"
                    required
                    @input="handleWorkDateChange"
                  />
                  <div class="invalid-feedback">{{ validationErrors.workDate }}</div>
                </div>

                <div class="col-md-3 mb-3">
                  <label class="form-label" for="shiftSchedule">Shift Schedule</label>
                  <select id="shiftSchedule" v-model="form.shiftSchedule" class="form-select premium-input" @change="applyShiftPreset">
                    <option value="regular">Regular Day Shift</option>
                    <option value="night">Night Shift</option>
                    <option value="compressed">Compressed Schedule</option>
                    <option value="flexible">Flexible Schedule</option>
                  </select>
                </div>
                <div class="col-md-3 mb-3">
                  <label class="form-label" for="shiftStart">Shift Start</label>
                  <input id="shiftStart" v-model="form.shiftStart" type="time" class="form-control premium-input" :class="fieldClass('shiftStart')" required @input="handleFormMutation('shiftStart')" />
                  <div class="invalid-feedback">{{ validationErrors.shiftStart }}</div>
                </div>
                <div class="col-md-3 mb-3">
                  <label class="form-label" for="shiftEnd">Shift End</label>
                  <input id="shiftEnd" v-model="form.shiftEnd" type="time" class="form-control premium-input" :class="fieldClass('shiftEnd')" required @input="handleFormMutation('shiftEnd')" />
                  <div class="invalid-feedback">{{ validationErrors.shiftEnd }}</div>
                </div>
                <div class="col-md-3 mb-3">
                  <label class="form-label" for="graceMinutes">Late Grace (minutes)</label>
                  <input id="graceMinutes" v-model.number="form.graceMinutes" type="number" min="0" max="120" class="form-control premium-input" :class="fieldClass('graceMinutes')" @input="handleFormMutation('graceMinutes')" />
                  <div class="invalid-feedback">{{ validationErrors.graceMinutes }}</div>
                </div>
              </div>

              <div class="d-flex align-items-center justify-content-between mt-2 mb-3">
                <div>
                  <h6 class="mb-1">2. Time logs</h6>
                  <p class="text-muted mb-0 small">Clock in and clock out are paired so worked hours are easier to verify.</p>
                </div>
              </div>

              <div class="row">
                <div class="col-md-6 mb-3">
                  <label class="form-label" for="clockIn">Clock In <span class="text-muted">(optional)</span></label>
                  <input id="clockIn" v-model="form.clockIn" type="time" class="form-control premium-input" :class="fieldClass('clockIn')" @input="handleFormMutation('clockIn')" />
                  <div class="invalid-feedback">{{ validationErrors.clockIn }}</div>
                </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label" for="clockOut">Clock Out <span class="text-muted">(optional)</span></label>
                  <input id="clockOut" v-model="form.clockOut" type="time" class="form-control premium-input" :class="fieldClass('clockOut')" @input="handleFormMutation('clockOut')" />
                  <div class="invalid-feedback">{{ validationErrors.clockOut }}</div>
                </div>

                <div class="col-md-4 mb-3">
                  <label class="form-label" for="breakOut">Break Out</label>
                  <input id="breakOut" v-model="form.breakOut" type="time" class="form-control premium-input" />
                </div>
                <div class="col-md-4 mb-3">
                  <label class="form-label" for="breakIn">Break In</label>
                  <input id="breakIn" v-model="form.breakIn" type="time" class="form-control premium-input" />
                </div>
                <div class="col-md-4 mb-3">
                  <label class="form-label" for="logAction">Entry Type</label>
                  <select id="logAction" v-model="form.logAction" class="form-select premium-input">
                    <option value="original">Original Log</option>
                    <option value="correction">Attendance Correction</option>
                  </select>
                </div>
              </div>

              <div class="row">
                <div class="col-md-6 mb-3">
                  <label class="form-label" for="restDayWork">Rest Day Work</label>
                  <select id="restDayWork" v-model="form.restDayWork" class="form-select premium-input">
                    <option value="no">No</option>
                    <option value="yes">Yes</option>
                  </select>
                </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label" for="holidayWork">Holiday Work</label>
                  <select id="holidayWork" v-model="form.holidayWork" class="form-select premium-input">
                    <option value="no">No</option>
                    <option value="yes">Yes</option>
                  </select>
                </div>
              </div>

              <div v-if="isCorrection" class="premium-correction mb-3">
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
                    <select id="correctionType" v-model="form.correctionType" class="form-select premium-input" :class="fieldClass('correctionType')" @change="handleFormMutation('correctionType')">
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
                    <textarea
                      id="adjustmentReason"
                      v-model="form.adjustmentReason"
                      class="form-control premium-input"
                      :class="fieldClass('adjustmentReason')"
                      rows="2"
                      placeholder="Explain why this correction is needed."
                      @input="handleFormMutation('adjustmentReason')"
                    ></textarea>
                    <div class="invalid-feedback">{{ validationErrors.adjustmentReason }}</div>
                  </div>
                </div>
              </div>

              <div class="d-flex flex-wrap gap-2 mt-2">
                <button type="button" class="btn btn-outline-primary premium-action" @click="saveDraft">Save Draft</button>
                <button type="submit" class="btn btn-primary">{{ submitButtonLabel }}</button>
              </div>

              <div class="alert mt-3 mb-0" :class="alertState.class" role="alert">{{ alertState.message }}</div>
            </form>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, reactive, ref, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import BreadcrumbBar from "@/components/BreadcrumbBar.vue";
import EmployeeSearchSelect from "@/components/EmployeeSearchSelect.vue";
import { ApiError, apiRequest } from "@/lib/api";
import { useAuthStore } from "@/stores/auth";

const authStore = useAuthStore();
const route = useRoute();
const router = useRouter();

const employeeData = ref({});
const employeeOptions = ref([]);

const shiftPresets = {
  regular: { start: "09:00", end: "18:00", label: "Regular Day Shift" },
  night: { start: "22:00", end: "06:00", label: "Night Shift" },
  compressed: { start: "08:00", end: "19:00", label: "Compressed Schedule" },
  flexible: { start: "10:00", end: "19:00", label: "Flexible Schedule" },
};

const alertState = reactive({
  class: "alert-light-primary border-primary",
  message:
    "Enter clock in and clock out to calculate late, undertime, overtime, night differential, and payable hours.",
});
const validationErrors = reactive({});

const form = reactive({
  employeeSelect: "",
  workDate: "",
  shiftSchedule: "regular",
  shiftStart: "09:00",
  shiftEnd: "18:00",
  graceMinutes: 0,
  clockIn: "",
  clockOut: "",
  breakOut: "",
  breakIn: "",
  logAction: "original",
  restDayWork: "no",
  holidayWork: "no",
  correctionType: "",
  adjustmentReason: "",
});

const logId = ref("Pending");
const existingLogId = ref("");
const duplicateCheck = reactive({
  isDuplicate: false,
  matchedLogId: "",
  isChecking: false,
});
let duplicateCheckRequestId = 0;

const isEditMode = computed(() => Boolean(String(route.params.logId || "").trim()));
const pageTitle = computed(() => (isEditMode.value ? "Edit Attendance" : "New Attendance"));
const pageSubtitle = computed(() =>
  isEditMode.value
    ? "Review and update the selected attendance log."
    : "Record shift logs and corrections for payroll reconciliation."
);
const submitButtonLabel = computed(() => (isEditMode.value ? "Update Attendance Log" : "Save Attendance Log"));

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
  const selectedEmployee = employeeData.value[form.employeeSelect];
  if (!selectedEmployee) return;
  form.shiftSchedule = selectedEmployee.workSchedule || "regular";
  form.shiftStart = selectedEmployee.defaultShiftStart || "09:00";
  form.shiftEnd = selectedEmployee.defaultShiftEnd || "18:00";
  form.graceMinutes = Number(selectedEmployee.defaultGraceMinutes || 0);
  syncRestDayFromSchedule();
}

function getDateWorkDay(dateValue) {
  if (!dateValue) return "";
  const date = new Date(`${dateValue}T00:00:00`);
  if (Number.isNaN(date.getTime())) return "";
  return ["sun", "mon", "tue", "wed", "thu", "fri", "sat"][date.getDay()];
}

function syncRestDayFromSchedule() {
  const selectedEmployee = employeeData.value[form.employeeSelect];
  const workDay = getDateWorkDay(form.workDate);
  if (!selectedEmployee || !workDay) return;
  form.restDayWork = selectedEmployee.workDays.includes(workDay) ? "no" : "yes";
}

function handleWorkDateChange() {
  handleFormMutation("workDate");
  syncRestDayFromSchedule();
}

function validateForm() {
  clearValidationErrors();

  if (!form.employeeSelect) validationErrors.employeeSelect = "Employee is required.";
  if (!form.workDate) validationErrors.workDate = "Date is required.";
  if (!form.shiftStart) validationErrors.shiftStart = "Shift start is required.";
  if (!form.shiftEnd) validationErrors.shiftEnd = "Shift end is required.";
  if (!Number.isInteger(form.graceMinutes) || form.graceMinutes < 0 || form.graceMinutes > 120) {
    validationErrors.graceMinutes = "Grace period must be from 0 to 120 minutes.";
  }
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

const metrics = computed(() => {
  const shiftStartMin = toMinutes(form.shiftStart);
  const shiftEndMin = normalizeEnd(shiftStartMin, toMinutes(form.shiftEnd));
  const clockInMin = toMinutes(form.clockIn);
  const clockOutMinRaw = toMinutes(form.clockOut);
  const clockOutMin =
    clockInMin !== null && clockOutMinRaw !== null ? normalizeEnd(clockInMin, clockOutMinRaw) : null;
  const breakMinutes = clockInMin !== null ? getBreakMinutes(clockInMin) : 0;
  const incomplete = clockInMin === null || clockOutMin === null;

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
      incomplete,
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
  const lateMinutes = clockInMin > shiftStartMin + form.graceMinutes ? clockInMin - shiftStartMin - form.graceMinutes : 0;
  const undertimeMinutes = clockOutMin < shiftEndMin ? shiftEndMin - clockOutMin : 0;
  const overtimeMinutes = clockOutMin > shiftEndMin ? clockOutMin - shiftEndMin : 0;
  const nightDiffMinutes = calculateNightDifferential(clockInMin, clockOutMin);
  const payableMinutes = Math.max(0, Math.min(workedMinutes, scheduledMinutes));
  const sameDayInvalid = clockOutMinRaw < clockInMin && shiftEndMin > shiftStartMin;

  return {
    valid: true,
    incomplete: false,
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

function deriveAttendanceStatus() {
  if (!metrics.value.valid) {
    if (metrics.value.incomplete && !metrics.value.breakInvalid) {
      return { label: "Incomplete", class: "bg-light-danger text-danger" };
    }
    return {
      label: isCorrection.value ? "Correction" : "Draft",
      class: isCorrection.value ? "bg-light-warning text-warning" : "bg-light-primary text-primary",
    };
  }
  if (isCorrection.value) return { label: "Correction", class: "bg-light-warning text-warning" };
  if (metrics.value.sameDayInvalid) return { label: "Invalid", class: "bg-light-danger text-danger" };

  if (duplicateCheck.isDuplicate) {
    return { label: "Duplicate Check", class: "bg-light-warning text-warning" };
  }

  if (metrics.value.lateMinutes > 0 && metrics.value.undertimeMinutes > 0) {
    return { label: "Late / Undertime", class: "bg-light-danger text-danger" };
  }

  if (metrics.value.lateMinutes > 0) return { label: "Late", class: "bg-light-warning text-warning" };
  if (metrics.value.undertimeMinutes > 0) return { label: "Undertime", class: "bg-light-danger text-danger" };
  return { label: "Present", class: "bg-light-success text-success" };
}

const statusBadge = computed(() => deriveAttendanceStatus());

function buildAttendanceAlert() {
  if (!metrics.value.valid) {
    if (metrics.value.incomplete && !metrics.value.breakInvalid) {
      return {
        type: "warning",
        message: "A missing clock in or clock out will be saved as incomplete attendance.",
      };
    }
    if (metrics.value.breakInvalid) {
      return {
        type: "danger",
        message: "Break Out and Break In must be completed together in the correct order.",
      };
    }

    return {
      type: "primary",
      message: "Enter clock in and clock out to calculate late, undertime, overtime, night differential, and payable hours.",
    };
  }

  if (isCorrection.value) {
    return {
      type: "warning",
      message: "This record is marked as a correction. Review the details before finalizing attendance.",
    };
  }

  if (metrics.value.sameDayInvalid) {
    return {
      type: "danger",
      message: "Clock Out cannot be earlier than Clock In for a same-day shift.",
    };
  }

  if (duplicateCheck.isDuplicate) {
    return {
      type: "warning",
      message: `A matching attendance log already exists${duplicateCheck.matchedLogId ? ` (${duplicateCheck.matchedLogId})` : ""}. Review before saving.`,
    };
  }

  if (metrics.value.lateMinutes > 0 && metrics.value.undertimeMinutes > 0) {
    return {
      type: "warning",
      message: `Late arrival and undertime detected. ${metrics.value.lateLabel} late and ${metrics.value.undertimeLabel} undertime will affect payable hours.`,
    };
  }

  if (metrics.value.lateMinutes > 0) {
    return {
      type: "warning",
      message: `Late arrival detected. ${metrics.value.lateLabel} will affect payable hours.`,
    };
  }

  if (metrics.value.undertimeMinutes > 0) {
    return {
      type: "warning",
      message: `Undertime detected. ${metrics.value.undertimeLabel} will reduce payable hours.`,
    };
  }

  return {
    type: "success",
    message: "Attendance log looks valid and will be recorded as present.",
  };
}

function syncAlertFromMetrics() {
  const attendanceAlert = buildAttendanceAlert();
  setAlert(attendanceAlert.type, attendanceAlert.message);
}

function saveDraft() {
  syncAlertFromMetrics();
  setAlert("primary", "Attendance draft saved locally.");
}

function goBack() {
  router.push("/attendance");
}

function applyAttendanceRecord(record) {
  existingLogId.value = record.log_id || "";
  logId.value = record.log_id || "Pending";
  form.employeeSelect = record.employee_code || "";
  form.workDate = record.work_date || "";
  form.shiftSchedule = record.shift_schedule || "regular";
  form.shiftStart = record.shift_start || "09:00";
  form.shiftEnd = record.shift_end || "18:00";
  form.graceMinutes = Number(record.grace_minutes || 0);
  form.clockIn = record.clock_in || "";
  form.clockOut = record.clock_out || "";
  form.breakOut = record.break_out || "";
  form.breakIn = record.break_in || "";
  form.logAction = record.log_action || "original";
  form.restDayWork = record.rest_day_work || "no";
  form.holidayWork = record.holiday_work || "no";
  form.correctionType = record.correction_type || "";
  form.adjustmentReason = record.adjustment_reason || "";
}

function buildAttendancePayload(statusLabel) {
  return {
    log_id: logId.value,
    employee_code: form.employeeSelect,
    employee_name: employeeData.value[form.employeeSelect]?.name || "Unknown Employee",
    work_date: form.workDate,
    shift_schedule: form.shiftSchedule,
    shift_start: form.shiftStart,
    shift_end: form.shiftEnd,
    grace_minutes: form.graceMinutes,
    clock_in: form.clockIn,
    clock_out: form.clockOut,
    source: "HRIS",
    break_out: form.breakOut || null,
    break_in: form.breakIn || null,
    log_action: form.logAction,
    rest_day_work: form.restDayWork,
    holiday_work: form.holidayWork,
    correction_type: form.correctionType || null,
    adjustment_reason: form.adjustmentReason.trim() || null,
    status: statusLabel,
    payable_hours: Number(metrics.value.payableHours || 0),
    notes: shiftPresets[form.shiftSchedule]?.label || form.shiftSchedule,
  };
}

async function saveAttendanceToApi(payload) {
  if (isEditMode.value && existingLogId.value) {
    const { log_id: _logId, ...updatePayload } = payload;
    return apiRequest(`/attendance/${encodeURIComponent(existingLogId.value)}`, {
      method: "PUT",
      token: authStore.accessToken,
      body: JSON.stringify(updatePayload),
    });
  }

  return apiRequest("/attendance", {
    method: "POST",
    token: authStore.accessToken,
    body: JSON.stringify(payload),
  });
}

async function checkDuplicateAttendance() {
  const hasRequiredFields = form.employeeSelect && form.workDate;
  const canCheck =
    hasRequiredFields &&
    Boolean(authStore.accessToken);

  duplicateCheckRequestId += 1;
  const requestId = duplicateCheckRequestId;

  if (!canCheck) {
    duplicateCheck.isDuplicate = false;
    duplicateCheck.matchedLogId = "";
    duplicateCheck.isChecking = false;
    return;
  }

  duplicateCheck.isChecking = true;

  try {
    const response = await apiRequest(
      `/attendance/duplicate-check?employee_code=${encodeURIComponent(form.employeeSelect)}&work_date=${encodeURIComponent(form.workDate)}&log_action=${encodeURIComponent(form.logAction)}${existingLogId.value ? `&exclude_log_id=${encodeURIComponent(existingLogId.value)}` : ""}`,
      {
        token: authStore.accessToken,
      }
    );

    if (requestId !== duplicateCheckRequestId) return;

    duplicateCheck.isDuplicate = Boolean(response.is_duplicate);
    duplicateCheck.matchedLogId = response.matched_log_id || "";
  } catch {
    if (requestId !== duplicateCheckRequestId) return;

    duplicateCheck.isDuplicate = false;
    duplicateCheck.matchedLogId = "";
  } finally {
    if (requestId === duplicateCheckRequestId) {
      duplicateCheck.isChecking = false;
    }
  }
}

async function handleSubmit() {
  syncAlertFromMetrics();

  if (!validateForm()) {
    return;
  }

  await checkDuplicateAttendance();
  syncAlertFromMetrics();
  if (duplicateCheck.isDuplicate && !isCorrection.value) {
    setAlert(
      "danger",
      `Attendance already exists for this employee on ${form.workDate}${duplicateCheck.matchedLogId ? ` (${duplicateCheck.matchedLogId})` : ""}.`
    );
    return;
  }
  ensureLogId();
  const statusLabel = isCorrection.value ? "Correction" : statusBadge.value.label;

  try {
    const savedRecord = await saveAttendanceToApi(buildAttendancePayload(statusLabel));
    if (isCorrection.value) {
      setAlert(
        "warning",
        `${(existingLogId.value || logId.value).trim()} ${isEditMode.value ? "updated as" : "saved as"} a corrected ${String(savedRecord.status || "attendance").toLowerCase()} record.`
      );
      return;
    }

    setAlert(
      "success",
      `${(existingLogId.value || logId.value).trim()} ${isEditMode.value ? "updated" : "saved"} as ${savedRecord.status}. Payable hours: ${Number(savedRecord.payable_hours || 0).toFixed(2)}.`
    );
  } catch (error) {
    if (error instanceof ApiError && error.status === 401) {
      setAlert("danger", "Your session expired. Please sign in again.");
      authStore.logout();
    } else if (error instanceof ApiError && error.status === 422) {
      setAlert("danger", error.message);
    } else {
      setAlert("danger", "Could not save the attendance log to the API. Please make sure FastAPI is running.");
    }
  }
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
      response.items.map((employee) => [
        employee.employee_code,
        {
          name: `${employee.first_name} ${employee.last_name}`,
          workSchedule: employee.work_schedule || "regular",
          workDays: String(employee.work_days || "mon,tue,wed,thu,fri").split(",").filter(Boolean),
          defaultShiftStart: employee.default_shift_start || "09:00",
          defaultShiftEnd: employee.default_shift_end || "18:00",
          defaultGraceMinutes: Number(employee.default_grace_minutes || 0),
        },
      ])
    );
  } catch {
    employeeOptions.value = [];
    employeeData.value = {};
  }
}

async function fetchAttendanceRecord() {
  const targetLogId = String(route.params.logId || "").trim();
  if (!targetLogId || !authStore.accessToken) return;

  try {
    const record = await apiRequest(`/attendance/record/${encodeURIComponent(targetLogId)}`, {
      token: authStore.accessToken,
    });
    applyAttendanceRecord(record);
  } catch (error) {
    if (error instanceof ApiError && error.status === 401) {
      authStore.logout();
      return;
    }
    setAlert("danger", "Could not load the attendance log for editing.");
  }
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
    form.graceMinutes,
    form.clockIn,
    form.clockOut,
    form.breakOut,
    form.breakIn,
    form.restDayWork,
    form.holidayWork,
    form.correctionType,
    form.adjustmentReason,
  ],
  async () => {
    await checkDuplicateAttendance();
    syncAlertFromMetrics();
  },
  { deep: true }
);

syncAlertFromMetrics();

onMounted(async () => {
  await fetchEmployees();
  await fetchAttendanceRecord();
});
</script>

<style scoped>
.premium-panel {
  border-radius: 1.35rem;
  border: 1px solid rgba(16, 24, 40, 0.06);
  overflow: hidden;
}

.premium-panel-header {
  padding-bottom: 1rem;
}

.premium-panel-body {
  background:
    radial-gradient(circle at top left, rgba(13, 110, 253, 0.05), transparent 35%),
    #fff;
}

.premium-back {
  width: 38px;
  height: 38px;
  padding: 0;
  border-color: rgba(148, 163, 184, 0.22);
  border-radius: 0.85rem;
}

.premium-input {
  border-color: rgba(148, 163, 184, 0.22);
}

.premium-input:focus {
  box-shadow: none;
  border-color: #0d6efd;
}

.premium-correction {
  border: 1px solid rgba(148, 163, 184, 0.16);
  border-radius: 1rem;
  padding: 1rem;
  background: linear-gradient(180deg, #fff 0%, #fbfdff 100%);
}

.premium-action {
  border-color: rgba(13, 110, 253, 0.22);
}

@media (max-width: 767.98px) {
  .premium-panel-header {
    padding-top: 1.1rem !important;
  }
}
</style>
