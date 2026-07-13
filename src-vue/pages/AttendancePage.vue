<template>
  <div>
    <BreadcrumbBar section="HR Modules" current="Time & Attendance" />

    <div class="premium-hero mb-4">
      <div class="d-flex flex-column flex-md-row justify-content-between align-items-md-center gap-3">
        <div>
          <div class="premium-badge mb-2">HR Modules</div>
          <h4 class="mb-1 premium-title">Time & Attendance</h4>
          <p class="mb-0 premium-subtitle">Monitor attendance, premium work, and correction items in one polished view.</p>
        </div>
      </div>
    </div>

    <div class="row g-3">
      <div class="col-lg-12">
        <!-- Summary (same layout style as Employee Master: 4 cards w/ labels + badge) -->
        <div class="row g-3 mb-3">
          <div class="col-6 col-md-6 col-xl-3">
            <div class="card border-0 shadow-sm h-100 premium-metric">
              <div class="card-body">
                <small class="text-muted d-block mb-2">Present</small>
                <div class="d-flex align-items-end justify-content-between gap-2">
                  <div>
                    <h3 class="mb-1">{{ overview.presentCount }}</h3>
                    <span class="text-muted small">Present on selected day</span>
                  </div>
                  <span class="badge bg-light-success text-success">OK</span>
                </div>
              </div>
            </div>
          </div>

          <div class="col-6 col-md-6 col-xl-3">
            <div class="card border-0 shadow-sm h-100 premium-metric">
              <div class="card-body">
                <small class="text-muted d-block mb-2">Late</small>
                <div class="d-flex align-items-end justify-content-between gap-2">
                  <div>
                    <h3 class="mb-1">{{ overview.lateCount }}</h3>
                    <span class="text-muted small">Late on selected day</span>
                  </div>
                  <span class="badge bg-light-warning text-warning">Alert</span>
                </div>
              </div>
            </div>
          </div>

          <div class="col-6 col-md-6 col-xl-3">
            <div class="card border-0 shadow-sm h-100 premium-metric">
              <div class="card-body">
                <small class="text-muted d-block mb-2">On Leave</small>
                <div class="d-flex align-items-end justify-content-between gap-2">
                  <div>
                    <h3 class="mb-1">{{ overview.onLeaveCount }}</h3>
                    <span class="text-muted small">Approved leave today</span>
                  </div>
                  <span class="badge bg-light-info text-info">Leave</span>
                </div>
              </div>
            </div>
          </div>

          <div class="col-6 col-md-6 col-xl-3">
            <div class="card border-0 shadow-sm h-100 premium-metric">
              <div class="card-body">
                <small class="text-muted d-block mb-2">Absent</small>
                <div class="d-flex align-items-end justify-content-between gap-2">
                  <div>
                    <h3 class="mb-1">{{ overview.absentCount }}</h3>
                    <span class="text-muted small">Scheduled but no log</span>
                  </div>
                  <span class="badge bg-light-danger text-danger">Check</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="col-lg-12">
        <div class="card border-0 shadow-sm premium-panel">
          <div class="card-header bg-white border-bottom-0 pt-4 pb-0 premium-panel-header">
            <div class="d-flex flex-column flex-md-row justify-content-between align-items-md-center gap-3">
              <div>
                <h5 class="mb-0">Daily Attendance Logs</h5>
                <small class="text-muted">Review attendance for the selected day so you can quickly see who is present.</small>
                <div class="text-muted small mt-1">{{ overview.expectedCount }} expected employees</div>
              </div>

              <div class="d-flex flex-column flex-md-row gap-2 align-items-stretch align-items-md-center flex-grow-1 justify-content-md-end">
                <input
                  v-model="attendanceDate"
                  type="date"
                  class="form-control premium-date-filter"
                />

                <div class="input-group w-100 premium-search">
                  <span class="input-group-text bg-light border-end-0">
                    <i class="ti ti-search"></i>
                  </span>
                  <input
                    v-model="attendanceSearch"
                    type="search"
                    class="form-control border-start-0 ps-0 bg-light"
                    placeholder="Search employee or log"
                  />
                </div>

                <RouterLink to="/attendance/new" class="btn btn-primary d-flex align-items-center justify-content-center gap-2 text-nowrap">
                  <i class="ti ti-user-plus"></i> New Attendance
                </RouterLink>

                <span class="badge bg-light-secondary text-secondary premium-pill">{{ attendanceCountLabel }}</span>
              </div>
            </div>
          </div>

          <div class="card-body p-0 premium-panel-body">
            <div class="px-3 pt-3 d-flex flex-nowrap overflow-auto gap-2 pb-2 mobile-filter-scroll premium-filter-row">
              <button
                v-for="filter in attendanceFilters"
                :key="filter.value"
                type="button"
                class="btn btn-sm rounded-pill px-3"
                :class="activeAttendanceFilter === filter.value ? 'btn-primary' : 'btn-outline-secondary'"
                @click="activeAttendanceFilter = filter.value"
              >
                {{ filter.label }}
              </button>
            </div>

            <div class="d-none d-md-block">
              <div class="table-responsive mt-3">
                <table class="table table-hover align-middle mb-0 premium-table">
                  <thead class="table-light">
                    <tr>
                      <th>Log ID</th>
                      <th>Employee</th>
                      <th>Date</th>
                      <th>Shift</th>
                      <th>Status</th>
                      <th>Variance</th>
                      <th>Payable</th>
                      <th class="text-end">Action</th>
                    </tr>
                  </thead>

                  <tbody>
                    <tr v-for="row in filteredAttendanceRows" :key="row.logId">
                      <td>{{ row.logId }}</td>
                      <td>{{ row.employee }}</td>
                      <td>{{ row.workDate }}</td>
                      <td>{{ row.shift }}</td>
                      <td>
                        <span class="badge" :class="row.statusClass">{{ row.statusLabel }}</span>
                        <span v-if="row.isCorrection" class="badge bg-light-info text-info ms-1">Corrected</span>
                      </td>
                      <td>{{ row.lateOt }}</td>
                      <td>{{ row.payable }}</td>
                      <td class="text-end">
                        <div class="d-inline-flex gap-2">
                          <button type="button" class="btn btn-sm btn-outline-primary" @click="openAttendanceDetail(row)">
                            View
                          </button>
                          <button
                            v-if="!String(row.logId || '').startsWith('ROSTER-')"
                            type="button"
                            class="btn btn-sm btn-primary"
                            @click="editAttendanceRow(row)"
                          >
                            Edit
                          </button>
                        </div>
                      </td>
                    </tr>

                    <tr v-if="!filteredAttendanceRows.length">
                      <td colspan="8" class="text-center text-muted py-4">
                        No attendance log matches the current search or filter.
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>

            <div class="d-md-none px-3 pb-3">
              <div v-for="row in filteredAttendanceRows" :key="`mobile-${row.logId}`" class="border p-3 mb-2 shadow-sm premium-mobile-card">
                <div class="d-flex justify-content-between gap-2 align-items-start">
                  <div>
                    <div class="fw-semibold">{{ row.employee }}</div>
                    <div class="small text-muted">{{ row.logId }}</div>
                  </div>
                  <span class="badge" :class="row.statusClass">{{ row.statusLabel }}</span>
                </div>
                <div class="small text-muted mt-2">Shift: {{ row.shift }}</div>
                <div class="small text-muted">Date: {{ row.workDate }}</div>
                <div v-if="row.isCorrection" class="small text-info">Corrected attendance entry</div>
                <div class="small text-muted">Variance: {{ row.lateOt }}</div>
                <div class="small text-muted">Payable: {{ row.payable }}</div>
                <div class="d-flex gap-2 mt-3">
                  <button type="button" class="btn btn-sm btn-outline-primary" @click="openAttendanceDetail(row)">
                    View
                  </button>
                  <button
                    v-if="!String(row.logId || '').startsWith('ROSTER-')"
                    type="button"
                    class="btn btn-sm btn-primary"
                    @click="editAttendanceRow(row)"
                  >
                    Edit
                  </button>
                </div>
              </div>

              <div v-if="!filteredAttendanceRows.length" class="text-center text-muted py-4">
                No attendance log matches the current search or filter.
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="selectedAttendanceRow" class="premium-modal-backdrop" @click="closeAttendanceDetail">
      <div class="premium-modal-card" @click.stop>
        <div class="d-flex justify-content-between align-items-start gap-3 mb-3">
          <div>
            <h5 class="mb-1">Attendance Details</h5>
            <div class="text-muted small">{{ selectedAttendanceRow.employee }} · {{ selectedAttendanceRow.logId }}</div>
          </div>
          <button type="button" class="btn btn-sm btn-outline-secondary" @click="closeAttendanceDetail">Close</button>
        </div>

        <div class="row g-3">
          <div class="col-md-6">
            <div class="premium-detail-item">
              <div class="premium-detail-label">Status</div>
              <div class="premium-detail-value">
                <span class="badge" :class="selectedAttendanceRow.statusClass">{{ selectedAttendanceRow.statusLabel }}</span>
              </div>
            </div>
          </div>
          <div class="col-md-6">
            <div class="premium-detail-item">
              <div class="premium-detail-label">Date</div>
              <div class="premium-detail-value">{{ selectedAttendanceRow.workDate }}</div>
            </div>
          </div>
          <div class="col-md-6">
            <div class="premium-detail-item">
              <div class="premium-detail-label">Employee Code</div>
              <div class="premium-detail-value">{{ selectedAttendanceRow.employeeId || "-" }}</div>
            </div>
          </div>
          <div class="col-md-6">
            <div class="premium-detail-item">
              <div class="premium-detail-label">Shift</div>
              <div class="premium-detail-value">{{ selectedAttendanceRow.shift }}</div>
            </div>
          </div>
          <div class="col-md-6">
            <div class="premium-detail-item">
              <div class="premium-detail-label">Clock In</div>
              <div class="premium-detail-value">{{ selectedAttendanceRow.raw?.clock_in || "-" }}</div>
            </div>
          </div>
          <div class="col-md-6">
            <div class="premium-detail-item">
              <div class="premium-detail-label">Clock Out</div>
              <div class="premium-detail-value">{{ selectedAttendanceRow.raw?.clock_out || "-" }}</div>
            </div>
          </div>
          <div class="col-md-6">
            <div class="premium-detail-item">
              <div class="premium-detail-label">Break Out</div>
              <div class="premium-detail-value">{{ selectedAttendanceRow.raw?.break_out || "-" }}</div>
            </div>
          </div>
          <div class="col-md-6">
            <div class="premium-detail-item">
              <div class="premium-detail-label">Break In</div>
              <div class="premium-detail-value">{{ selectedAttendanceRow.raw?.break_in || "-" }}</div>
            </div>
          </div>
          <div class="col-md-6">
            <div class="premium-detail-item">
              <div class="premium-detail-label">Variance</div>
              <div class="premium-detail-value">{{ selectedAttendanceRow.lateOt }}</div>
            </div>
          </div>
          <div class="col-md-6">
            <div class="premium-detail-item">
              <div class="premium-detail-label">Payable Hours</div>
              <div class="premium-detail-value">{{ selectedAttendanceRow.payable }}</div>
            </div>
          </div>
          <div class="col-md-6">
            <div class="premium-detail-item">
              <div class="premium-detail-label">Entry Type</div>
              <div class="premium-detail-value">{{ selectedAttendanceRow.isCorrection ? "Correction" : "Original Log" }}</div>
            </div>
          </div>
          <div class="col-md-6">
            <div class="premium-detail-item">
              <div class="premium-detail-label">Premium Work</div>
              <div class="premium-detail-value">{{ selectedAttendanceRow.premium === "yes" ? "Yes" : "No" }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref, watch } from "vue";
