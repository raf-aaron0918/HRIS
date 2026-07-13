<template>
  <div>
    <BreadcrumbBar section="Dashboard" current="Home" />

    <div class="row g-3">
      <div class="col-12">
        <div class="card border-0 shadow-sm premium-hero">
          <div class="card-body p-4 p-lg-5">
            <div class="d-flex flex-column flex-lg-row justify-content-between align-items-lg-center gap-4">
              <div>
                <span class="badge rounded-pill premium-badge mb-3">HRIS Operations Center</span>
                <h3 class="mb-2 premium-title">Dashboard</h3>
                <p class="text-muted mb-0 premium-subtitle">Quick access to the main HR workflows.</p>
              </div>
              <div class="premium-hero-meta">
                <span class="badge bg-light-success text-success">Live sync</span>
                <span class="text-muted small">Pulled from the HRIS API</span>
              </div>
            </div>
            <div class="row g-3 mt-4">
              <div class="col-6 col-lg-3">
                <div class="premium-metric h-100">
                  <small class="text-muted d-block mb-1">Employees</small>
                  <h4 class="mb-0">{{ employeeCount }}</h4>
                </div>
              </div>
              <div class="col-6 col-lg-3">
                <div class="premium-metric h-100">
                  <small class="text-muted d-block mb-1">Present Today</small>
                  <h4 class="mb-0">{{ presentTodayCount }}</h4>
                  <small class="text-muted">{{ expectedTodayCount }} expected</small>
                </div>
              </div>
              <div class="col-6 col-lg-3">
                <div class="premium-metric h-100">
                  <small class="text-muted d-block mb-1">Pending Leave</small>
                  <h4 class="mb-0">{{ leavePendingCount }}</h4>
                </div>
              </div>
              <div class="col-6 col-lg-3">
                <div class="premium-metric h-100">
                  <small class="text-muted d-block mb-1">Payroll Drafts</small>
                  <h4 class="mb-0">{{ payrollDraftCount }}</h4>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="col-lg-5">
        <div class="card h-100 border-0 shadow-sm premium-panel">
          <div class="card-header d-flex align-items-center justify-content-between premium-panel-header">
            <h5 class="mb-0">Approval Queue</h5>
            <span class="badge bg-light-warning text-warning">{{ approvalQueueTotal }} items</span>
          </div>
          <div class="card-body premium-panel-body">
            <div v-if="dashboardLoading" class="text-muted small">Loading live dashboard data...</div>
            <div v-else-if="dashboardError" class="alert alert-warning mb-0">
              {{ dashboardError }}
            </div>
            <div v-for="item in approvals" :key="item.label" class="premium-item mb-3">
              <div class="d-flex justify-content-between align-items-start mb-1">
                <h6 class="mb-0">{{ item.label }}</h6>
                <span class="badge" :class="item.badgeClass">{{ item.count }}</span>
              </div>
              <div class="text-muted small">{{ item.label === "Leave Requests" ? "Waiting for approval" : item.label === "Attendance Corrections" ? "Needs review" : "Check before payroll close" }}</div>
            </div>
          </div>
        </div>
      </div>

      <div class="col-lg-7">
        <div class="card h-100 border-0 shadow-sm premium-panel">
          <div class="card-header d-flex align-items-center justify-content-between premium-panel-header">
            <h5 class="mb-0">Recent Audit Trail</h5>
            <RouterLink to="/reports" class="btn btn-sm btn-light-primary">View Reports</RouterLink>
          </div>
          <div class="card-body p-0 premium-panel-body">
            <div class="table-responsive">
              <table class="table table-hover align-middle mb-0 premium-table">
                <thead class="table-light">
                  <tr>
                    <th>Activity</th>
                    <th>Employee</th>
                    <th>Module</th>
                    <th>Status</th>
                    <th>Time</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="activity in recentActivity" :key="`${activity.activity}-${activity.time}`" class="premium-table-row">
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
const presentTodayCount = ref(0);
const expectedTodayCount = ref(0);
const leavePendingCount = ref(0);
const attendanceCorrectionsCount = ref(0);
const payrollExceptionCount = ref(0);
const payrollDraftCount = ref(0);
const recentActivities = ref([]);
const auditActivities = ref([]);

