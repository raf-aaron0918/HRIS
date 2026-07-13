<template>
  <div>
    <BreadcrumbBar section="HR Modules / Payroll" current="Batch Finalization" />

    <div class="premium-hero mb-3">
      <div class="d-flex flex-column flex-lg-row justify-content-between align-items-lg-center gap-3">
        <div>
          <div class="premium-badge mb-2">Payroll Batch</div>
          <h4 class="mb-1 premium-title">Finalize Payroll in Batch</h4>
          <p class="mb-0 premium-subtitle">Load one cutoff, review employee salary results, then publish selected payroll records in one action.</p>
        </div>
        <RouterLink to="/payroll" class="btn btn-outline-primary">
          <i class="ti ti-arrow-left"></i> Single Payroll
        </RouterLink>
      </div>
    </div>

    <div class="card border-0 shadow-sm premium-panel mb-3">
      <div class="card-body premium-panel-body">
        <div v-if="!canManagePayroll" class="alert alert-light-warning border-warning mb-3" role="alert">
          Only HR Admin and Payroll Admin users can finalize payroll batches.
        </div>

        <div class="row align-items-end">
          <div class="col-md-3 mb-3">
            <label class="form-label" for="batchCutoffStart">Cutoff Start</label>
            <input id="batchCutoffStart" v-model="batchForm.cutoffStart" type="date" class="form-control">
          </div>
          <div class="col-md-3 mb-3">
            <label class="form-label" for="batchCutoffEnd">Cutoff End</label>
            <input id="batchCutoffEnd" v-model="batchForm.cutoffEnd" type="date" class="form-control">
          </div>
          <div class="col-md-3 mb-3">
            <label class="form-label" for="batchPayrollMode">Payroll Mode</label>
            <select id="batchPayrollMode" v-model="batchForm.payrollMode" class="form-select">
              <option value="regular">Regular</option>
              <option value="final">Final Pay</option>
              <option value="retro">Retro Adjustment</option>
            </select>
          </div>
          <div class="col-md-3 mb-3 d-grid">
            <button type="button" class="btn btn-primary" :disabled="!canManagePayroll || isLoadingBatch" @click="loadBatch">
              {{ isLoadingBatch ? "Loading..." : "Load Batch Preview" }}
            </button>
          </div>
        </div>

        <div class="row g-2">
          <div class="col-6 col-md-3">
            <div class="summary-tile">
              <small>Employees</small>
              <strong>{{ batchRows.length }}</strong>
            </div>
          </div>
          <div class="col-6 col-md-3">
            <div class="summary-tile">
              <small>Selected</small>
              <strong>{{ selectedRows.length }}</strong>
            </div>
          </div>
          <div class="col-6 col-md-3">
            <div class="summary-tile">
              <small>Total Net Pay</small>
              <strong>{{ money(selectedNetPay) }}</strong>
            </div>
          </div>
          <div class="col-6 col-md-3">
            <div class="summary-tile">
              <small>Blocked</small>
              <strong>{{ blockedRows.length }}</strong>
            </div>
          </div>
        </div>

        <div class="alert mt-3 mb-0" :class="batchAlert.class" role="alert">{{ batchAlert.message }}</div>
      </div>
    </div>

    <div class="card border-0 shadow-sm premium-panel">
      <div class="card-header bg-white border-bottom-0 pt-4 premium-panel-header">
        <div class="d-flex flex-column flex-md-row justify-content-between gap-3">
          <div>
            <h5 class="mb-1">Batch Preview</h5>
            <small class="text-muted">Review calculated payroll before publishing. Incomplete logs are blocked by default.</small>
          </div>
          <div class="d-flex flex-wrap gap-2">
            <button type="button" class="btn btn-outline-secondary btn-sm" :disabled="!batchRows.length" @click="toggleAllRows">
              {{ allSelectableRowsSelected ? "Unselect All" : "Select All Ready" }}
            </button>
            <button type="button" class="btn btn-success btn-sm" :disabled="!canManagePayroll || isFinalizing || !selectedRows.length" @click="finalizeBatch">
              {{ isFinalizing ? "Finalizing..." : `Finalize ${selectedRows.length} Payroll(s)` }}
            </button>
          </div>
        </div>
      </div>
      <div class="card-body premium-panel-body">
        <div class="table-responsive d-none d-lg-block">
          <table class="table table-hover align-middle">
            <thead>
              <tr>
                <th>
                  <input type="checkbox" class="form-check-input" :checked="allSelectableRowsSelected" :disabled="!batchRows.length" @change="toggleAllRows">
                </th>
                <th>Employee</th>
                <th>Attendance</th>
                <th>Base Pay</th>
                <th>Deductions</th>
                <th>Net Pay</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="row in batchRows" :key="row.employeeCode">
                <td>
                  <input v-model="row.selected" type="checkbox" class="form-check-input" :disabled="row.blocked || row.finalized">
                </td>
                <td>
                  <strong>{{ row.employeeName }}</strong>
                  <div class="text-muted small">{{ row.employeeCode }} · {{ row.department || "No department" }}</div>
                </td>
                <td>
                  <div class="small">{{ row.paidHours }}h paid / {{ row.scheduledHours }}h scheduled</div>
                  <div class="text-muted small">{{ row.presentDays }} present · {{ row.leaveDays }} leave · {{ row.absentDays }} absent</div>
                </td>
                <td>{{ money(row.basePay) }}</td>
                <td>{{ money(row.totalDeductions) }}</td>
                <td><strong>{{ money(row.netPay) }}</strong></td>
                <td><span class="badge" :class="row.statusClass">{{ row.statusLabel }}</span></td>
              </tr>
              <tr v-if="!batchRows.length">
                <td colspan="7" class="text-center text-muted py-4">Choose a cutoff and load the batch preview.</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="d-lg-none">
          <div v-for="row in batchRows" :key="`mobile-${row.employeeCode}`" class="batch-card">
            <div class="d-flex justify-content-between gap-3">
              <div>
                <h6 class="mb-1">{{ row.employeeName }}</h6>
                <div class="text-muted small">{{ row.employeeCode }} · {{ row.department || "No department" }}</div>
              </div>
              <input v-model="row.selected" type="checkbox" class="form-check-input" :disabled="row.blocked || row.finalized">
            </div>
            <div class="row g-2 mt-2">
              <div class="col-6"><small>Base</small><strong>{{ money(row.basePay) }}</strong></div>
              <div class="col-6"><small>Net</small><strong>{{ money(row.netPay) }}</strong></div>
              <div class="col-6"><small>Paid</small><strong>{{ row.paidHours }}h</strong></div>
              <div class="col-6"><small>Absent</small><strong>{{ row.absentDays }}</strong></div>
            </div>
            <span class="badge mt-3" :class="row.statusClass">{{ row.statusLabel }}</span>
          </div>
          <div v-if="!batchRows.length" class="text-center text-muted py-4">Choose a cutoff and load the batch preview.</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, reactive, ref, watch } from "vue";
