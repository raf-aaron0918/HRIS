<template>
  <div>
    <BreadcrumbBar section="HR Modules" current="Payroll" />

    <div class="premium-hero mb-4">
      <div class="d-flex flex-column flex-md-row justify-content-between align-items-md-center gap-3">
        <div>
          <div class="premium-badge mb-2">HR Modules</div>
          <h4 class="mb-1 premium-title">Payroll</h4>
          <p class="mb-0 premium-subtitle">Prepare payroll runs with a cleaner workflow, role-based access, and clearer net pay visibility.</p>
        </div>
      </div>
    </div>

    <div class="row g-3">
      <div class="col-12">
        <div class="card h-100 border-0 shadow-sm premium-panel">
          <div class="card-header d-flex flex-column flex-md-row align-items-stretch align-items-md-center justify-content-between gap-3 bg-white border-bottom-0 pt-4 pb-0 premium-panel-header">
            <div>
              <h5 class="mb-0">Payroll Run</h5>
              <small class="text-muted">Keep the essentials in the form and let the system calculate the rest.</small>
            </div>
            <span class="badge" :class="runBadge.class">{{ form.payslipStatus }}</span>
          </div>
          <div class="card-body premium-panel-body">
            <div v-if="!canManagePayroll" class="alert alert-light-warning border-warning mb-3" role="alert">
              Only HR Admin and Payroll Admin users can create or publish payroll runs.
            </div>
            <form novalidate @submit.prevent="handleSubmit">
              <div class="d-flex align-items-center justify-content-between mb-3">
                <div>
                  <h6 class="mb-1">1. Payroll details</h6>
                  <p class="text-muted mb-0 small">Start with the cutoff, mode, and document status.</p>
                </div>
              </div>

              <div class="row">
                <div class="col-md-4 mb-3">
                  <label class="form-label" for="payrollRunId">Payroll ID</label>
                  <input id="payrollRunId" v-model="form.payrollRunId" type="text" class="form-control" placeholder="PR-2026-001" readonly>
                </div>
                <div class="col-md-4 mb-3">
                  <label class="form-label" for="cutoffStart">Cutoff Start</label>
                  <input id="cutoffStart" v-model="form.cutoffStart" type="date" class="form-control" :class="fieldClass('cutoffStart')" required @input="handleFormMutation('cutoffStart')">
                  <div class="invalid-feedback">{{ validationErrors.cutoffStart }}</div>
                </div>
                <div class="col-md-4 mb-3">
                  <label class="form-label" for="cutoffEnd">Cutoff End</label>
                  <input id="cutoffEnd" v-model="form.cutoffEnd" type="date" class="form-control" :class="fieldClass('cutoffEnd')" required @input="handleFormMutation('cutoffEnd')">
                  <div class="invalid-feedback">{{ validationErrors.cutoffEnd }}</div>
                </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label" for="payrollMode">Payroll Mode</label>
                  <select id="payrollMode" v-model="form.payrollMode" class="form-select">
                    <option value="regular">Regular</option>
                    <option value="final">Final Pay</option>
                    <option value="retro">Retro Adjustment</option>
                  </select>
                </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label" for="payslipStatus">Payslip Status</label>
                  <select id="payslipStatus" v-model="form.payslipStatus" class="form-select" required>
                    <option>Draft</option>
                    <option>Published</option>
                  </select>
                </div>
              </div>

              <div class="d-flex align-items-center justify-content-between mt-2 mb-3">
                <div>
                  <h6 class="mb-1">2. Employee context</h6>
                  <p class="text-muted mb-0 small">Pick the employee once and the panel fills the profile fields.</p>
                </div>
              </div>

              <div class="row">
                <div class="col-md-6 mb-3">
                  <label class="form-label" for="employeeSelect">Employee</label>
                  <select id="employeeSelect" v-model="form.employeeSelect" class="form-select" :class="fieldClass('employeeSelect')" required @change="populateEmployee">
                    <option value="">Select employee</option>
                    <option v-for="employee in employeeOptions" :key="employee.employee_code" :value="employee.employee_code">
                      {{ employee.name }}
                    </option>
                  </select>
                  <div class="invalid-feedback">{{ validationErrors.employeeSelect }}</div>
                </div>
                <div class="col-md-3 mb-3">
                  <label class="form-label" for="employeeId">Employee ID</label>
                  <input id="employeeId" :value="form.employeeSelect" type="text" class="form-control" readonly placeholder="Employee ID">
                </div>
                <div class="col-md-3 mb-3">
                  <label class="form-label" for="position">Position</label>
                  <input id="position" :value="selectedEmployee?.position || ''" type="text" class="form-control" readonly placeholder="HR Officer">
                </div>
                <div class="col-md-4 mb-3">
                  <label class="form-label" for="employeeName">Employee Name</label>
                  <input id="employeeName" :value="selectedEmployee?.name || ''" type="text" class="form-control" readonly placeholder="Auto-filled from employee master">
                </div>
                <div class="col-md-4 mb-3">
                  <label class="form-label" for="department">Department</label>
                  <input id="department" :value="selectedEmployee?.department || ''" type="text" class="form-control" readonly placeholder="Administration">
                </div>
                <div class="col-md-4 mb-3">
                  <label class="form-label" for="branch">Branch</label>
                  <input id="branch" :value="selectedEmployee?.branch || ''" type="text" class="form-control" readonly placeholder="Main Branch">
                </div>
              </div>

              <div class="d-flex align-items-center justify-content-between mt-2 mb-3">
                <div>
                  <h6 class="mb-1">3. Earnings and deductions</h6>
                  <p class="text-muted mb-0 small">Use only the values that need review.</p>
                </div>
              </div>

              <div class="row">
                <div class="col-md-4 mb-3">
                  <label class="form-label" for="basePay">Base Pay</label>
                  <input id="basePay" v-model.number="form.basePay" type="number" step="0.01" min="0" class="form-control">
                </div>
                <div class="col-md-4 mb-3">
                  <label class="form-label" for="otPay">OT Pay</label>
                  <input id="otPay" v-model.number="form.otPay" type="number" step="0.01" min="0" class="form-control">
                </div>
                <div class="col-md-4 mb-3">
                  <label class="form-label" for="holidayPay">Holiday Pay</label>
                  <input id="holidayPay" v-model.number="form.holidayPay" type="number" step="0.01" min="0" class="form-control">
                </div>
                <div class="col-md-4 mb-3">
                  <label class="form-label" for="nightDiffPay">Night Differential</label>
                  <input id="nightDiffPay" v-model.number="form.nightDiffPay" type="number" step="0.01" min="0" class="form-control">
                </div>
                <div class="col-md-4 mb-3">
                  <label class="form-label" for="allowances">Allowances</label>
                  <input id="allowances" v-model.number="form.allowances" type="number" step="0.01" min="0" class="form-control">
                </div>
                <div class="col-md-4 mb-3">
                  <label class="form-label" for="taxDeduction">Withholding Tax</label>
                  <input id="taxDeduction" v-model.number="form.taxDeduction" type="number" step="0.01" min="0" class="form-control">
                </div>

                <div class="col-md-3 mb-3">
                  <label class="form-label" for="sssDeduction">SSS</label>
                  <input id="sssDeduction" v-model.number="form.sssDeduction" type="number" step="0.01" min="0" class="form-control">
                </div>
                <div class="col-md-3 mb-3">
                  <label class="form-label" for="philhealthDeduction">PhilHealth</label>
                  <input id="philhealthDeduction" v-model.number="form.philhealthDeduction" type="number" step="0.01" min="0" class="form-control">
                </div>
                <div class="col-md-3 mb-3">
                  <label class="form-label" for="pagibigDeduction">Pag-IBIG</label>
                  <input id="pagibigDeduction" v-model.number="form.pagibigDeduction" type="number" step="0.01" min="0" class="form-control">
                </div>
                <div class="col-md-3 mb-3">
                  <label class="form-label" for="remarks">Remarks</label>
                  <input id="remarks" v-model="form.remarks" type="text" class="form-control" placeholder="Retro, final pay, adjustment notes">
                </div>
              </div>

              <div class="d-grid gap-2 d-md-flex flex-md-wrap mt-2">
                <button type="button" class="btn btn-outline-primary premium-action" :disabled="!canManagePayroll" @click="saveDraft">Save Draft</button>
                <button type="button" class="btn btn-outline-success premium-action" :disabled="!canManagePayroll" @click="applySampleRates">Apply Sample Rates</button>
                <button type="submit" class="btn btn-primary" :disabled="!canManagePayroll">Finalize Payroll Batch</button>
              </div>

              <div class="alert mt-3 mb-0" :class="payrollAlert.class" role="alert">
                {{ payrollAlert.message }}
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
const employeeData = ref({});
const employeeOptions = ref([]);
const canManagePayroll = computed(() =>
  ["HR Admin", "Payroll Admin"].includes(authStore.currentUser?.role || "")
);

