<template>
  <div>
    <BreadcrumbBar section="HR Modules / Time & Attendance" current="New Attendance" />

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
                <h5 class="mb-0">Attendance Entry</h5>
                <small class="text-muted">Record shift logs and corrections for payroll reconciliation.</small>
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
                  <select
                    id="employeeSelect"
                    v-model="form.employeeSelect"
                    class="form-select premium-input"
                    :class="fieldClass('employeeSelect')"
                    required
                    @change="handleEmployeeChange"
                  >
                    <option value="">Select employee</option>
                    <option v-for="employee in employeeOptions" :key="employee.employee_code" :value="employee.employee_code">
                      {{ employee.employee_code }} - {{ employee.name }}
                    </option>
                  </select>
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
                    required
                    @input="handleFormMutation('workDate')"
                  />
                  <div class="invalid-feedback">{{ validationErrors.workDate }}</div>
                </div>

                <div class="col-md-4 mb-3">
                  <label class="form-label" for="shiftSchedule">Shift Schedule</label>
                  <select id="shiftSchedule" v-model="form.shiftSchedule" class="form-select premium-input" @change="applyShiftPreset">
                    <option value="regular">Regular Day Shift</option>
                    <option value="night">Night Shift</option>
                    <option value="compressed">Compressed Schedule</option>
                    <option value="flexible">Flexible Schedule</option>
                  </select>
                </div>
                <div class="col-md-4 mb-3">
                  <label class="form-label" for="shiftStart">Shift Start</label>
                  <input id="shiftStart" v-model="form.shiftStart" type="time" class="form-control premium-input" :class="fieldClass('shiftStart')" required @input="handleFormMutation('shiftStart')" />
                  <div class="invalid-feedback">{{ validationErrors.shiftStart }}</div>
                </div>
                <div class="col-md-4 mb-3">
                  <label class="form-label" for="shiftEnd">Shift End</label>
                  <input id="shiftEnd" v-model="form.shiftEnd" type="time" class="form-control premium-input" :class="fieldClass('shiftEnd')" required @input="handleFormMutation('shiftEnd')" />
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
                  <input id="clockIn" v-model="form.clockIn" type="time" class="form-control premium-input" :class="fieldClass('clockIn')" required @input="handleFormMutation('clockIn')" />
                  <div class="invalid-feedback">{{ validationErrors.clockIn }}</div>
                </div>
                <div class="col-md-4 mb-3">
                  <label class="form-label" for="clockOut">Clock Out</label>
                  <input id="clockOut" v-model="form.clockOut" type="time" class="form-control premium-input" :class="fieldClass('clockOut')" required @input="handleFormMutation('clockOut')" />
                  <div class="invalid-feedback">{{ validationErrors.clockOut }}</div>
                </div>
                <div class="col-md-4 mb-3">
                  <label class="form-label" for="source">Source / Device</label>
                  <select id="source" v-model="form.source" class="form-select premium-input" :class="fieldClass('source')" required @change="handleFormMutation('source')">
                    <option value="">Select source</option>
                    <option>Web</option>
                    <option>Mobile</option>
                    <option>Biometric</option>
                  </select>
                  <div class="invalid-feedback">{{ validationErrors.source }}</div>
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
                <button type="submit" class="btn btn-primary">Save Attendance Log</button>
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
import { useRouter } from "vue-router";
import BreadcrumbBar from "@/components/BreadcrumbBar.vue";
import { ApiError, apiRequest } from "@/lib/api";
import { useAuthStore } from "@/stores/auth";

const authStore = useAuthStore();
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
  if (!form.employeeSelect && logId.value !== "Pending") return;
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
    return {
      label: isCorrection.value ? "Pending Correction" : "Draft",
      class: isCorrection.value ? "bg-light-warning text-warning" : "bg-light-primary text-primary",
    };
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

function goBack() {
  router.push("/attendance");
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
    if (isCorrection.value) {
      setAlert("warning", `${logId.value.trim()} submitted for supervisor approval.`);
      return;
    }

    setAlert(
      "success",
      `${logId.value.trim()} saved to the HRIS API. Payroll can reconcile the record against the shift schedule.`
    );
  } catch (error) {
    if (error instanceof ApiError && error.status === 401) {
      setAlert("danger", "Your session expired. Please sign in again.");
      authStore.logout();
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
    employeeData.value = Object.fromEntries(employeeOptions.value.map((e) => [e.employee_code, e.name]));
  } catch {
    employeeOptions.value = [];
    employeeData.value = {};
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
