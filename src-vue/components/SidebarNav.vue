<template>
  <nav class="pc-sidebar" :class="{ 'pc-sidebar-hide': sidebarHidden, 'mob-sidebar-active': mobileOpen }">
    <div class="navbar-wrapper">
      <div class="m-header text-center py-3">
        <RouterLink to="/dashboard" class="b-brand text-primary d-block w-100 text-center py-2">
          <span class="fw-bold fs-3 d-block">HRIS</span>
        </RouterLink>
      </div>
      <div class="navbar-content">
        <ul class="pc-navbar">
          <li v-for="item in navItems" :key="item.to" class="pc-item" :class="{ active: route.path === item.to }">
            <RouterLink :to="item.to" class="pc-link">
              <span class="pc-micon"><i :class="item.icon"></i></span>
              <span class="pc-mtext">{{ item.label }}</span>
            </RouterLink>
          </li>
        </ul>
      </div>
    </div>
    <div v-if="mobileOpen" class="pc-menu-overlay" @click="$emit('closeMobile')"></div>
  </nav>
</template>

<script setup>
import { useRoute, RouterLink } from "vue-router";

defineProps({
  sidebarHidden: {
    type: Boolean,
    default: false,
  },
  mobileOpen: {
    type: Boolean,
    default: false,
  },
});

defineEmits(["closeMobile"]);

const route = useRoute();

const navItems = [
  { to: "/dashboard", label: "Dashboard", icon: "ti ti-dashboard" },
  { to: "/employees", label: "Employee Master", icon: "ti ti-users" },
  { to: "/attendance", label: "Time & Attendance", icon: "ti ti-clock" },
  { to: "/leave", label: "Leave Management", icon: "ti ti-calendar-event" },
  { to: "/payroll", label: "Payroll", icon: "ti ti-receipt-2" },
  { to: "/accounts", label: "Accounts", icon: "ti ti-user-check" },
  { to: "/reports", label: "Reports", icon: "ti ti-chart-bar" },
];
</script>