const payrollAlert = reactive({
  class: "alert-light-primary border-primary",
  message: "Select an employee and review the earnings before publishing the payroll batch.",
});
const validationErrors = reactive({});

const form = reactive({
  payrollRunId: generatePayrollRunId(),
  cutoffStart: "",
  cutoffEnd: "",
  payrollMode: "regular",
  payslipStatus: "Draft",
  employeeSelect: "",
  basePay: 0,
  otPay: 0,
  holidayPay: 0,
  nightDiffPay: 0,
  allowances: 0,
  taxDeduction: 0,
  sssDeduction: 0,
  philhealthDeduction: 0,
  pagibigDeduction: 0,
  remarks: "",
});

function money(value) {
  return Number(value || 0).toFixed(2);
}

function generatePayrollRunId() {
  const date = new Date();
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  const randomPart = Math.random().toString(36).slice(2, 6).toUpperCase();
  return `PR-${year}${month}${day}-${randomPart}`;
}

function setAlert(type, message) {
  payrollAlert.class = `alert-light-${type} border-${type}`;
  payrollAlert.message = message;
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

const selectedEmployee = computed(() => employeeData.value[form.employeeSelect] || null);

const grossPay = computed(
  () =>
    Number(form.basePay || 0) +
    Number(form.otPay || 0) +
    Number(form.holidayPay || 0) +
    Number(form.nightDiffPay || 0) +
    Number(form.allowances || 0)
);

const totalDeductions = computed(
  () =>
    Number(form.sssDeduction || 0) +
    Number(form.philhealthDeduction || 0) +
    Number(form.pagibigDeduction || 0) +
    Number(form.taxDeduction || 0)
);

const netPay = computed(() => grossPay.value - totalDeductions.value);
const runBadge = computed(() =>
  form.payslipStatus === "Published"
    ? { class: "bg-light-success text-success" }
    : { class: "bg-light-primary text-primary" }
);

function populateEmployee() {
  clearFieldError("employeeSelect");
  const data = employeeData.value[form.employeeSelect];
  if (!data) {
    form.basePay = 0;
    return;
  }

  if (!Number(form.basePay || 0)) {
    form.basePay = data.basePay;
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
          department: employee.department,
          branch: employee.branch || "",
          position: employee.position,
          basePay: 0,
        },
      ])
    );
  } catch {
    employeeOptions.value = [];
    employeeData.value = {};
  }
}

