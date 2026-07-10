<template>
  <div>
    <BreadcrumbBar section="HR Modules" current="Leave Management" />

    <div class="premium-hero mb-4">
      <div class="d-flex flex-column flex-md-row justify-content-between align-items-md-center gap-3">
        <div>
          <div class="premium-badge mb-2">HR Modules</div>
          <h4 class="mb-1 premium-title">Leave Management</h4>
          <p class="mb-0 premium-subtitle">Submit and review leave requests with credits, policy checks, and payroll impact in one clean flow.</p>
        </div>
      </div>
    </div>

    <div class="row g-3">
      <div class="col-12">
        <div class="card h-100 border-0 shadow-sm premium-panel">
          <div class="card-header d-flex flex-column flex-md-row align-items-stretch align-items-md-center justify-content-between gap-3 bg-white border-bottom-0 pt-4 pb-0 premium-panel-header">
            <div>
              <h5 class="mb-1">Leave Request Form</h5>
              <small class="text-muted">Submit leave requests with live credit checks, policy guidance, and approval routing.</small>
            </div>
            <span class="badge" :class="statusBadge.class">{{ form.status }}</span>
          </div>
          <div class="card-body premium-panel-body">
            <form novalidate @submit.prevent="handleSubmit">
              <div class="mb-3">
                <h6 class="mb-1">1. Employee and schedule details</h6>
                <p class="text-muted mb-0 small">Select the employee, leave type, and requested leave period.</p>
              </div>

              <div class="row">
                <div class="col-md-6 mb-3">
                  <label class="form-label" for="employee">Employee</label>
                  <select id="employee" v-model="form.employee" class="form-select" :class="fieldClass('employee')" required @change="handleFormMutation('employee')">
                    <option value="">Select employee</option>
                    <option v-for="employee in employeeOptions" :key="employee.employee_code" :value="employee.name">
                      {{ employee.name }}
                    </option>
                  </select>
                  <div class="invalid-feedback">{{ validationErrors.employee }}</div>
                </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label" for="leaveType">Leave Type</label>
                  <select id="leaveType" v-model="form.leaveType" class="form-select" :class="fieldClass('leaveType')" required @change="handleFormMutation('leaveType')">
                    <option value="">Select leave type</option>
                    <option value="vacation">Vacation Leave</option>
                    <option value="sick">Sick Leave</option>
                    <option value="emergency">Emergency Leave</option>
                    <option value="maternity">Maternity Leave</option>
                    <option value="paternity">Paternity Leave</option>
                    <option value="unpaid">Leave Without Pay</option>
                  </select>
                  <div class="invalid-feedback">{{ validationErrors.leaveType }}</div>
                </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label" for="startDate">Start Date</label>
                  <input id="startDate" v-model="form.startDate" type="date" class="form-control" :class="fieldClass('startDate')" required @input="handleFormMutation('startDate')">
                  <div class="invalid-feedback">{{ validationErrors.startDate }}</div>
                </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label" for="endDate">End Date</label>
                  <input id="endDate" v-model="form.endDate" type="date" class="form-control" :class="fieldClass('endDate')" required @input="handleFormMutation('endDate')">
                  <div class="invalid-feedback">{{ validationErrors.endDate }}</div>
                </div>
                <div class="col-md-12 mb-3">
                  <label class="form-label">Leave Mode</label>
                  <div class="d-flex flex-wrap gap-3">
                    <div class="form-check">
                      <input id="fullDay" v-model="form.leaveMode" class="form-check-input" type="radio" value="full">
                      <label class="form-check-label" for="fullDay">Full Day</label>
                    </div>
                    <div class="form-check">
                      <input id="halfDayAm" v-model="form.leaveMode" class="form-check-input" type="radio" value="half-am">
                      <label class="form-check-label" for="halfDayAm">Half-day AM</label>
                    </div>
                    <div class="form-check">
                      <input id="halfDayPm" v-model="form.leaveMode" class="form-check-input" type="radio" value="half-pm">
                      <label class="form-check-label" for="halfDayPm">Half-day PM</label>
                    </div>
                  </div>
                </div>
              </div>

              <div class="mt-2 mb-3">
                <h6 class="mb-1">2. Request reason and approval details</h6>
                <p class="text-muted mb-0 small">Add the request explanation, supporting document, and supervisor route.</p>
              </div>

              <div class="row">
                <div class="col-md-12 mb-3">
                  <label class="form-label" for="reason">Reason</label>
                  <textarea id="reason" v-model="form.reason" class="form-control" :class="fieldClass('reason')" rows="4" placeholder="State the reason for the leave request..." required @input="handleFormMutation('reason')"></textarea>
                  <div class="invalid-feedback">{{ validationErrors.reason }}</div>
                </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label" for="attachment">Attachment</label>
                  <input id="attachment" class="form-control" type="file" accept=".pdf,.png,.jpg,.jpeg,.doc,.docx" @change="handleAttachmentChange">
                  <small class="text-muted">Attach a medical certificate or supporting file when policy requires it.</small>
                </div>
                <div class="col-md-3 mb-3">
                  <label class="form-label" for="approver">Immediate Supervisor</label>
                  <select id="approver" v-model="form.approver" class="form-select" :class="fieldClass('approver')" @change="handleFormMutation('approver')">
                    <option value="">Select approver</option>
                    <option v-for="employee in employeeOptions" :key="`approver-${employee.employee_code}`" :value="employee.name">
                      {{ employee.name }}
                    </option>
                  </select>
                  <div class="invalid-feedback">{{ validationErrors.approver }}</div>
                </div>
                <div class="col-md-3 mb-3">
                  <label class="form-label" for="status">Status</label>
                  <select id="status" v-model="form.status" class="form-select">
                    <option>Draft</option>
                    <option>Pending</option>
                    <option>For HR Review</option>
                  </select>
                </div>
              </div>

              <div class="row g-3 mt-1 mb-2">
                <div class="col-md-6">
                  <div class="border rounded-4 p-3 h-100 premium-note">
                    <small class="text-muted d-block mb-1">Policy reminder</small>
                    <span class="text-muted small d-block">Sick leave may require an attachment. Leave without pay affects payroll directly.</span>
                  </div>
                </div>
                <div class="col-md-6">
                  <div class="border rounded-4 p-3 h-100 premium-note">
                    <small class="text-muted d-block mb-1">Validation coverage</small>
                    <span class="text-muted small d-block">The form checks date range, available credits, holidays, and approval readiness.</span>
                  </div>
                </div>
              </div>

              <div class="d-grid gap-2 d-md-flex flex-md-wrap mt-3">
                <button type="button" class="btn btn-outline-primary premium-action" @click="saveDraft">Save Draft</button>
                <button type="submit" class="btn btn-primary">Submit Leave Request</button>
              </div>

              <div class="alert mt-3 mb-0" :class="policyAlert.class" role="alert">
                {{ policyAlert.message }}
              </div>
            </form>
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
const employeeOptions = ref([]);

