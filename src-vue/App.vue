<template>
  <RouterView v-slot="{ Component, route }">
    <AppShell v-if="route.meta.shell">
      <component :is="Component" />
    </AppShell>
    <component :is="Component" v-else />
  </RouterView>
</template>

<script setup>
import { RouterView } from "vue-router";
import AppShell from "@/layouts/AppShell.vue";
</script>