import { RouterLink } from "vue-router";
import BreadcrumbBar from "@/components/BreadcrumbBar.vue";
import { ApiError, apiRequest } from "@/lib/api";
import { useAuthStore } from "@/stores/auth";

const authStore = useAuthStore();
const employees = ref([]);
const batchRows = ref([]);
const isLoadingBatch = ref(false);
const isFinalizing = ref(false);
const canManagePayroll = computed(() =>
  ["HR Admin", "Payroll Admin"].includes(authStore.currentUser?.role || "")
);

const batchForm = reactive({
  cutoffStart: "",
  cutoffEnd: "",
  payrollMode: "regular",
});

const batchAlert = reactive({
  class: "alert-light-primary border-primary",
  message: "Select a cutoff to preview payroll for all employees.",
});

const selectedRows = computed(() => batchRows.value.filter((row) => row.selected && !row.blocked && !row.finalized));
const blockedRows = computed(() => batchRows.value.filter((row) => row.blocked));
const selectedNetPay = computed(() => selectedRows.value.reduce((total, row) => total + row.netPay, 0));
const allSelectableRowsSelected = computed(() => {
  const selectable = batchRows.value.filter((row) => !row.blocked && !row.finalized);
  return selectable.length > 0 && selectable.every((row) => row.selected);
});

