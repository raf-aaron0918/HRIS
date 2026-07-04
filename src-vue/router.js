import { createRouter, createWebHistory } from "vue-router";
import LoginPage from "@/pages/LoginPage.vue";
import DashboardPage from "@/pages/DashboardPage.vue";
import EmployeeMasterPage from "@/pages/EmployeeMasterPage.vue";
import AttendancePage from "@/pages/AttendancePage.vue";
import LeaveManagementPage from "@/pages/LeaveManagementPage.vue";
import PayrollPage from "@/pages/PayrollPage.vue";
import ReportsPage from "@/pages/ReportsPage.vue";
import AccountManagementPage from "@/pages/AccountManagementPage.vue";
import { useAuthStore } from "@/stores/auth";

const routes = [
  {
    path: "/",
    redirect: "/login",
  },
  {
    path: "/login",
    name: "login",
    component: LoginPage,
    meta: {
      shell: false,
      title: "Sign In to HRIS",
    },
  },
  {
    path: "/dashboard",
    name: "dashboard",
    component: DashboardPage,
    meta: {
      shell: true,
      title: "HR Dashboard",
      breadcrumb: {
        section: "Dashboard",
        current: "Home",
      },
    },
  },
  {
    path: "/employees",
    name: "employees",
    component: EmployeeMasterPage,
    meta: {
      shell: true,
      title: "Employee Master",
    },
  },
  {
    path: "/attendance",
    name: "attendance",
    component: AttendancePage,
    meta: {
      shell: true,
      title: "Time & Attendance",
    },
  },
  {
    path: "/leave",
    name: "leave",
    component: LeaveManagementPage,
    meta: {
      shell: true,
      title: "Leave Management",
    },
  },
  {
    path: "/payroll",
    name: "payroll",
    component: PayrollPage,
    meta: {
      shell: true,
      title: "Payroll",
    },
  },
  {
    path: "/accounts",
    name: "accounts",
    component: AccountManagementPage,
    meta: {
      shell: true,
      title: "User Accounts",
    },
  },
  {
    path: "/reports",
    name: "reports",
    component: ReportsPage,
    meta: {
      shell: true,
      title: "Reports",
    },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach(async (to) => {
  const authStore = useAuthStore();

  if (!authStore.hydrated) {
    authStore.hydrate();
  }

  if (to.meta.shell && !authStore.isAuthenticated) {
    return {
      path: "/login",
      query: { redirect: to.fullPath },
    };
  }

  if (to.path === "/login" && authStore.isAuthenticated) {
    return "/dashboard";
  }

  return true;
});

router.afterEach((to) => {
  if (to.meta?.title) {
    document.title = `HRIS | ${to.meta.title}`;
  }
});

export default router;
