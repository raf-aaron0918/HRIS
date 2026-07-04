<template>
  <div class="page-header">
    <div class="page-block">
      <div class="row align-items-center">
        <div class="col-md-12">
          <div class="page-header-title">
            <h5 class="mb-0">{{ current }}</h5>
          </div>
          <ul class="breadcrumb">
            <li class="breadcrumb-item">{{ section }}</li>
            <li class="breadcrumb-item" aria-current="page">{{ current }}</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  section: {
    type: String,
    required: true,
  },
  current: {
    type: String,
    required: true,
  },
});
</script>