function validateForm() {
  clearValidationErrors();

  if (!form.cutoffStart) validationErrors.cutoffStart = "Cutoff start is required.";
  if (!form.cutoffEnd) validationErrors.cutoffEnd = "Cutoff end is required.";
  if (form.cutoffStart && form.cutoffEnd && new Date(form.cutoffEnd) < new Date(form.cutoffStart)) {
    validationErrors.cutoffEnd = "Cutoff end cannot be earlier than cutoff start.";
  }
  if (!form.employeeSelect) validationErrors.employeeSelect = "Employee is required.";

  if (Object.keys(validationErrors).length) {
    setAlert("danger", "Please complete the highlighted required fields. Optional blank fields can be skipped.");
    return false;
  }

  return true;
}

function updateAlertFromValues() {
  if (netPay.value < 0) {
    setAlert("danger", "Total deductions exceed gross earnings. Review the batch before publishing.");
    return;
  }

  if (netPay.value === 0 && grossPay.value > 0) {
    setAlert("warning", "Gross earnings are fully offset by deductions. Double-check the statutory values before publishing.");
    return;
  }

  setAlert("success", "Payroll batch is balanced and ready for review.");
}

function applySampleRates() {
  if (selectedEmployee.value && !Number(form.basePay || 0)) {
    form.basePay = selectedEmployee.value.basePay;
  }

  const gross = grossPay.value;
  form.holidayPay = Number((gross * 0.1).toFixed(2));
  form.nightDiffPay = Number((gross * 0.05).toFixed(2));
  form.sssDeduction = Number((gross * 0.045).toFixed(2));
  form.philhealthDeduction = Number((gross * 0.05).toFixed(2));
  form.pagibigDeduction = Number(Math.min(100, gross * 0.02).toFixed(2));
  form.taxDeduction = Number((gross * 0.1).toFixed(2));
  setAlert("info", "Sample payroll values applied. Adjust them to match your configured payroll tables.");
}

