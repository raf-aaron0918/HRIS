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
                    <span class="text-muted small">Recent present logs</span>
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
                    <span class="text-muted small">Late arrivals</span>
                  </div>
                  <span class="badge bg-light-warning text-warning">Alert</span>
                </div>
              </div>
            </div>
          </div>

          <div class="col-6 col-md-6 col-xl-3">
            <div class="card border-0 shadow-sm h-100 premium-metric">
              <div class="card-body">
                <small class="text-muted d-block mb-2">Corrections</small>
                <div class="d-flex align-items-end justify-content-between gap-2">
                  <div>
                    <h3 class="mb-1">{{ overview.correctionCount }}</h3>
                    <span class="text-muted small">Correction items</span>
                  </div>
                  <span class="badge bg-light-info text-info">Review</span>
                </div>
              </div>
            </div>
          </div>

          <div class="col-6 col-md-6 col-xl-3">
            <div class="card border-0 shadow-sm h-100 premium-metric">
              <div class="card-body">
                <small class="text-muted d-block mb-2">Premium Work</small>
                <div class="d-flex align-items-end justify-content-between gap-2">
                  <div>
                    <h3 class="mb-1">{{ overview.premiumCount }}</h3>
                    <span class="text-muted small">Overtime / rest / holiday</span>
                  </div>
                  <span class="badge bg-light-primary text-primary">Pay</span>
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
                <h5 class="mb-0">Recent Attendance Logs</h5>
                <small class="text-muted">Review live logs, premium work, and correction items in one list.</small>
              </div>

              <div class="d-flex flex-column flex-md-row gap-2 align-items-stretch align-items-md-center flex-grow-1 justify-content-md-end">
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
                      <td>
                        <span class="badge" :class="row.statusClass">{{ row.statusLabel }}</span>
                      </td>
                      <td>{{ row.lateOt }}</td>
                      <td>{{ row.payable }}</td>
                      <td>{{ row.source }}</td>
                      <td class="text-end">
                        <a href="#" class="btn btn-sm btn-outline-primary" @click.prevent="noopView(row)">
                          View
                        </a>
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
              <div v-for="row in filteredAttendanceRows" :key="`mobile-${row.logId}`" class="border rounded-4 p-3 mb-2 shadow-sm premium-mobile-card">
                <div class="d-flex justify-content-between gap-2 align-items-start">
                  <div>
                    <div class="fw-semibold">{{ row.employee }}</div>
                    <div class="small text-muted">{{ row.logId }}</div>
                  </div>
                  <span class="badge" :class="row.statusClass">{{ row.statusLabel }}</span>
                </div>
                <div class="small text-muted mt-2">Shift: {{ row.shift }}</div>
                <div class="small text-muted">Late / OT: {{ row.lateOt }}</div>
                <div class="small text-muted">Payable: {{ row.payable }}</div>
                <div class="small text-muted">Source: {{ row.source }}</div>
              </div>

              <div v-if="!filteredAttendanceRows.length" class="text-center text-muted py-4">
                No attendance log matches the current search or filter.
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from "vue";
import BreadcrumbBar from "@/components/BreadcrumbBar.vue";
import { RouterLink } from "vue-router";
import { apiRequest } from "@/lib/api";
import { useAuthStore } from "@/stores/auth";

const authStore = useAuthStore();

const attendanceRows = ref([]);

const attendanceFilters = [
  { value: "all", label: "All" },
  { value: "late", label: "Late" },
  { value: "correction", label: "Correction" },
  { value: "night", label: "Night Shift" },
  { value: "premium", label: "Premium Work" },
];

const attendanceSearch = ref("");
const activeAttendanceFilter = ref("all");

const overview = computed(() => ({
  presentCount: attendanceRows.value.filter((row) => row.status === "present").length,
  lateCount: attendanceRows.value.filter((row) => row.status === "late").length,
  correctionCount: attendanceRows.value.filter((row) => row.status === "correction").length,
  premiumCount: attendanceRows.value.filter((row) => row.premium === "yes").length,
}));

const filteredAttendanceRows = computed(() => {
  const query = attendanceSearch.value.trim().toLowerCase();

  return attendanceRows.value.filter((row) => {
    const haystack = `${row.logId} ${row.employee} ${row.shift} ${row.statusLabel} ${row.source}`.toLowerCase();
    if (query && !haystack.includes(query)) return false;

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

function normalizeAttendanceRow(log) {
  const status = String(log.status || "saved").toLowerCase();

  return {
    logId: log.log_id,
    employeeId: log.employee_code,
    employee: log.employee_name,
    shift: log.shift_schedule || "Shift",
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

async function fetchAttendanceLogs() {
  if (!authStore.accessToken) return;

  try {
    const response = await apiRequest("/attendance", { token: authStore.accessToken });
    attendanceRows.value = (response.items || []).map(normalizeAttendanceRow);
  } catch {
    attendanceRows.value = [];
  }
}

// Entry form was removed from this page; keep handler safe.
function noopView() {}

onMounted(() => {
  fetchAttendanceLogs();
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
  border-color: rgba(148, 163, 184, 0.18) !important;
  background: linear-gradient(180deg, #fff 0%, #fbfdff 100%);
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