const approvals = computed(() => [
  {
    label: "Leave Requests",
    count: String(leavePendingCount.value),
    badgeClass: "bg-light-warning text-warning",
  },
  {
    label: "Attendance Corrections",
    count: String(attendanceCorrectionsCount.value),
    badgeClass: "bg-light-info text-info",
  },
  {
    label: "Payroll Exceptions",
    count: String(payrollExceptionCount.value),
    badgeClass: "bg-light-danger text-danger",
  },
]);

const recentActivity = computed(() => auditActivities.value.length ? auditActivities.value : recentActivities.value);
const approvalQueueTotal = computed(() => leavePendingCount.value + attendanceCorrectionsCount.value + payrollExceptionCount.value);

function normalizeEmployeeCount(items) {
  employeeCount.value = items.length;
}

function normalizeAttendanceSummary(summary, logs) {
  const todayDate = getTodayDateValue();
  const attendanceLogs = logs || [];
  const todaysLogs = attendanceLogs.filter((log) => log.work_date === todayDate);
  const fallbackPresentCount = new Set(
    todaysLogs
      .filter((log) => isPresentAttendanceStatus(log.status))
      .map((log) => getAttendanceIdentityKey(log))
      .filter(Boolean)
  ).size;

  expectedTodayCount.value = Number(summary?.today?.expected || 0);
  presentTodayCount.value = Math.max(Number(summary?.today?.present || 0), fallbackPresentCount);
  attendanceCorrectionsCount.value = todaysLogs.filter(
    (log) => String(log.status || "").toLowerCase().includes("correction") || String(log.log_action || "").toLowerCase() === "correction"
  ).length;
  recentActivities.value = (logs || []).slice(0, 5).map((log) => ({
    activity: normalizeAttendanceStatusLabel(log.status),
    employee: log.employee_name || log.employee_code || "-",
    module: "Attendance",
    status: normalizeAttendanceStatusLabel(log.status),
    badgeClass: "bg-light-info text-info",
    time: log.work_date || "-",
  }));
}

function normalizeAttendanceStatusLabel(statusValue) {
  const rawStatus = String(statusValue || "Saved");
  const normalizedStatus = rawStatus.toLowerCase();

  if (normalizedStatus.includes("for payroll review") || normalizedStatus.includes("approved") || normalizedStatus.includes("saved")) {
    return "Present";
  }

  if (normalizedStatus.includes("pending correction")) {
    return "Correction";
  }

  return rawStatus;
}

function isPresentAttendanceStatus(statusValue) {
  const normalizedStatus = normalizeAttendanceStatusLabel(statusValue).toLowerCase();
  return (
    normalizedStatus.includes("present") ||
    normalizedStatus.includes("late") ||
    normalizedStatus.includes("undertime")
  );
}

function getAttendanceIdentityKey(log) {
  const employeeCode = String(log.employee_code || "").trim();
  if (employeeCode) return `code:${employeeCode}`;

  const employeeName = String(log.employee_name || "").trim().toLowerCase().replace(/\s+/g, " ");
  if (employeeName) return `name:${employeeName}`;

  const logId = String(log.log_id || "").trim();
  return logId ? `log:${logId}` : "";
}