import BreadcrumbBar from "@/components/BreadcrumbBar.vue";
import { RouterLink, useRouter } from "vue-router";
import { apiRequest } from "@/lib/api";
import { useAuthStore } from "@/stores/auth";

const authStore = useAuthStore();
const router = useRouter();

const attendanceRows = ref([]);
const rosterRows = ref([]);
const attendanceDate = ref(getTodayDateValue());

const attendanceFilters = [
  { value: "all", label: "All" },
  { value: "late", label: "Late" },
  { value: "incomplete", label: "Incomplete" },
  { value: "on_leave", label: "On Leave" },
  { value: "absent", label: "Absent" },
  { value: "correction", label: "Correction" },
  { value: "night", label: "Night Shift" },
  { value: "premium", label: "Premium Work" },
];

const attendanceSearch = ref("");
const activeAttendanceFilter = ref("all");
const selectedAttendanceRow = ref(null);

const dayAttendanceRows = computed(() =>
  [
    ...attendanceRows.value.filter((row) => !attendanceDate.value || row.workDate === attendanceDate.value),
    ...rosterRows.value.filter((row) => !attendanceDate.value || row.workDate === attendanceDate.value),
  ]
);

const overview = computed(() => ({
  expectedCount: dayAttendanceRows.value.filter((row) => row.isExpected).length,
  presentCount: dayAttendanceRows.value.filter((row) => row.isPresent).length,
  lateCount: dayAttendanceRows.value.filter((row) => row.status.includes("late")).length,
  onLeaveCount: dayAttendanceRows.value.filter((row) => row.status === "on leave").length,
  absentCount: dayAttendanceRows.value.filter((row) => row.status === "absent").length,
}));

