<template>
  <div class="me-auto topbar-start">
    <div class="topbar-left-controls">
      <button type="button" class="topbar-sidebar-toggle" aria-label="Toggle sidebar" @click="$emit('toggleSidebar')">
        <i class="ti ti-menu-2"></i>
      </button>
      <form class="header-search topbar-search d-none d-md-flex">
        <i class="ti ti-search icon-search"></i>
        <input type="search" class="form-control border-0 shadow-none" placeholder="Search here..." />
      </form>
    </div>
  </div>
  <div class="ms-auto">
    <ul class="list-unstyled">
      <li class="dropdown pc-h-item">
        <a class="pc-head-link dropdown-toggle arrow-none me-0 notification-trigger" data-bs-toggle="dropdown" href="#" role="button" @click="markNotificationsViewed">
          <i class="ti ti-mail"></i>
          <span v-if="notificationCount" class="badge rounded-pill bg-danger pc-h-badge">{{ notificationCount }}</span>
        </a>
        <div class="dropdown-menu dropdown-notification dropdown-menu-end pc-h-dropdown">
          <div class="dropdown-header d-flex align-items-center justify-content-between">
            <h5 class="m-0">Notifications</h5>
            <a href="#!" class="pc-head-link bg-transparent"><i class="ti ti-x text-danger"></i></a>
          </div>
          <div class="dropdown-divider"></div>
          <div class="dropdown-header px-0 text-wrap header-notification-scroll position-relative" style="max-height: calc(100vh - 215px)">
            <div v-if="notificationsLoading" class="px-3 py-3 text-muted small">Loading notifications...</div>
            <div v-else-if="notificationsError" class="px-3 py-3 text-danger small">{{ notificationsError }}</div>
            <div v-else-if="!notifications.length" class="px-3 py-3 text-muted small">No notifications right now.</div>
            <div v-else class="list-group list-group-flush w-100">
              <a
                v-for="item in notifications"
                :key="`${item.title}-${item.time}`"
                href="#"
                class="list-group-item list-group-item-action"
                @click.prevent="goToNotification(item)"
              >
                <div class="d-flex">
                  <div class="flex-shrink-0">
                    <div class="user-avtar notification-avatar" :class="item.avatarClass">
                      <i :class="item.icon"></i>
                    </div>
                  </div>
                  <div class="flex-grow-1 ms-1">
                    <span class="float-end text-muted">{{ item.time }}</span>
                    <p class="text-body mb-1">{{ item.title }}</p>
                    <span class="text-muted">{{ item.subtitle }}</span>
                  </div>
                </div>
              </a>
            </div>
          </div>
        </div>
      </li>
      <li class="dropdown pc-h-item header-user-profile">
        <a class="pc-head-link dropdown-toggle arrow-none me-0" data-bs-toggle="dropdown" href="#" role="button">
          <img :src="avatar2" alt="user-image" class="user-avtar" />
          <span>{{ displayName }}</span>
        </a>
        <div class="dropdown-menu dropdown-user-profile dropdown-menu-end pc-h-dropdown">
          <div class="dropdown-header">
            <div class="d-flex mb-1">
              <div class="flex-shrink-0">
                <img :src="avatar2" alt="user-image" class="user-avtar wid-35" />
              </div>
              <div class="flex-grow-1 ms-3">
                <h6 class="mb-1">{{ displayName }}</h6>
                <span>{{ displayRole }}</span>
              </div>
            </div>
          </div>
          <div class="px-3 pb-3">
            <a href="#" class="dropdown-item" @click.prevent="handleLogout">
              <i class="ti ti-power"></i>
              <span>Logout</span>
            </a>
          </div>
        </div>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { computed, onMounted, ref, watch } from "vue";
import { useRouter } from "vue-router";
import { ApiError, apiRequest } from "@/lib/api";
import { useAuthStore } from "@/stores/auth";

import avatar2 from "../../src/assets/images/user/avatar-2.jpg";

defineEmits(["toggleSidebar"]);
const router = useRouter();
const authStore = useAuthStore();
const notifications = ref([]);
const notificationsLoading = ref(false);
const notificationsError = ref("");
const readNotificationKeys = ref(new Set());

const displayName = computed(() => authStore.currentUser?.full_name || "HRIS User");
const displayRole = computed(() => authStore.currentUser?.role || "Authorized User");
const notificationCount = computed(
  () => notifications.value.filter((item) => !readNotificationKeys.value.has(item.key)).length
);

function handleLogout() {
  authStore.logout();
  router.push("/login");
}

