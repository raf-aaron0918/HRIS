<template>
  <div class="me-auto pc-mob-drp">
    <ul class="list-unstyled">
      <li class="pc-h-item pc-sidebar-collapse">
        <a href="#" class="pc-head-link ms-0" aria-label="Toggle sidebar" @click.prevent="$emit('toggleSidebar')">
          <i class="ti ti-menu-2"></i>
        </a>
      </li>
      <li class="pc-h-item d-none d-md-inline-flex">
        <form class="header-search">
          <i class="ti ti-search icon-search"></i>
          <input type="search" class="form-control border-0 shadow-none" placeholder="Search here..." />
        </form>
      </li>
    </ul>
  </div>
  <div class="ms-auto">
    <ul class="list-unstyled">
      <li class="dropdown pc-h-item">
        <a class="pc-head-link dropdown-toggle arrow-none me-0" data-bs-toggle="dropdown" href="#" role="button">
          <i class="ti ti-mail"></i>
        </a>
        <div class="dropdown-menu dropdown-notification dropdown-menu-end pc-h-dropdown">
          <div class="dropdown-header d-flex align-items-center justify-content-between">
            <h5 class="m-0">Message</h5>
            <a href="#!" class="pc-head-link bg-transparent"><i class="ti ti-x text-danger"></i></a>
          </div>
          <div class="dropdown-divider"></div>
          <div class="dropdown-header px-0 text-wrap header-notification-scroll position-relative" style="max-height: calc(100vh - 215px)">
            <div class="list-group list-group-flush w-100">
              <a class="list-group-item list-group-item-action" v-for="item in messages" :key="item.title">
                <div class="d-flex">
                  <div class="flex-shrink-0">
                    <img :src="item.avatar" alt="user-image" class="user-avtar" />
                  </div>
                  <div class="flex-grow-1 ms-1">
                    <span class="float-end text-muted">{{ item.time }}</span>
                    <p class="text-body mb-1" v-html="item.title"></p>
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
          <img src="/dist/assets/images/user/avatar-2.jpg" alt="user-image" class="user-avtar" />
          <span>{{ displayName }}</span>
        </a>
        <div class="dropdown-menu dropdown-user-profile dropdown-menu-end pc-h-dropdown">
          <div class="dropdown-header">
            <div class="d-flex mb-1">
              <div class="flex-shrink-0">
                <img src="/dist/assets/images/user/avatar-2.jpg" alt="user-image" class="user-avtar wid-35" />
              </div>
              <div class="flex-grow-1 ms-3">
                <h6 class="mb-1">{{ displayName }}</h6>
                <span>{{ displayRole }}</span>
              </div>
            </div>
          </div>
          <div class="px-3 pb-3">
            <RouterLink to="/dashboard" class="dropdown-item">
              <i class="ti ti-dashboard"></i>
              <span>Dashboard</span>
            </RouterLink>
            <RouterLink to="/employees" class="dropdown-item">
              <i class="ti ti-users"></i>
              <span>Employee Master</span>
            </RouterLink>
            <RouterLink to="/accounts" class="dropdown-item">
              <i class="ti ti-user-cog"></i>
              <span>Accounts</span>
            </RouterLink>
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
import { computed } from "vue";
import { RouterLink } from "vue-router";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";

defineEmits(["toggleSidebar"]);
const router = useRouter();
const authStore = useAuthStore();

const displayName = computed(() => authStore.currentUser?.full_name || "HRIS User");
const displayRole = computed(() => authStore.currentUser?.role || "Authorized User");

function handleLogout() {
  authStore.logout();
  router.push("/login");
}

const messages = [
  {
    avatar: "/dist/assets/images/user/avatar-2.jpg",
    time: "3:00 AM",
    title: "It's <b>Cristina Danny's</b> birthday today.",
    subtitle: "2 min ago",
  },
  {
    avatar: "/dist/assets/images/user/avatar-1.jpg",
    time: "6:00 PM",
    title: "<b>Aida Burg</b> commented on your post.",
    subtitle: "5 August",
  },
  {
    avatar: "/dist/assets/images/user/avatar-3.jpg",
    time: "2:45 PM",
    title: "<b>There was a failure in your setup.</b>",
    subtitle: "7 hours ago",
  },
];
</script>