const filteredAttendanceRows = computed(() => {
  const query = attendanceSearch.value.trim().toLowerCase();

  return dayAttendanceRows.value.filter((row) => {
    const haystack = `${row.logId} ${row.employee} ${row.workDate} ${row.shift} ${row.statusLabel}`.toLowerCase();
    if (query && !haystack.includes(query)) return false;

    if (activeAttendanceFilter.value === "all") return true;
    if (activeAttendanceFilter.value === "late") return row.status.includes("late");
    if (activeAttendanceFilter.value === "incomplete") return row.status.includes("incomplete");
    if (activeAttendanceFilter.value === "on_leave") return row.status === "on leave";
    if (activeAttendanceFilter.value === "absent") return row.status === "absent";
    if (activeAttendanceFilter.value === "correction") return row.isCorrection;
    if (activeAttendanceFilter.value === "night") return row.shiftFilter === "night";
    if (activeAttendanceFilter.value === "premium") return row.premium === "yes";

    return true;
  });
});

const attendanceCountLabel = computed(() => {
  const count = filteredAttendanceRows.value.length;
  return `${count} record${count === 1 ? "" : "s"}`;
});

function normalizeAttendanceRow(log) {
  const rawStatus = String(log.status || "saved");
  const status = rawStatus.toLowerCase();
  const isCorrection = String(log.log_action || "").toLowerCase() === "correction";
  let statusLabel = rawStatus || "Saved";

  if (status.includes("for payroll review") || status.includes("approved") || status.includes("saved")) {
    statusLabel = "Present";
  } else if (status.includes("pending correction")) {
    statusLabel = "Correction";
  }

  const isPresent =
    status.includes("present") ||
    status.includes("saved") ||
    status.includes("late") ||
    status.includes("undertime") ||
    status.includes("overtime") ||
    status.includes("night differential") ||
    status.includes("rest day work") ||
    status.includes("holiday work");

  return {
    logId: log.log_id,
    employeeId: log.employee_code,
    employee: log.employee_name,
    workDate: log.work_date,
    shift: log.shift_schedule || "Shift",
    status,
    isCorrection,
    isExpected: true,
    isPresent,
    shiftFilter: log.shift_schedule === "night" ? "night" : "day",
    premium: log.rest_day_work === "yes" || log.holiday_work === "yes" ? "yes" : "no",
    statusLabel,
    statusClass:
      status.includes("late")
        ? "bg-light-warning text-warning"
        : status.includes("undertime")
          ? "bg-light-danger text-danger"
        : status.includes("incomplete") || status.includes("invalid")
          ? "bg-light-danger text-danger"
        : status.includes("correction")
          ? "bg-light-info text-info"
          : status.includes("overtime") || status.includes("night differential") || status.includes("rest day work") || status.includes("holiday work")
            ? "bg-light-info text-info"
          : isPresent
            ? "bg-light-success text-success"
            : "bg-light-primary text-primary",
    lateOt: [
      Number(log.late_minutes || 0) ? `${Number(log.late_minutes)}m late` : "",
      Number(log.undertime_minutes || 0) ? `${Number(log.undertime_minutes)}m undertime` : "",
      Number(log.overtime_minutes || 0) ? `${Number(log.overtime_minutes)}m OT` : "",
    ].filter(Boolean).join(" / ") || "On schedule",
    payable: `${Number(log.payable_hours || 0).toFixed(2)} hrs`,
    raw: log,
  };
}