const availableCredits = ref(18);
const holidaySet = new Set(["2026-07-04", "2026-12-25", "2026-01-01"]);

const form = reactive({
  employee: "",
  leaveType: "",
  startDate: "",
  endDate: "",
  leaveMode: "full",
  reason: "",
  attachment: null,
  approver: "",
  status: "Draft",
});

const policyAlert = reactive({
  class: "alert-light-primary border-primary",
  message: "Fill out the form to see leave balance checks, payroll impact, and policy warnings here.",
});
const validationErrors = reactive({});

const leaveTypesRequiringCredits = new Set(["vacation", "sick", "emergency"]);

function generateLeaveRequestId() {
  const date = new Date();
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  const randomPart = Math.random().toString(36).slice(2, 6).toUpperCase();
  return `LV-${year}${month}${day}-${randomPart}`;
}

function getLeaveModeFactor() {
  return form.leaveMode.startsWith("half") ? 0.5 : 1;
}

function isWeekend(date) {
  const day = date.getDay();
  return day === 0 || day === 6;
}

function isHoliday(date) {
  return holidaySet.has(date.toISOString().slice(0, 10));
}

const leaveDays = computed(() => {
  if (!form.startDate || !form.endDate) return 0;

  const start = new Date(`${form.startDate}T00:00:00`);
  const end = new Date(`${form.endDate}T00:00:00`);

  if (Number.isNaN(start.getTime()) || Number.isNaN(end.getTime()) || end < start) return 0;

  let total = 0;
  const cursor = new Date(start);
  while (cursor <= end) {
    if (!isWeekend(cursor) && !isHoliday(cursor)) {
      total += 1;
    }
    cursor.setDate(cursor.getDate() + 1);
  }

  return total * getLeaveModeFactor();
});

const creditsUsed = computed(() => (leaveTypesRequiringCredits.has(form.leaveType) ? leaveDays.value : 0));
const payrollImpact = computed(() => (form.leaveType === "unpaid" ? leaveDays.value : 0));
const balanceAfter = computed(() => Math.max(availableCredits.value - creditsUsed.value, 0));
const statusBadge = computed(() => {
  if (form.status === "Pending") return { class: "bg-light-warning text-warning" };
  if (form.status === "For HR Review") return { class: "bg-light-danger text-danger" };
  return { class: "bg-light-primary text-primary" };
});

function setPolicyAlert(type, message) {
  policyAlert.class = `alert-light-${type} border-${type}`;
  policyAlert.message = message;
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

function updatePolicyAlert() {
  const hasInvalidRange =
    form.startDate && form.endDate && new Date(form.endDate) < new Date(form.startDate);

  if (hasInvalidRange) {
    setPolicyAlert("danger", "End date cannot be earlier than the start date.");
    return;
  }

  if (!form.startDate || !form.endDate || !form.leaveType) {
    setPolicyAlert("primary", "Fill out the form to see leave balance checks, payroll impact, and policy warnings here.");
    return;
  }

  if (form.leaveType === "sick" && !form.attachment) {
    setPolicyAlert("warning", "Sick leave may need an attachment depending on company policy.");
    return;
  }

  if (creditsUsed.value > availableCredits.value && leaveTypesRequiringCredits.has(form.leaveType)) {
    setPolicyAlert("danger", "Not enough leave credits for this request. HR or policy override would be required.");
    return;
  }

  if (
    isHoliday(new Date(`${form.startDate}T00:00:00`)) ||
    isHoliday(new Date(`${form.endDate}T00:00:00`))
  ) {
    setPolicyAlert("info", "The selected range touches a holiday. The system should verify whether the holiday is chargeable.");
    return;
  }

  setPolicyAlert(
    "success",
    `Leave looks valid. Estimated credits used: ${creditsUsed.value.toFixed(1)}. Balance after request: ${balanceAfter.value.toFixed(1)}.`
  );
}

function handleAttachmentChange(event) {
  const files = event.target.files;
  form.attachment = files && files.length ? files[0] : null;
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
  } catch {
    employeeOptions.value = [];
  }
}