function setAlert(type, message) {
  batchAlert.class = `alert-light-${type} border-${type}`;
  batchAlert.message = message;
}

function money(value) {
  return Number(value || 0).toFixed(2);
}

function roundMoney(value) {
  return Number(Number(value || 0).toFixed(2));
}

function generatePayrollRunId(employeeCode) {
  const date = new Date();
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  const randomPart = Math.random().toString(36).slice(2, 6).toUpperCase();
  return `PR-${year}${month}${day}-${employeeCode}-${randomPart}`;
}

function calculatePagibigEmployeeShare(monthlyBasicSalary) {
  const salary = Math.max(0, Number(monthlyBasicSalary || 0));
  const salaryBase = Math.min(salary, 10000);
  const rate = salary <= 1500 ? 0.01 : 0.02;
  return roundMoney(Math.min(salaryBase * rate, 200));
}

function calculatePhilhealthEmployeeShare(monthlyBasicSalary) {
  const salary = Math.max(0, Number(monthlyBasicSalary || 0));
  if (salary <= 0) return 0;
  return roundMoney(Math.min(Math.max(salary, 10000), 100000) * 0.025);
}

function calculateSssEmployeeShare(monthlyBasicSalary) {
  const salary = Math.max(0, Number(monthlyBasicSalary || 0));
  if (salary <= 0) return 0;
  const boundedSalary = Math.min(Math.max(salary, 5000), 35000);
  const monthlySalaryCredit = Math.min(Math.max(Math.floor((boundedSalary + 250) / 500) * 500, 5000), 35000);
  return roundMoney(monthlySalaryCredit * 0.05);
}

function parseTimeToMinutes(value, fallback) {
  const [hourText, minuteText] = String(value || fallback).split(":");
  const hour = Number(hourText);
  const minute = Number(minuteText);
  if (Number.isNaN(hour) || Number.isNaN(minute)) return 0;
  return hour * 60 + minute;
}

function scheduledHoursPerDay(employee) {
  const start = parseTimeToMinutes(employee.shiftStart, "09:00");
  let end = parseTimeToMinutes(employee.shiftEnd, "18:00");
  if (end <= start) end += 24 * 60;
  return Math.max((end - start) / 60, 0) || 8;
}

function monthlyScheduledHours(employee) {
  if (!batchForm.cutoffStart) return 0;

  const date = new Date(`${batchForm.cutoffStart}T00:00:00`);
  if (Number.isNaN(date.getTime())) return 0;

  const workDays = new Set(
    String(employee.workDays || "mon,tue,wed,thu,fri")
      .split(",")
      .map((day) => day.trim().toLowerCase())
      .filter(Boolean)
  );
  const dayKeys = ["sun", "mon", "tue", "wed", "thu", "fri", "sat"];
  const year = date.getFullYear();
  const month = date.getMonth();
  const lastDate = new Date(year, month + 1, 0).getDate();
  let scheduledDays = 0;

  for (let day = 1; day <= lastDate; day += 1) {
    const cursor = new Date(year, month, day);
    if (workDays.has(dayKeys[cursor.getDay()])) scheduledDays += 1;
  }

  return scheduledDays * scheduledHoursPerDay(employee);
}