function normalizeRosterRow(row) {
  const status = String(row.status || "Absent").toLowerCase();
  const isOnLeave = status === "on leave";
  const leaveType = row.leave_type || "Approved leave";

  return {
    logId: `ROSTER-${row.employee_code}`,
    employeeId: row.employee_code,
    employee: row.employee_name,
    workDate: row.work_date,
    shift: row.shift_schedule || "Shift",
    status,
    isCorrection: false,
    isExpected: true,
    isPresent: false,
    shiftFilter: row.shift_schedule === "night" ? "night" : "day",
    premium: "no",
    statusLabel: isOnLeave ? `On Leave (${leaveType})` : "Absent",
    statusClass: isOnLeave ? "bg-light-info text-info" : "bg-light-danger text-danger",
    lateOt: isOnLeave ? leaveType : "No attendance log",
    payable: "0.00 hrs",
    raw: row,
  };
}

async function fetchAttendanceData() {
  if (!authStore.accessToken) return;

  try {
    const [logsResponse, summaryResponse] = await Promise.all([
      apiRequest("/attendance", { token: authStore.accessToken }),
      apiRequest(`/attendance/summary?work_date=${encodeURIComponent(attendanceDate.value)}`, { token: authStore.accessToken }),
    ]);
    attendanceRows.value = (logsResponse.items || []).map(normalizeAttendanceRow);
    rosterRows.value = (summaryResponse.daily_roster || [])
      .filter((row) => String(row.status || "").toLowerCase() !== "logged")
      .map(normalizeRosterRow);
  } catch {
    attendanceRows.value = [];
    rosterRows.value = [];
  }
}

