<template>
  <div>
    <BreadcrumbBar :section="section" :current="current" />
    <div ref="moduleRoot"></div>
  </div>
</template>

<script setup>
import { onMounted, ref } from "vue";
import BreadcrumbBar from "@/components/BreadcrumbBar.vue";
import { mountLegacyModule } from "@/utils/htmlModule";

const props = defineProps({
  rawHtml: {
    type: String,
    required: true,
  },
  section: {
    type: String,
    required: true,
  },
  current: {
    type: String,
    required: true,
  },
  extraScope: {
    type: Object,
    default: () => ({}),
  },
});

const moduleRoot = ref(null);

onMounted(() => {
  if (!moduleRoot.value) {
    return;
  }
  mountLegacyModule(moduleRoot.value, props.rawHtml, props.extraScope);
});
</script>
