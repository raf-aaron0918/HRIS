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
                  <label class="form-label" for="status">Submission Status</label>
                  <input id="status" :value="submissionStatusLabel" type="text" class="form-control" readonly>
                  <small class="text-muted">Leave requests are submitted as pending, then approved or rejected by HR.</small>
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

              <div v-if="!canManageLeaveRequests" class="alert alert-light-info border-info mt-3 mb-0">
                You can submit leave here. Approval actions are available to `HR Admin` and `Immediate Supervisor` accounts in the queue below.
              </div>

              <div class="alert mt-3 mb-0" :class="policyAlert.class" role="alert">
                {{ policyAlert.message }}
              </div>
            </form>
          </div>
        </div>
      </div>

      <div class="col-12">
        <div class="card border-0 shadow-sm premium-panel">
          <div class="card-header d-flex flex-column flex-md-row align-items-stretch align-items-md-center justify-content-between gap-3 bg-white border-bottom-0 pt-4 pb-0 premium-panel-header">
            <div>
              <h5 class="mb-1">Leave Approval Queue</h5>
              <small class="text-muted">Review submitted leave requests and approve or reject them directly from HR.</small>
            </div>
            <span class="badge bg-light-warning text-warning">{{ pendingLeaveCount }} pending</span>
          </div>
          <div class="card-body premium-panel-body">
            <div v-if="queueError" class="alert alert-warning mb-3">{{ queueError }}</div>
            <div v-if="queueLoading" class="text-muted small">Loading leave requests...</div>
            <template v-else>
              <div class="queue-category-row mb-4">
                <button
                  v-for="category in queueCategories"
                  :key="category.value"
                  type="button"
                  class="btn btn-sm queue-category-button"
                  :class="activeQueueCategory === category.value ? category.activeClass : 'btn-outline-secondary'"
                  @click="activeQueueCategory = category.value"
                >
                  {{ category.label }}
                  <span class="ms-1">{{ category.count }}</span>
                </button>
              </div>

              <div v-if="selectedLeaveRequest" class="border p-3 p-md-4 mb-4 premium-review-panel">
                <div class="d-flex flex-column flex-md-row justify-content-between align-items-start gap-3 mb-3">
                  <div>
                    <h6 class="mb-1">Leave Request Review</h6>
                    <div class="text-muted small">{{ selectedLeaveRequest.employee_name }} - {{ selectedLeaveRequest.request_id }}</div>
                  </div>
                  <div class="d-flex flex-wrap gap-2">
                    <span class="badge" :class="getRequestStatusBadge(selectedLeaveRequest.status).class">
                      {{ selectedLeaveRequest.status }}
                    </span>
                    <button type="button" class="btn btn-sm btn-outline-secondary" @click="selectedLeaveRequest = null">Close</button>
                  </div>
                </div>

                <div class="row g-3">
                  <div class="col-md-6">
                    <div class="premium-review-item">
                      <div class="premium-review-label">Leave Type</div>
                      <div class="premium-review-value">{{ formatLeaveType(selectedLeaveRequest.leave_type) }}</div>
                    </div>
                  </div>
                  <div class="col-md-6">
                    <div class="premium-review-item">
                      <div class="premium-review-label">Date Range</div>
                      <div class="premium-review-value">{{ selectedLeaveRequest.start_date }} to {{ selectedLeaveRequest.end_date }}</div>
                    </div>
                  </div>
                  <div class="col-md-6">
                    <div class="premium-review-item">
                      <div class="premium-review-label">Leave Mode</div>
                      <div class="premium-review-value">{{ formatLeaveType(selectedLeaveRequest.leave_mode) }}</div>
                    </div>
                  </div>
                  <div class="col-md-6">
                    <div class="premium-review-item">
                      <div class="premium-review-label">Approver</div>
                      <div class="premium-review-value">{{ selectedLeaveRequest.approver || "Not assigned" }}</div>
                    </div>
                  </div>
                  <div class="col-md-12">
                    <div class="premium-review-item">
                      <div class="premium-review-label">Reason</div>
                      <div class="premium-review-value">{{ selectedLeaveRequest.reason || "No reason provided." }}</div>
                    </div>
                  </div>
                  <div class="col-md-12">
                    <div class="premium-review-item">
                      <div class="premium-review-label">Proof / Attachment</div>
                      <div class="premium-review-value">{{ selectedLeaveRequest.attachment_name || "No attachment submitted." }}</div>
                      <div v-if="selectedLeaveRequest.attachment_data_url" class="mt-2">
                        <a
                          class="btn btn-sm btn-outline-primary"
                          :href="selectedLeaveRequest.attachment_data_url"
                          :download="selectedLeaveRequest.attachment_name || 'leave-attachment'"
                          target="_blank"
                          rel="noopener noreferrer"
                        >
                          View attachment
                        </a>
                      </div>
                    </div>
                  </div>
                </div>

                <div class="d-grid gap-2 d-md-flex justify-content-md-end mt-3">
                  <button
                    type="button"
                    class="btn btn-outline-success"
                    :disabled="!canApproveRequest(selectedLeaveRequest) || decisionRequestId === selectedLeaveRequest.request_id"
                    @click="applyLeaveDecision(selectedLeaveRequest, 'Approved')"
                  >
                    {{ decisionRequestId === selectedLeaveRequest.request_id && decisionStatus === 'Approved' ? "Saving..." : "Approve" }}
                  </button>
                  <button
                    type="button"
                    class="btn btn-outline-danger"
                    :disabled="!canApproveRequest(selectedLeaveRequest) || decisionRequestId === selectedLeaveRequest.request_id"
                    @click="applyLeaveDecision(selectedLeaveRequest, 'Rejected')"
                  >
                    {{ decisionRequestId === selectedLeaveRequest.request_id && decisionStatus === 'Rejected' ? "Saving..." : "Reject" }}
                  </button>
                </div>
              </div>

              <div class="d-none d-md-block table-responsive">
                <table class="table table-hover align-middle mb-0 premium-table">
                  <thead class="table-light">
                    <tr>
                      <th>Request ID</th>
                      <th>Employee</th>
                      <th>Leave Type</th>
                      <th>Dates</th>
                      <th>Approver</th>
                      <th>Status</th>
                      <th class="text-end">Action</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="request in filteredLeaveRequests" :key="request.request_id">
                      <td>{{ request.request_id }}</td>
                      <td>{{ request.employee_name }}</td>
                      <td>{{ formatLeaveType(request.leave_type) }}</td>
                      <td>{{ request.start_date }} to {{ request.end_date }}</td>
                      <td>{{ request.approver }}</td>
                      <td>
                        <span class="badge" :class="getRequestStatusBadge(request.status).class">
                          {{ request.status }}
                        </span>
                      </td>
                      <td class="text-end">
                        <div class="d-inline-flex gap-2">
                          <button
                            type="button"
                            class="btn btn-sm btn-outline-primary"
                            @click="selectedLeaveRequest = request"
                          >
                            View
                          </button>
                          <button
                            type="button"
                            class="btn btn-sm btn-outline-success"
                            :disabled="!canApproveRequest(request) || decisionRequestId === request.request_id"
                            @click="applyLeaveDecision(request, 'Approved')"
                          >
                            {{ decisionRequestId === request.request_id && decisionStatus === 'Approved' ? "Saving..." : "Approve" }}
                          </button>
                          <button
                            type="button"
                            class="btn btn-sm btn-outline-danger"
                            :disabled="!canApproveRequest(request) || decisionRequestId === request.request_id"
                            @click="applyLeaveDecision(request, 'Rejected')"
                          >
                            {{ decisionRequestId === request.request_id && decisionStatus === 'Rejected' ? "Saving..." : "Reject" }}
                          </button>
                        </div>
                      </td>
                    </tr>
                    <tr v-if="!filteredLeaveRequests.length">
                      <td colspan="7" class="text-center text-muted py-4">{{ emptyQueueMessage }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>

              <div class="d-grid gap-3 d-md-none">
                <div v-for="request in filteredLeaveRequests" :key="`mobile-${request.request_id}`" class="border p-3 shadow-sm premium-mobile-card">
                  <div class="d-flex justify-content-between align-items-start gap-2">
                    <div>
                      <div class="fw-semibold">{{ request.employee_name }}</div>
                      <div class="small text-muted">{{ request.request_id }}</div>
                    </div>
                    <span class="badge" :class="getRequestStatusBadge(request.status).class">{{ request.status }}</span>
                  </div>
                  <div class="small text-muted mt-2">Type: {{ formatLeaveType(request.leave_type) }}</div>
                  <div class="small text-muted">Dates: {{ request.start_date }} to {{ request.end_date }}</div>
                  <div class="small text-muted">Approver: {{ request.approver }}</div>
                  <div class="d-grid gap-2 mt-3">
                    <button
                      type="button"
                      class="btn btn-sm btn-outline-primary"
                      @click="selectedLeaveRequest = request"
                    >
                      View
                    </button>
                    <button
                      type="button"
                      class="btn btn-sm btn-outline-success"
                      :disabled="!canApproveRequest(request) || decisionRequestId === request.request_id"
                      @click="applyLeaveDecision(request, 'Approved')"
                    >
                      {{ decisionRequestId === request.request_id && decisionStatus === 'Approved' ? "Saving..." : "Approve" }}
                    </button>
                    <button
                      type="button"
                      class="btn btn-sm btn-outline-danger"
                      :disabled="!canApproveRequest(request) || decisionRequestId === request.request_id"
                      @click="applyLeaveDecision(request, 'Rejected')"
                    >
                      {{ decisionRequestId === request.request_id && decisionStatus === 'Rejected' ? "Saving..." : "Reject" }}
                    </button>
                  </div>
                </div>

                <div v-if="!filteredLeaveRequests.length" class="text-center text-muted py-4">{{ emptyQueueMessage }}</div>
              </div>
            </template>
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
const leaveRequests = ref([]);
const queueLoading = ref(false);
const queueError = ref("");
const decisionRequestId = ref("");
const decisionStatus = ref("");
const selectedLeaveRequest = ref(null);
const activeQueueCategory = ref("Pending");

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
const approvalEligibleStatuses = new Set(["Pending", "For HR Review"]);

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
const pendingLeaveCount = computed(() =>
  leaveRequests.value.filter((request) => approvalEligibleStatuses.has(request.status)).length
);
const approvedLeaveCount = computed(() =>
  leaveRequests.value.filter((request) => String(request.status || "").toLowerCase() === "approved").length
);
const rejectedLeaveCount = computed(() =>
  leaveRequests.value.filter((request) => String(request.status || "").toLowerCase() === "rejected").length
);
const queueCategories = computed(() => [
  {
    value: "Pending",
    label: "Pending",
    count: pendingLeaveCount.value,
    activeClass: "btn-warning",
  },
  {
    value: "Approved",
    label: "Approved",
    count: approvedLeaveCount.value,
    activeClass: "btn-success",
  },
  {
    value: "Rejected",
    label: "Rejected",
    count: rejectedLeaveCount.value,
    activeClass: "btn-danger",
  },
]);
const filteredLeaveRequests = computed(() => {
  const activeCategory = activeQueueCategory.value.toLowerCase();
  return leaveRequests.value.filter((request) => String(request.status || "").toLowerCase() === activeCategory);
});
const emptyQueueMessage = computed(() => `No ${activeQueueCategory.value.toLowerCase()} leave requests available.`);
const canManageLeaveRequests = computed(() => {
  const role = authStore.currentUser?.role || "";
  return role === "HR Admin" || role === "Immediate Supervisor";
});
const submissionStatusLabel = computed(() => (form.status === "Draft" ? "Draft" : "Pending"));
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

function readFileAsDataUrl(file) {
  return new Promise((resolve, reject) => {
    if (!file) {
      resolve(null);
      return;
    }

    const reader = new FileReader();
    reader.onload = () => resolve(typeof reader.result === "string" ? reader.result : null);
    reader.onerror = () => reject(new Error("Could not read attachment."));
    reader.readAsDataURL(file);
  });
}

function getRequestStatusBadge(status) {
  if (status === "Approved") return { class: "bg-light-success text-success" };
  if (status === "Rejected") return { class: "bg-light-danger text-danger" };
  if (status === "Pending") return { class: "bg-light-warning text-warning" };
  if (status === "For HR Review") return { class: "bg-light-info text-info" };
  return { class: "bg-light-secondary text-secondary" };
}

function formatLeaveType(value) {
  return String(value || "")
    .split("-")
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(" ");
}

function canApproveRequest(request) {
  return canManageLeaveRequests.value && approvalEligibleStatuses.has(request.status);
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

async function fetchLeaveRequests() {
  if (!authStore.accessToken) return;

  queueLoading.value = true;
  queueError.value = "";

  try {
    const response = await apiRequest("/leave", {
      token: authStore.accessToken,
    });
    leaveRequests.value = response.items || [];
  } catch (error) {
    if (error instanceof ApiError && error.status === 401) {
      authStore.logout();
    } else {
      queueError.value = "Could not load leave requests.";
    }
    leaveRequests.value = [];
  } finally {
    queueLoading.value = false;
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

async function buildLeavePayload(status) {
  const attachmentDataUrl = await readFileAsDataUrl(form.attachment);

  return {
    request_id: generateLeaveRequestId(),
    employee_name: form.employee,
    leave_type: form.leaveType,
    start_date: form.startDate,
    end_date: form.endDate,
    leave_mode: form.leaveMode,
    reason: form.reason.trim(),
    attachment_name: form.attachment?.name || null,
    attachment_data_url: attachmentDataUrl,
    attachment_mime_type: form.attachment?.type || null,
    approver: form.approver,
    status,
    leave_days: leaveDays.value,
    credits_used: creditsUsed.value,
    payroll_impact: payrollImpact.value,
    notes:
      form.leaveType === "unpaid"
        ? "Employee filed leave without pay. Once approved, payroll should reflect the deduction."
        : "Employee filed leave and it is waiting for HR or supervisor approval.",
  };
}

async function handleSubmit() {
  updatePolicyAlert();

  if (!validateForm()) {
    return;
  }

  const nextStatus = "Pending";

  try {
    const payload = await buildLeavePayload(nextStatus);

    await apiRequest("/leave", {
      method: "POST",
      token: authStore.accessToken,
      body: JSON.stringify(payload),
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

  await fetchLeaveRequests();
  updatePolicyAlert();
}

async function applyLeaveDecision(request, status) {
  if (!canApproveRequest(request)) return;

  decisionRequestId.value = request.request_id;
  decisionStatus.value = status;

  try {
    await apiRequest(`/leave/${encodeURIComponent(request.request_id)}`, {
      method: "PUT",
      token: authStore.accessToken,
      body: JSON.stringify({
        employee_name: request.employee_name,
        leave_type: request.leave_type,
        start_date: request.start_date,
        end_date: request.end_date,
        leave_mode: request.leave_mode,
        reason: request.reason,
        attachment_name: request.attachment_name || null,
        attachment_data_url: request.attachment_data_url || null,
        attachment_mime_type: request.attachment_mime_type || null,
        approver: authStore.currentUser?.full_name || request.approver,
        status,
        leave_days: request.leave_days,
        credits_used: request.credits_used,
        payroll_impact: request.payroll_impact,
        notes: request.notes || null,
      }),
    });

    leaveRequests.value = leaveRequests.value.map((item) =>
      item.request_id === request.request_id
        ? {
            ...item,
            status,
            approver: authStore.currentUser?.full_name || item.approver,
          }
        : item
    );

    if (selectedLeaveRequest.value?.request_id === request.request_id) {
      selectedLeaveRequest.value = {
        ...selectedLeaveRequest.value,
        status,
        approver: authStore.currentUser?.full_name || selectedLeaveRequest.value.approver,
      };
    }

    setPolicyAlert(
      status === "Approved" ? "success" : "warning",
      `${request.employee_name} leave request was marked as ${status.toLowerCase()}.`
    );
  } catch (error) {
    if (error instanceof ApiError && error.status === 401) {
      authStore.logout();
      return;
    }

    setPolicyAlert("danger", `Could not update the leave request to ${status.toLowerCase()}.`);
  } finally {
    decisionRequestId.value = "";
    decisionStatus.value = "";
  }
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

watch(
  () => [activeQueueCategory.value, filteredLeaveRequests.value.map((request) => request.request_id).join("|")],
  () => {
    if (
      selectedLeaveRequest.value &&
      !filteredLeaveRequests.value.some((request) => request.request_id === selectedLeaveRequest.value.request_id)
    ) {
      selectedLeaveRequest.value = null;
    }
  }
);

updatePolicyAlert();

onMounted(() => {
  fetchEmployees();
  fetchLeaveRequests();
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

.premium-table thead th {
  color: #475569;
  font-size: 0.78rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  border-bottom-color: rgba(148, 163, 184, 0.2);
}

.premium-mobile-card {
  border-color: rgba(148, 163, 184, 0.18) !important;
  background: linear-gradient(180deg, #fff 0%, #fbfdff 100%);
}

.premium-review-panel {
  border-color: rgba(148, 163, 184, 0.2) !important;
  background: linear-gradient(180deg, rgba(13, 110, 253, 0.03) 0%, #fff 100%);
}

.premium-review-item {
  border: 1px solid rgba(148, 163, 184, 0.18);
  padding: 0.9rem 1rem;
  background: #fff;
}

.premium-review-label {
  color: #64748b;
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  margin-bottom: 0.35rem;
}

.premium-review-value {
  color: #0f172a;
  white-space: pre-wrap;
  word-break: break-word;
}

.queue-category-row {
  display: flex;
  flex-wrap: nowrap;
  gap: 0.5rem;
  overflow-x: auto;
  padding-bottom: 0.15rem;
}

.queue-category-button {
  flex: 0 0 auto;
  white-space: nowrap;
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