function openAttendanceDetail(row) {
  selectedAttendanceRow.value = row;
}

function closeAttendanceDetail() {
  selectedAttendanceRow.value = null;
}

function editAttendanceRow(row) {
  if (!row?.raw?.log_id) return;
  closeAttendanceDetail();
  router.push(`/attendance/${encodeURIComponent(row.raw.log_id)}/edit`);
}

function getTodayDateValue() {
  const today = new Date();
  const year = today.getFullYear();
  const month = String(today.getMonth() + 1).padStart(2, "0");
  const day = String(today.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
}

onMounted(() => {
  fetchAttendanceData();
});

watch(attendanceDate, () => {
  fetchAttendanceData();
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

.premium-metric {
  border-radius: 1.1rem;
  border: 1px solid rgba(16, 24, 40, 0.06);
  background: linear-gradient(180deg, #ffffff 0%, #fbfdff 100%);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.premium-metric:hover {
  transform: translateY(-2px);
  box-shadow: 0 14px 30px rgba(15, 23, 42, 0.08) !important;
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

.premium-search .input-group-text,
.premium-search .form-control {
  border-color: rgba(148, 163, 184, 0.22);
}

.premium-date-filter {
  min-width: 180px;
  border-color: rgba(148, 163, 184, 0.22);
}

.premium-date-filter:focus {
  box-shadow: none;
  border-color: #0d6efd;
}

.premium-search .form-control:focus {
  box-shadow: none;
  border-color: #0d6efd;
}

.premium-pill {
  align-self: center;
  padding: 0.55rem 0.8rem;
  border-radius: 999px;
}

.premium-filter-row {
  scrollbar-width: thin;
}

.premium-filter-row .btn {
  white-space: nowrap;
}

.premium-table thead th {
  color: #475569;
  font-size: 0.78rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  border-bottom-color: rgba(148, 163, 184, 0.2);
}

.premium-table tbody td {
  padding-top: 1rem;
  padding-bottom: 1rem;
}

.premium-mobile-card {
  border-radius: 0;
  border-color: rgba(148, 163, 184, 0.18) !important;
  background: linear-gradient(180deg, #fff 0%, #fbfdff 100%);
}

.premium-modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.48);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
  z-index: 1080;
}

.premium-modal-card {
  width: min(760px, 100%);
  max-height: calc(100vh - 2rem);
  overflow-y: auto;
  background: #fff;
  border-radius: 0;
  padding: 1.25rem;
  box-shadow: 0 24px 60px rgba(15, 23, 42, 0.24);
}

.premium-detail-item {
  border: 1px solid rgba(148, 163, 184, 0.18);
  background: #fff;
  padding: 0.9rem 1rem;
}

.premium-detail-label {
  color: #64748b;
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  margin-bottom: 0.35rem;
}

.premium-detail-value {
  color: #0f172a;
  word-break: break-word;
}

@media (max-width: 767.98px) {
  .premium-hero {
    padding: 1rem 1.1rem;
    border-radius: 1.15rem;
  }

  .premium-panel-header {
    padding-top: 1.1rem !important;
  }

  .premium-modal-card {
    padding: 1rem;
  }
}
</style>