function getTodayDateValue() {
  const today = new Date();
  const year = today.getFullYear();
  const month = String(today.getMonth() + 1).padStart(2, "0");
  const day = String(today.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
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

}

function normalizeAuditLogs(logs) {
  auditActivities.value = (logs || []).slice(0, 8).map((log) => ({
    activity: `${log.action} ${log.record_id}`,
    employee: log.actor || "-",
    module: log.module || "Audit",
    status: log.actor_role || "Recorded",
    badgeClass: "bg-light-primary text-primary",
    time: log.created_at || "-",
  }));
}

async function loadDashboardData() {
  if (!authStore.accessToken) return;

  dashboardLoading.value = true;
  dashboardError.value = "";

  try {
    const [employees, attendanceSummary, attendanceLogs, leaveSummary, leaveRequests, payrollSummary, payrollRuns, auditLogs] = await Promise.all([
      apiRequest("/employees", { token: authStore.accessToken }),
      apiRequest(`/attendance/summary?work_date=${encodeURIComponent(getTodayDateValue())}`, { token: authStore.accessToken }),
      apiRequest("/attendance", { token: authStore.accessToken }),
      apiRequest("/leave/summary", { token: authStore.accessToken }),
      apiRequest("/leave", { token: authStore.accessToken }),
      apiRequest("/payroll/summary", { token: authStore.accessToken }),
      apiRequest("/payroll", { token: authStore.accessToken }),
      apiRequest("/audit-logs?limit=8", { token: authStore.accessToken }).catch(() => ({ items: [] })),
    ]);

    normalizeEmployeeCount(employees.items || []);
    normalizeAttendanceSummary(attendanceSummary, attendanceLogs.items || []);
    normalizeLeaveSummary(leaveSummary, leaveRequests.items || []);
    normalizePayrollSummary(payrollSummary, payrollRuns.items || []);
    normalizeAuditLogs(auditLogs.items || []);
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

<style scoped>
.premium-hero {
  background:
    radial-gradient(circle at top right, rgba(78, 115, 223, 0.14), transparent 28%),
    linear-gradient(180deg, #ffffff 0%, #fbfcff 100%);
  border: 1px solid rgba(15, 23, 42, 0.06);
  border-radius: 1.25rem;
}

.premium-badge {
  background: rgba(59, 130, 246, 0.12);
  color: #2563eb;
  border: 1px solid rgba(59, 130, 246, 0.16);
  padding: 0.45rem 0.8rem;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}

.premium-title {
  letter-spacing: -0.03em;
  font-weight: 700;
}

.premium-subtitle {
  max-width: 34rem;
}

.premium-hero-meta {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 0.45rem;
  min-width: 12rem;
}

.premium-metric {
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid rgba(15, 23, 42, 0.08);
  border-radius: 1rem;
  padding: 1rem 1rem 1.05rem;
  box-shadow: 0 10px 30px rgba(15, 23, 42, 0.04);
}

.premium-panel {
  border-radius: 1.15rem;
  border: 1px solid rgba(15, 23, 42, 0.06) !important;
}

.premium-panel-header {
  background: rgba(248, 250, 252, 0.9);
  border-bottom: 1px solid rgba(15, 23, 42, 0.06);
  padding: 1rem 1.25rem;
}

.premium-panel-body {
  padding: 1.25rem;
}

.premium-item {
  background: linear-gradient(180deg, #ffffff 0%, #fbfcfe 100%);
  border: 1px solid rgba(15, 23, 42, 0.08);
  border-radius: 0.95rem;
  padding: 1rem 1rem 0.95rem;
  box-shadow: 0 8px 20px rgba(15, 23, 42, 0.03);
}

.premium-table thead th {
  font-size: 0.78rem;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: #64748b;
  border-bottom: 1px solid rgba(15, 23, 42, 0.08);
}

.premium-table tbody td {
  padding-top: 1rem;
  padding-bottom: 1rem;
}

.premium-table-row {
  transition: background-color 0.2s ease;
}

.premium-table-row:hover {
  background: rgba(59, 130, 246, 0.03);
}

@media (max-width: 991.98px) {
  .premium-panel-body {
    padding: 1rem;
  }

  .premium-hero-meta {
    min-width: 0;
  }
}
</style>
