<template>
  <div class="vue-shell">
    <div class="loader-bg" v-if="false">
      <div class="loader-track">
        <div class="loader-fill"></div>
      </div>
    </div>

    <SidebarNav :sidebar-hidden="isSidebarHidden" :mobile-open="isMobileSidebarOpen" @close-mobile="closeMobileSidebar" />

    <header class="pc-header">
      <div class="header-wrapper">
        <TopbarHeader @toggle-sidebar="toggleSidebar" />
      </div>
    </header>

    <div class="pc-container">
      <div class="pc-content">
        <slot />
      </div>
    </div>
  </div>
</template>

<script setup>
import { onBeforeUnmount, onMounted, ref, watch } from "vue";
import { useRoute } from "vue-router";
import SidebarNav from "@/components/SidebarNav.vue";
import TopbarHeader from "@/components/TopbarHeader.vue";

const route = useRoute();
const isSidebarHidden = ref(false);
const isMobileSidebarOpen = ref(false);

function isMobileViewport() {
  return typeof window !== "undefined" && window.innerWidth <= 1024;
}

function closeMobileSidebar() {
  isMobileSidebarOpen.value = false;
}

function handleResize() {
  if (!isMobileViewport()) {
    isMobileSidebarOpen.value = false;
  }
}

function toggleSidebar() {
  if (isMobileViewport()) {
    isMobileSidebarOpen.value = !isMobileSidebarOpen.value;
    return;
  }

  isSidebarHidden.value = !isSidebarHidden.value;
}

watch(
  () => route.fullPath,
  () => {
    closeMobileSidebar();
  }
);

onMounted(() => {
  window.addEventListener("resize", handleResize);
});

onBeforeUnmount(() => {
  window.removeEventListener("resize", handleResize);
});
</script>