function calculateEmployeePayroll(employee, attendanceRow) {
  const scheduledHours = Number(attendanceRow?.scheduled_hours || 0);
  const scheduledDays = Number(attendanceRow?.scheduled_days || 0);
  const averageScheduledHours = scheduledDays > 0 ? scheduledHours / scheduledDays : scheduledHoursPerDay(employee);
  const paidLeaveHours = Number(attendanceRow?.leave_days || 0) * averageScheduledHours;
  const paidHours = Number(attendanceRow?.regular_payable_hours || 0) + paidLeaveHours;
  const monthlyHours = monthlyScheduledHours(employee);
  const payType = employee.payType || "monthly";
  const allowanceRatio = scheduledHours > 0 ? Math.min(paidHours / scheduledHours, 1) : 0;

  let basePay = 0;
  if (payType === "hourly") {
    basePay = Number(employee.basePay || 0) * paidHours;
  } else if (payType === "daily") {
    basePay = Number(employee.basePay || 0) * (averageScheduledHours > 0 ? paidHours / averageScheduledHours : 0);
  } else {
    basePay = Number(employee.basePay || 0) * (monthlyHours > 0 ? Math.min(paidHours / monthlyHours, 1) : 0);
  }

  basePay = roundMoney(basePay);
  const allowances = roundMoney(Number(employee.fixedAllowance || 0) * allowanceRatio);
  const sssDeduction = calculateSssEmployeeShare(basePay);
  const philhealthDeduction = calculatePhilhealthEmployeeShare(basePay);
  const pagibigDeduction = calculatePagibigEmployeeShare(basePay);
  const grossPay = roundMoney(basePay + allowances);
  const totalDeductions = roundMoney(sssDeduction + philhealthDeduction + pagibigDeduction);
  const netPay = roundMoney(grossPay - totalDeductions);
  const incompleteLogs = Number(attendanceRow?.incomplete_logs || 0);
  const blocked = incompleteLogs > 0 || scheduledHours <= 0;

  return {
    selected: !blocked,
    finalized: false,
    blocked,
    employeeCode: employee.employeeCode,
    employeeName: employee.name,
    department: employee.department,
    position: employee.position,
    branch: employee.branch,
    basePay,
    allowances,
    sssDeduction,
    philhealthDeduction,
    pagibigDeduction,
    totalDeductions,
    grossPay,
    netPay,
    paidHours: roundMoney(paidHours),
    scheduledHours: roundMoney(scheduledHours),
    presentDays: Number(attendanceRow?.present_days || 0),
    leaveDays: Number(attendanceRow?.leave_days || 0),
    absentDays: Number(attendanceRow?.absent_days || 0),
    incompleteLogs,
    statusLabel: blocked ? "Needs Attendance Fix" : "Ready",
    statusClass: blocked ? "bg-light-danger text-danger" : "bg-light-success text-success",
  };
}

async function fetchEmployees() {
  if (!authStore.accessToken) return;

  const response = await apiRequest("/employees", { token: authStore.accessToken });
  employees.value = (response.items || []).map((employee) => ({
    employeeCode: employee.employee_code,
    name: `${employee.first_name} ${employee.last_name}`,
    department: employee.department,
    position: employee.position,
    branch: employee.branch || "",
    payType: employee.pay_type || "monthly",
    basePay: Number(employee.base_rate || 0),
    fixedAllowance: Number(employee.fixed_allowance || 0),
    workDays: employee.work_days || "mon,tue,wed,thu,fri",
    shiftStart: employee.default_shift_start || "09:00",
    shiftEnd: employee.default_shift_end || "18:00",
  }));
}

function validateBatchDates() {
  if (!batchForm.cutoffStart || !batchForm.cutoffEnd) {
    setAlert("danger", "Cutoff start and cutoff end are required.");
    return false;
  }
  if (new Date(batchForm.cutoffEnd) < new Date(batchForm.cutoffStart)) {
    setAlert("danger", "Cutoff end cannot be earlier than cutoff start.");
    return false;
  }
  return true;
}

async function loadBatch() {
  if (!validateBatchDates()) return;

  isLoadingBatch.value = true;
  try {
    if (!employees.value.length) await fetchEmployees();
    const response = await apiRequest(
      `/attendance/payroll-summary?cutoff_start=${encodeURIComponent(batchForm.cutoffStart)}&cutoff_end=${encodeURIComponent(batchForm.cutoffEnd)}`,
      { token: authStore.accessToken }
    );
    const rowsByEmployee = Object.fromEntries((response.rows || []).map((row) => [row.employee_code, row]));
    batchRows.value = employees.value.map((employee) => calculateEmployeePayroll(employee, rowsByEmployee[employee.employeeCode]));
    setAlert("success", `Batch preview loaded. ${selectedRows.value.length} payroll record(s) are ready to finalize.`);
  } catch (error) {
    if (error instanceof ApiError && error.status === 401) {
      authStore.logout();
      setAlert("danger", "Your session expired. Please sign in again.");
    } else {
      setAlert("danger", "Could not load payroll batch preview. Make sure FastAPI is running.");
    }
  } finally {
    isLoadingBatch.value = false;
  }
}

