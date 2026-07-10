<template>
  <div>
    <BreadcrumbBar section="Dashboard" current="Home" />

    <div class="row g-3">
      <div class="col-xl-8">
        <div class="card h-100 border-0 shadow-sm overflow-hidden">
          <div class="card-body p-4 d-flex flex-column justify-content-between h-100">
            <div class="row align-items-center g-4">
              <div class="col-12">
                <span class="badge bg-light-primary text-primary mb-3">HRIS Operations Center</span>
                <h3 class="mb-2">Track people, time, leave, payroll, and reports from one HR dashboard.</h3>
                <p class="text-muted mb-3">
                  This view is focused on the daily work of HR Admins: monitor employee changes, watch attendance issues, review approvals, and prepare payroll-ready data.
                </p>
                <div class="d-flex flex-wrap align-items-center gap-2 mb-4">
                  <RouterLink to="/employees" class="btn btn-primary">Open Employee Master</RouterLink>
                  <RouterLink to="/attendance" class="btn btn-outline-primary">Review Attendance</RouterLink>
                  <RouterLink to="/reports" class="btn btn-outline-secondary">Open Reports</RouterLink>
                </div>
              </div>
            </div>
            <div class="row g-3">
              <div class="col-md-4" v-for="card in heroStats" :key="card.label">
                <div class="border rounded-3 p-3 h-100 bg-light">
                  <small class="text-muted d-block mb-1">{{ card.label }}</small>
                  <strong class="d-block">{{ card.value }}</strong>
                  <span class="text-muted small">{{ card.caption }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="col-xl-4">
        <div class="card h-100 border-0 shadow-sm">
          <div class="card-header d-flex align-items-center justify-content-between">
            <h5 class="mb-0">Approval Queue</h5>
            <span class="badge bg-light-warning text-warning">{{ approvalQueueTotal }} items</span>
          </div>
          <div class="card-body">
            <div v-if="dashboardLoading" class="text-muted small">Loading live dashboard data...</div>
            <div v-else-if="dashboardError" class="alert alert-warning mb-0">
              {{ dashboardError }}
            </div>
            <div v-for="item in approvals" :key="item.label" class="border rounded-3 p-3 mb-3">
              <div class="d-flex justify-content-between align-items-start mb-1">
                <h6 class="mb-0">{{ item.label }}</h6>
                <span class="badge" :class="item.badgeClass">{{ item.count }}</span>
              </div>
              <p class="text-muted mb-0 text-sm">{{ item.caption }}</p>
            </div>
          </div>
        </div>
      </div>

      <div class="col-md-6 col-xl-3" v-for="module in moduleStats" :key="module.title">
        <div class="card h-100">
          <div class="card-body">
            <h6 class="mb-2 f-w-400 text-muted">{{ module.title }}</h6>
            <h4 class="mb-3">
              {{ module.value }}
              <span class="badge" :class="module.badgeClass"><i :class="module.icon"></i> {{ module.badge }}</span>
            </h4>
            <p class="mb-0 text-muted text-sm">{{ module.caption }}</p>
          </div>
        </div>
      </div>

      <div class="col-xl-8">
        <div class="card h-100">
          <div class="card-header d-flex align-items-center justify-content-between">
            <h5 class="mb-0">Quick Actions</h5>
            <span class="text-muted text-sm">Most-used HR tasks</span>
          </div>
          <div class="card-body">
            <div class="row g-3">
              <div class="col-md-6 col-lg-4" v-for="action in quickActions" :key="action.title">
                <RouterLink :to="action.to" class="text-decoration-none">
                  <div class="border rounded-3 p-3 h-100">
                    <div class="d-flex align-items-center justify-content-between mb-2">
                      <h6 class="mb-0 text-dark">{{ action.title }}</h6>
                      <i :class="action.icon"></i>
                    </div>
                    <p class="text-muted mb-0 text-sm">{{ action.caption }}</p>
                  </div>
                </RouterLink>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="col-xl-4">
        <div class="card h-100">
          <div class="card-header">
            <h5 class="mb-0">Important Dates</h5>
          </div>
          <div class="card-body">
            <div v-for="date in importantDates" :key="date.label" class="d-flex align-items-start justify-content-between border-bottom pb-3 mb-3">
              <div>
                <h6 class="mb-1">{{ date.label }}</h6>
                <p class="text-muted mb-0 text-sm">{{ date.caption }}</p>
              </div>
              <span class="badge" :class="date.badgeClass">{{ date.when }}</span>
            </div>
          </div>
        </div>
      </div>

      <div class="col-12">
        <div class="card h-100">
          <div class="card-header d-flex align-items-center justify-content-between">
            <h5 class="mb-0">Recent Activity</h5>
            <RouterLink to="/reports" class="btn btn-sm btn-light-primary">View Reports</RouterLink>
          </div>
          <div class="card-body p-0">
            <div class="table-responsive">
              <table class="table table-hover mb-0">
                <thead>
                  <tr>
                    <th>Activity</th>
                    <th>Employee</th>
                    <th>Module</th>
                    <th>Status</th>
                    <th>Time</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="activity in recentActivity" :key="`${activity.activity}-${activity.time}`">
                    <td>{{ activity.activity }}</td>
                    <td>{{ activity.employee }}</td>
                    <td>{{ activity.module }}</td>
                    <td><span class="badge" :class="activity.badgeClass">{{ activity.status }}</span></td>
                    <td>{{ activity.time }}</td>
                  </tr>
                  <tr v-if="!recentActivity.length">
                    <td colspan="5" class="text-center text-muted py-4">
                      {{ dashboardLoading ? "Loading recent activity..." : "No recent activity to display yet." }}
                    </td>
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
import { computed, onMounted, ref, watch } from "vue";
import { RouterLink } from "vue-router";
import BreadcrumbBar from "@/components/BreadcrumbBar.vue";
import { apiRequest } from "@/lib/api";
import { useAuthStore } from "@/stores/auth";

const authStore = useAuthStore();
const dashboardLoading = ref(false);
const dashboardError = ref("");
const employeeCount = ref(0);
const activeEmployeeCount = ref(0);
const presentTodayCount = ref(0);
const lateTodayCount = ref(0);
const leavePendingCount = ref(0);
const attendanceCorrectionsCount = ref(0);
const payrollExceptionCount = ref(0);
const payrollDraftCount = ref(0);
const payrollPublishedCount = ref(0);
const recentActivities = ref([]);
const payrollCutoffLabel = ref("No payroll cutoff configured yet.");
const payrollCutoffBadge = ref("-");

const heroStats = computed(() => [
  {
    label: "Workforce",
    value: `${activeEmployeeCount.value} active employee${activeEmployeeCount.value === 1 ? "" : "s"}`,
    caption: `${employeeCount.value} total employee${employeeCount.value === 1 ? "" : "s"} on file`,
  },
  {
    label: "Attendance",
    value: `${presentTodayCount.value} present today`,
    caption: `${lateTodayCount.value} late log${lateTodayCount.value === 1 ? "" : "s"} in the latest attendance data`,
  },
  {
    label: "Payroll",
    value: payrollDraftCount.value > 0 ? `${payrollDraftCount.value} draft run${payrollDraftCount.value === 1 ? "" : "s"}` : "No open cutoff",
    caption:
      payrollPublishedCount.value > 0
        ? `${payrollPublishedCount.value} published payroll run${payrollPublishedCount.value === 1 ? "" : "s"}`
        : "Create payroll runs from Payroll",
  },
]);

const approvals = computed(() => [
  {
    label: "Leave Requests",
    count: String(leavePendingCount.value),
    caption:
      leavePendingCount.value > 0
        ? "Leave requests are waiting for approval."
        : "No leave requests waiting for approval.",
    badgeClass: "bg-light-warning text-warning",
  },
  {
    label: "Attendance Corrections",
    count: String(attendanceCorrectionsCount.value),
    caption:
      attendanceCorrectionsCount.value > 0
        ? "Attendance correction requests need supervisor review."
        : "No attendance correction requests need supervisor review.",
    badgeClass: "bg-light-info text-info",
  },
  {
    label: "Payroll Exceptions",
    count: String(payrollExceptionCount.value),
    caption:
      payrollExceptionCount.value > 0
        ? "Payroll exceptions are waiting for review."
        : "No payroll exceptions are waiting for review.",
    badgeClass: "bg-light-danger text-danger",
  },
]);

const moduleStats = computed(() => [
  {
    title: "Employee Master",
    value: String(employeeCount.value),
    badge: employeeCount.value > 0 ? "Live" : "Empty",
    badgeClass: "bg-light-primary border border-primary",
    icon: "ti ti-users",
    caption: "Profiles, status changes, onboarding, offboarding, and document tracking.",
  },
  {
    title: "Attendance Control",
    value: String(presentTodayCount.value + lateTodayCount.value),
    badge: presentTodayCount.value > 0 ? "Live" : "No logs",
    badgeClass: "bg-light-success border border-success",
    icon: "ti ti-clock-check",
    caption: "Shift logs, late cases, undertime, overtime, and correction requests.",
  },
  {
    title: "Leave Management",
    value: String(leavePendingCount.value),
    badge: leavePendingCount.value > 0 ? "Pending" : "None",
    badgeClass: "bg-light-warning border border-warning",
    icon: "ti ti-calendar-event",
    caption: "Balances, leave types, approval flow, cancellations, and payroll impact.",
  },
  {
    title: "Payroll Run",
    value: payrollDraftCount.value > 0 ? "Draft" : "Ready",
    badge: payrollDraftCount.value > 0 ? "Cutoff open" : "No draft",
    badgeClass: "bg-light-danger border border-danger",
    icon: "ti ti-wallet",
    caption: "Compensation, deductions, premiums, and payslip publication are still under review.",
  },
]);

const quickActions = [
  { to: "/employees", title: "Add Employee", icon: "ti ti-user-plus text-primary", caption: "Create a profile and begin onboarding." },
  { to: "/attendance", title: "Attendance Review", icon: "ti ti-clock text-info", caption: "Check late logs, OT, and correction requests." },
  { to: "/leave", title: "Leave Approval", icon: "ti ti-calendar-plus text-warning", caption: "Review leave requests and balances." },
  { to: "/payroll", title: "Run Payroll", icon: "ti ti-cash text-danger", caption: "Review cutoff, deductions, and payroll summary." },
  { to: "/accounts", title: "Add Account", icon: "ti ti-user-cog text-secondary", caption: "Create sign-in access for HRIS users." },
  { to: "/reports", title: "Generate Reports", icon: "ti ti-report-analytics text-success", caption: "Export employee, attendance, leave, and payroll data." },
];

const importantDates = computed(() => [
  {
    label: "Payroll Cutoff End",
    caption: payrollCutoffLabel.value,
    when: payrollCutoffBadge.value,
    badgeClass: payrollDraftCount.value > 0 ? "bg-light-warning text-warning" : "bg-light-secondary text-secondary",
  },
]);

const recentActivity = computed(() => recentActivities.value);
const approvalQueueTotal = computed(() => leavePendingCount.value + attendanceCorrectionsCount.value + payrollExceptionCount.value);

function normalizeEmployeeCount(items) {
  employeeCount.value = items.length;
  activeEmployeeCount.value = items.filter((employee) => (employee.account_status || employee.employment_status) === "Active").length;
}

function normalizeAttendanceSummary(summary, logs) {
  const today = summary?.today || {};
  presentTodayCount.value = Number(today.present || 0);
  lateTodayCount.value = Number(today.late || 0);
  attendanceCorrectionsCount.value = Number(today.corrections || 0);
  recentActivities.value = (logs || []).slice(0, 5).map((log) => ({
    activity: log.status || "Attendance update",
    employee: log.employee_name || log.employee_code || "-",
    module: "Attendance",
    status: log.status || "Saved",
    badgeClass: "bg-light-info text-info",
    time: log.work_date || "-",
  }));
}

function normalizeLeaveSummary(summary, requests) {
  const pending = Number(summary?.pending_requests || 0);
  leavePendingCount.value = pending;
  if (!recentActivities.value.length) {
    recentActivities.value = (requests || []).slice(0, 5).map((request) => ({
      activity: request.leave_type || "Leave request",
      employee: request.employee_name || "-",
      module: "Leave",
      status: request.status || "Draft",
      badgeClass: "bg-light-warning text-warning",
      time: request.start_date || "-",
    }));
  }
}

function normalizePayrollSummary(summary, runs) {
  const recentRuns = runs || [];
  payrollDraftCount.value = recentRuns.filter((run) => String(run.payslip_status || "").toLowerCase() === "draft").length;
  payrollPublishedCount.value = Number(summary?.published_runs || 0);
  payrollExceptionCount.value = recentRuns.filter((run) => String(run.payslip_status || "").toLowerCase() === "exception").length;

  if (recentRuns.length && !recentActivities.value.length) {
    recentActivities.value = recentRuns.slice(0, 5).map((run) => ({
      activity: `Payroll ${run.payslip_status || "Draft"}`,
      employee: run.employee_name || run.employee_code || "-",
      module: "Payroll",
      status: run.payslip_status || "Draft",
      badgeClass: "bg-light-danger text-danger",
      time: `${run.cutoff_start || "-"} to ${run.cutoff_end || "-"}`,
    }));
  }

  if (recentRuns.length) {
    const latestRun = recentRuns[0];
    payrollCutoffLabel.value = `${latestRun.cutoff_start || "-"} to ${latestRun.cutoff_end || "-"}`;
    payrollCutoffBadge.value = latestRun.payslip_status || "Draft";
  }
}

async function loadDashboardData() {
  if (!authStore.accessToken) return;

  dashboardLoading.value = true;
  dashboardError.value = "";

  try {
    const [employees, attendanceSummary, attendanceLogs, leaveSummary, leaveRequests, payrollSummary, payrollRuns] = await Promise.all([
      apiRequest("/employees", { token: authStore.accessToken }),
      apiRequest("/attendance/summary", { token: authStore.accessToken }),
      apiRequest("/attendance", { token: authStore.accessToken }),
      apiRequest("/leave/summary", { token: authStore.accessToken }),
      apiRequest("/leave", { token: authStore.accessToken }),
      apiRequest("/payroll/summary", { token: authStore.accessToken }),
      apiRequest("/payroll", { token: authStore.accessToken }),
    ]);

    normalizeEmployeeCount(employees.items || []);
    normalizeAttendanceSummary(attendanceSummary, attendanceLogs.items || []);
    normalizeLeaveSummary(leaveSummary, leaveRequests.items || []);
    normalizePayrollSummary(payrollSummary, payrollRuns.items || []);
  } catch (error) {
    dashboardError.value = error?.message || "Unable to load dashboard data.";
  } finally {
    dashboardLoading.value = false;
  }
}

onMounted(loadDashboardData);
watch(
  () => authStore.accessToken,
  () => {
    loadDashboardData();
  }
);
</script>