function saveDraft() {
  if (!canManagePayroll.value) {
    setAlert("danger", "Only HR Admin and Payroll Admin users can create payroll runs.");
    return;
  }
  form.payslipStatus = "Draft";
  setAlert("primary", "Payroll draft saved locally.");
}

function buildPayrollPayload() {
  return {
    payroll_run_id: form.payrollRunId,
    cutoff_start: form.cutoffStart,
    cutoff_end: form.cutoffEnd,
    payroll_mode: form.payrollMode,
    payslip_status: "Published",
    employee_code: form.employeeSelect,
    employee_name: selectedEmployee.value?.name || form.employeeSelect,
    department: selectedEmployee.value?.department || null,
    position: selectedEmployee.value?.position || null,
    branch: selectedEmployee.value?.branch || null,
    base_pay: Number(form.basePay || 0),
    ot_pay: Number(form.otPay || 0),
    holiday_pay: Number(form.holidayPay || 0),
    night_diff_pay: Number(form.nightDiffPay || 0),
    allowances: Number(form.allowances || 0),
    tax_deduction: Number(form.taxDeduction || 0),
    sss_deduction: Number(form.sssDeduction || 0),
    philhealth_deduction: Number(form.philhealthDeduction || 0),
    pagibig_deduction: Number(form.pagibigDeduction || 0),
    gross_pay: grossPay.value,
    total_deductions: totalDeductions.value,
    net_pay: netPay.value,
    remarks: `${form.payrollMode} payroll for ${selectedEmployee.value?.name || form.employeeSelect} published from ${form.cutoffStart} to ${form.cutoffEnd}.`,
  };
}

async function handleSubmit() {
  if (!canManagePayroll.value) {
    setAlert("danger", "Only HR Admin and Payroll Admin users can create payroll runs.");
    return;
  }

  form.payrollRunId = generatePayrollRunId();

  if (!validateForm()) {
    return;
  }

  try {
    await apiRequest("/payroll", {
      method: "POST",
      token: authStore.accessToken,
      body: JSON.stringify(buildPayrollPayload()),
    });
  } catch (error) {
    if (error instanceof ApiError && error.status === 401) {
      setAlert("danger", "Your session expired. Please sign in again.");
      authStore.logout();
    } else {
      setAlert("danger", "Could not save the payroll run to the API. Please make sure FastAPI is running.");
    }
    return;
  }

  form.payslipStatus = "Published";
  form.remarks = `${form.payrollMode} payroll for ${selectedEmployee.value?.name || form.employeeSelect} published from ${form.cutoffStart} to ${form.cutoffEnd}.`;
  setAlert("success", `${form.payrollRunId.trim()} finalized in the HRIS API. Payslip is ready for employee access.`);
}

watch(
  () => [
    form.cutoffStart,
    form.cutoffEnd,
    form.payslipStatus,
    form.employeeSelect,
    form.basePay,
    form.otPay,
    form.holidayPay,
    form.nightDiffPay,
    form.allowances,
    form.taxDeduction,
    form.sssDeduction,
    form.philhealthDeduction,
    form.pagibigDeduction,
  ],
  () => {
    updateAlertFromValues();
  },
  { deep: true }
);

updateAlertFromValues();

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