function toggleAllRows() {
  const shouldSelect = !allSelectableRowsSelected.value;
  batchRows.value.forEach((row) => {
    if (!row.blocked && !row.finalized) row.selected = shouldSelect;
  });
}

function buildPayrollPayload(row) {
  return {
    payroll_run_id: generatePayrollRunId(row.employeeCode),
    cutoff_start: batchForm.cutoffStart,
    cutoff_end: batchForm.cutoffEnd,
    payroll_mode: batchForm.payrollMode,
    payslip_status: "Published",
    employee_code: row.employeeCode,
    employee_name: row.employeeName,
    department: row.department || null,
    position: row.position || null,
    branch: row.branch || null,
    base_pay: row.basePay,
    ot_pay: 0,
    holiday_pay: 0,
    night_diff_pay: 0,
    allowances: row.allowances,
    tax_deduction: 0,
    sss_deduction: row.sssDeduction,
    philhealth_deduction: row.philhealthDeduction,
    pagibig_deduction: row.pagibigDeduction,
    gross_pay: row.grossPay,
    total_deductions: row.totalDeductions,
    net_pay: row.netPay,
    remarks: `Batch ${batchForm.payrollMode} payroll from ${batchForm.cutoffStart} to ${batchForm.cutoffEnd}. ${row.paidHours} paid hour(s), ${row.absentDays} absent day(s), ${row.leaveDays} leave day(s).`,
  };
}

async function finalizeBatch() {
  if (!selectedRows.value.length) {
    setAlert("warning", "Select at least one ready employee before finalizing.");
    return;
  }

  isFinalizing.value = true;
  let savedCount = 0;
  try {
    for (const row of selectedRows.value) {
      await apiRequest("/payroll", {
        method: "POST",
        token: authStore.accessToken,
        body: JSON.stringify(buildPayrollPayload(row)),
      });
      row.finalized = true;
      row.selected = false;
      row.statusLabel = "Published";
      row.statusClass = "bg-light-primary text-primary";
      savedCount += 1;
    }
    setAlert("success", `${savedCount} payroll record(s) finalized and published.`);
  } catch (error) {
    setAlert("danger", error instanceof Error ? error.message : "Batch finalization stopped because one payroll record could not be saved.");
  } finally {
    isFinalizing.value = false;
  }
}

watch(
  () => [batchForm.cutoffStart, batchForm.cutoffEnd, batchForm.payrollMode],
  () => {
    batchRows.value = [];
    setAlert("primary", "Cutoff changed. Load the batch preview again.");
  }
);

onMounted(() => {
  fetchEmployees().catch(() => {
    setAlert("danger", "Could not load employees for payroll batch.");
  });
});
</script>

<style scoped>
.premium-hero {
  border: 1px solid rgba(16, 24, 40, 0.08);
  border-radius: 1.25rem;
  padding: 1.15rem 1.35rem;
  background:
    linear-gradient(135deg, rgba(13, 110, 253, 0.08), rgba(13, 110, 253, 0.02)),
    #fff;
  box-shadow: 0 10px 30px rgba(15, 23, 42, 0.05);
}

.premium-badge {
  display: inline-flex;
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
}

.premium-panel {
  border-radius: 0.85rem;
  overflow: hidden;
}

.premium-panel-body {
  background:
    radial-gradient(circle at top left, rgba(13, 110, 253, 0.05), transparent 35%),
    #fff;
}

.summary-tile {
  border: 1px solid rgba(148, 163, 184, 0.18);
  border-radius: 0.5rem;
  padding: 0.75rem;
  min-height: 74px;
}

.summary-tile small,
.batch-card small {
  color: #64748b;
  display: block;
  margin-bottom: 0.25rem;
}

.summary-tile strong,
.batch-card strong {
  color: #0f172a;
  display: block;
}

.batch-card {
  border: 1px solid rgba(148, 163, 184, 0.2);
  border-radius: 0.5rem;
  margin-bottom: 0.75rem;
  padding: 1rem;
}
</style>
