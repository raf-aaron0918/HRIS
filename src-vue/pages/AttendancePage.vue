<template>
  <div>
    <BreadcrumbBar section="HR Modules" current="Time & Attendance" />

    <div class="row g-3 mb-4">
      <div class="col-12 d-flex flex-column flex-md-row justify-content-between align-items-md-center gap-3">
        <div class="d-flex align-items-center gap-2">
          <h5 class="mb-0">Time & Attendance</h5>
        </div>
      </div>
    </div>

    <div class="row g-3">
      <div class="col-lg-12">
        <!-- Summary (same layout style as Employee Master: 4 cards w/ labels + badge) -->
        <div class="row g-3 mb-3">
          <div class="col-6 col-md-6 col-xl-3">
            <div class="card border-0 shadow-sm h-100">
              <div class="card-body">
                <small class="text-muted d-block mb-2">Present</small>
                <div class="d-flex align-items-end justify-content-between">
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
            <div class="card border-0 shadow-sm h-100">
              <div class="card-body">
                <small class="text-muted d-block mb-2">Late</small>
                <div class="d-flex align-items-end justify-content-between">
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
            <div class="card border-0 shadow-sm h-100">
              <div class="card-body">
                <small class="text-muted d-block mb-2">Corrections</small>
                <div class="d-flex align-items-end justify-content-between">
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
            <div class="card border-0 shadow-sm h-100">
              <div class="card-body">
                <small class="text-muted d-block mb-2">Premium Work</small>
                <div class="d-flex align-items-end justify-content-between">
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
        <div class="card border-0 shadow-sm">
          <div class="card-header bg-white border-bottom-0 pt-4 pb-0">
            <div class="d-flex flex-column flex-md-row justify-content-between align-items-md-center gap-3">
              <div>
                <h5 class="mb-0">Recent Attendance Logs</h5>
                <small class="text-muted">Review live logs, premium work, and correction items in one list.</small>
              </div>

              <div class="d-flex gap-2 align-items-center">
                <div class="input-group" style="max-width: 300px;">
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

                <RouterLink
                  to="/attendance/new"
                  class="btn btn-primary d-flex align-items-center gap-2 text-nowrap"
                >
                  <i class="ti ti-user-plus"></i> New Attendance
                </RouterLink>

                <span class="badge bg-light-secondary text-secondary">{{ attendanceCountLabel }}</span>
              </div>
            </div>
          </div>

          <div class="card-body p-0">
            <div class="px-3 pt-3 d-flex flex-nowrap overflow-auto gap-2 pb-2 mobile-filter-scroll">
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

            <div class="table-responsive mt-3">
              <table class="table table-hover align-middle mb-0">
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