function validateForm() {
  clearValidationErrors();

  if (!form.employee) validationErrors.employee = "Employee is required.";
  if (!form.leaveType) validationErrors.leaveType = "Leave type is required.";
  if (!form.startDate) validationErrors.startDate = "Start date is required.";
  if (!form.endDate) validationErrors.endDate = "End date is required.";
  if (form.startDate && form.endDate && new Date(form.endDate) < new Date(form.startDate)) {
    validationErrors.endDate = "End date cannot be earlier than the start date.";
  }
  if (!form.reason.trim()) validationErrors.reason = "Reason is required.";
  if (!form.approver) validationErrors.approver = "Approver is required.";

  if (Object.keys(validationErrors).length) {
    setPolicyAlert("danger", "Please complete the highlighted required fields. Optional blank fields can be skipped.");
    return false;
  }

  return true;
}

function saveDraft() {
  form.status = "Draft";
  updatePolicyAlert();
  setPolicyAlert("primary", "Leave request draft saved locally.");
}

function buildLeavePayload(status) {
  return {
    request_id: generateLeaveRequestId(),
    employee_name: form.employee,
    leave_type: form.leaveType,
    start_date: form.startDate,
    end_date: form.endDate,
    leave_mode: form.leaveMode,
    reason: form.reason.trim(),
    attachment_name: form.attachment?.name || null,
    approver: form.approver,
    status,
    leave_days: leaveDays.value,
    credits_used: creditsUsed.value,
    payroll_impact: payrollImpact.value,
    notes:
      form.leaveType === "unpaid"
        ? "Employee files leave, supervisor approves, and payroll reflects leave without pay."
        : "Employee files leave, supervisor approves, and HR reviews when policy requires it.",
  };
}

async function handleSubmit() {
  updatePolicyAlert();

  if (!validateForm()) {
    return;
  }

  const nextStatus = form.leaveType === "sick" ? "For HR Review" : "Pending";

  try {
    await apiRequest("/leave", {
      method: "POST",
      token: authStore.accessToken,
      body: JSON.stringify(buildLeavePayload(nextStatus)),
    });
  } catch (error) {
    if (error instanceof ApiError && error.status === 401) {
      setPolicyAlert("danger", "Your session expired. Please sign in again.");
      authStore.logout();
    } else {
      setPolicyAlert("danger", "Could not save the leave request to the API. Please make sure FastAPI is running.");
    }
    return;
  }

  form.status = nextStatus;
  setPolicyAlert("success", `${form.employee} leave request was saved to the HRIS API and is ready for approval.`);

  if (leaveTypesRequiringCredits.has(form.leaveType)) {
    availableCredits.value = Math.max(0, availableCredits.value - leaveDays.value);
  }

  updatePolicyAlert();
}

watch(
  () => [
    form.employee,
    form.leaveType,
    form.startDate,
    form.endDate,
    form.leaveMode,
    form.reason,
    form.approver,
    form.status,
    form.attachment,
  ],
  () => {
    updatePolicyAlert();
  },
  { deep: true }
);

updatePolicyAlert();

onMounted(() => {
  fetchEmployees();
});
</script>

<style scoped>
.premium-hero {
  border: 1px solid rgba(16, 24, 40, 0.08);
  border-radius: 1.5rem;
  padding: 1.25rem 1.5rem;
  background:
    linear-gradient(135deg, rgba(13, 110, 253, 0.08), rgba(13, 110, 253, 0.02)),
    #fff;
  box-shadow: 0 10px 30px rgba(15, 23, 42, 0.05);
}

.premium-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  border-radius: 999px;
  padding: 0.35rem 0.75rem;
  background: rgba(13, 110, 253, 0.08);
  color: #0d6efd;
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}

.premium-title {
  font-weight: 800;
  letter-spacing: -0.03em;
}

.premium-subtitle {
  color: #64748b;
  max-width: 56rem;
}

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

.premium-note {
  border-color: rgba(148, 163, 184, 0.18) !important;
  background: linear-gradient(180deg, #fff 0%, #fbfdff 100%);
}

.premium-action {
  border-color: rgba(13, 110, 253, 0.22);
}

@media (max-width: 767.98px) {
  .premium-hero {
    padding: 1rem 1.1rem;
    border-radius: 1.15rem;
  }

  .premium-panel-header {
    padding-top: 1.1rem !important;
  }
}
</style>