function getTodayDateValue() {
  const today = new Date();
  const year = today.getFullYear();
  const month = String(today.getMonth() + 1).padStart(2, "0");
  const day = String(today.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
}

function toNotificationTime(value) {
  if (!value) return "Today";
  if (value === getTodayDateValue()) return "Today";
  return value;
}

function notificationStorageKey() {
  const userKey = authStore.currentUser?.username || authStore.currentUser?.email || "guest";
  return `hris-read-notifications:${userKey}`;
}

function makeNotificationKey(parts) {
  return parts.map((part) => String(part || "").trim().toLowerCase()).join("|");
}

function loadReadNotificationKeys() {
  try {
    readNotificationKeys.value = new Set(JSON.parse(localStorage.getItem(notificationStorageKey()) || "[]"));
  } catch {
    readNotificationKeys.value = new Set();
  }
}

function saveReadNotificationKeys(keys) {
  localStorage.setItem(notificationStorageKey(), JSON.stringify([...keys].slice(-100)));
}

function markNotificationsViewed() {
  if (!notifications.value.length) return;

  const nextKeys = new Set(readNotificationKeys.value);
  notifications.value.forEach((item) => {
    if (item.key) nextKeys.add(item.key);
  });
  readNotificationKeys.value = nextKeys;
  saveReadNotificationKeys(nextKeys);
}

function buildAttendanceNotifications(logs) {
  const todayDate = getTodayDateValue();

  return (logs || [])
    .filter((log) => log.work_date === todayDate)
    .filter((log) => {
      const status = String(log.status || "").toLowerCase();
      return status.includes("correction") || status.includes("late") || status.includes("undertime") || status.includes("incomplete") || status.includes("duplicate");
    })
    .slice(0, 4)
    .map((log) => ({
      key: makeNotificationKey(["attendance", log.log_id, log.employee_code, log.work_date, log.status]),
      title: `${log.employee_name || log.employee_code || "Employee"} attendance`,
      subtitle: log.status || "Attendance update",
      time: toNotificationTime(log.work_date),
      route: "/attendance",
      icon: "ti ti-clock-exclamation",
      avatarClass: "bg-light-warning text-warning",
    }));
}

function buildLeaveNotifications(summary) {
  const pendingCount = Number(summary?.pending_requests || 0);
  if (!pendingCount) return [];

  return [
    {
      key: makeNotificationKey(["leave", "pending", pendingCount]),
      title: "Pending leave requests",
      subtitle: `${pendingCount} leave request(s) waiting for review.`,
      time: "Today",
      route: "/leave",
      icon: "ti ti-calendar-time",
      avatarClass: "bg-light-info text-info",
    },
  ];
}

function buildPayrollNotifications(summary, runs) {
  const draftCount = Number(summary?.draft_runs || 0);
  const exceptionRuns = (runs || []).filter((run) => String(run.payslip_status || "").toLowerCase() === "exception");
  const items = [];

  if (draftCount) {
    items.push({
      key: makeNotificationKey(["payroll", "draft", draftCount]),
      title: "Payroll drafts in progress",
      subtitle: `${draftCount} payroll draft(s) still need finalization.`,
      time: "Today",
      route: "/payroll",
      icon: "ti ti-file-invoice",
      avatarClass: "bg-light-primary text-primary",
    });
  }

  if (exceptionRuns.length) {
    items.push({
      key: makeNotificationKey(["payroll", "exception", exceptionRuns.length]),
      title: "Payroll exceptions found",
      subtitle: `${exceptionRuns.length} payroll record(s) need attention.`,
      time: "Today",
      route: "/payroll",
      icon: "ti ti-alert-circle",
      avatarClass: "bg-light-danger text-danger",
    });
  }

  return items;
}

async function loadNotifications() {
  if (!authStore.accessToken) {
    notifications.value = [];
    notificationsError.value = "";
    return;
  }

  notificationsLoading.value = true;
  notificationsError.value = "";

  try {
    const [attendanceLogs, leaveSummary, payrollSummary, payrollRuns] = await Promise.all([
      apiRequest("/attendance", { token: authStore.accessToken }),
      apiRequest("/leave/summary", { token: authStore.accessToken }),
      apiRequest("/payroll/summary", { token: authStore.accessToken }),
      apiRequest("/payroll", { token: authStore.accessToken }),
    ]);

    notifications.value = [
      ...buildAttendanceNotifications(attendanceLogs.items || []),
      ...buildLeaveNotifications(leaveSummary),
      ...buildPayrollNotifications(payrollSummary, payrollRuns.items || []),
    ].slice(0, 6);
  } catch (error) {
    if (error instanceof ApiError && error.status === 401) {
      authStore.logout();
      router.push("/login");
      return;
    }

    notifications.value = [];
    notificationsError.value = "Could not load notifications.";
  } finally {
    notificationsLoading.value = false;
  }
}

function goToNotification(item) {
  if (item?.key) {
    const nextKeys = new Set(readNotificationKeys.value);
    nextKeys.add(item.key);
    readNotificationKeys.value = nextKeys;
    saveReadNotificationKeys(nextKeys);
  }

  if (item?.route) {
    router.push(item.route);
  }
}

onMounted(() => {
  loadReadNotificationKeys();
  loadNotifications();
});

watch(
  () => authStore.accessToken,
  () => {
    loadReadNotificationKeys();
    loadNotifications();
  }
);
</script>

<style scoped>
.notification-trigger {
  position: relative;
}

.pc-h-badge {
  position: absolute;
  top: 2px;
  right: -4px;
  min-width: 18px;
  height: 18px;
  padding: 0 5px;
  font-size: 0.65rem;
  line-height: 18px;
}

.notification-avatar {
  display: inline-flex;
  align-items: center;
  justify-content: center;
}
</style>
