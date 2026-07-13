<template>
  <div class="employee-search-select" :class="{ 'is-disabled': disabled }">
    <div class="employee-search-input-wrap">
      <input
        :id="inputId"
        v-model="searchText"
        type="text"
        class="form-control"
        :class="[inputClass, { 'is-invalid': invalid }]"
        :placeholder="placeholder"
        :disabled="disabled"
        autocomplete="off"
        role="combobox"
        :aria-expanded="isOpen"
        @focus="openSuggestions"
        @input="handleInput"
        @keydown.down.prevent="moveHighlight(1)"
        @keydown.up.prevent="moveHighlight(-1)"
        @keydown.enter.prevent="selectHighlighted"
        @keydown.esc="closeSuggestions"
        @blur="closeSuggestionsSoon"
      >
      <button
        v-if="modelValue && !disabled"
        type="button"
        class="employee-search-clear"
        aria-label="Clear selected employee"
        @mousedown.prevent="clearSelection"
      >
        <i class="ti ti-x"></i>
      </button>
    </div>

    <div v-if="isOpen" class="employee-search-menu">
      <button
        v-for="(option, index) in filteredOptions"
        :key="optionValue(option)"
        type="button"
        class="employee-search-option"
        :class="{ active: index === highlightedIndex }"
        @mousedown.prevent="selectOption(option)"
      >
        <span>{{ optionPrimary(option) }}</span>
        <small>{{ optionMeta(option) }}</small>
      </button>
      <div v-if="!filteredOptions.length" class="employee-search-empty">No matching employee found.</div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, watch } from "vue";

const props = defineProps({
  modelValue: {
    type: String,
    default: "",
  },
  options: {
    type: Array,
    default: () => [],
  },
  inputId: {
    type: String,
    default: "",
  },
  placeholder: {
    type: String,
    default: "Type employee name, code, or email",
  },
  disabled: {
    type: Boolean,
    default: false,
  },
  invalid: {
    type: Boolean,
    default: false,
  },
  inputClass: {
    type: String,
    default: "",
  },
  valueKey: {
    type: String,
    default: "employee_code",
  },
  labelKey: {
    type: String,
    default: "name",
  },
  detailKeys: {
    type: Array,
    default: () => ["employee_code", "employeeCode", "email", "department"],
  },
});

const emit = defineEmits(["update:modelValue", "change"]);

const searchText = ref("");
const isOpen = ref(false);
const highlightedIndex = ref(0);

const selectedOption = computed(() =>
  props.options.find((option) => optionValue(option) === props.modelValue) || null
);

const filteredOptions = computed(() => {
  const query = searchText.value.trim().toLowerCase();
  const options = props.options || [];

  if (!query) return options.slice(0, 8);

  return options
    .filter((option) => searchableText(option).includes(query))
    .slice(0, 8);
});

function optionValue(option) {
  return String(option?.[props.valueKey] || option?.employee_code || option?.employeeCode || option?.name || "");
}

function optionPrimary(option) {
  return String(option?.[props.labelKey] || option?.name || option?.employee_name || optionValue(option));
}

function optionMeta(option) {
  return props.detailKeys
    .map((key) => option?.[key])
    .filter(Boolean)
    .join(" - ");
}

function searchableText(option) {
  return [
    optionPrimary(option),
    optionMeta(option),
    optionValue(option),
  ]
    .join(" ")
    .toLowerCase();
}

function syncSearchText() {
  searchText.value = selectedOption.value ? optionPrimary(selectedOption.value) : "";
}

function openSuggestions() {
  if (props.disabled) return;
  isOpen.value = true;
  highlightedIndex.value = 0;
}

function closeSuggestions() {
  isOpen.value = false;
  syncSearchText();
}

function closeSuggestionsSoon() {
  window.setTimeout(closeSuggestions, 120);
}

function handleInput() {
  openSuggestions();
  highlightedIndex.value = 0;

  if (!searchText.value.trim()) {
    emit("update:modelValue", "");
    emit("change", "");
  }
}

function moveHighlight(direction) {
  openSuggestions();
  if (!filteredOptions.value.length) return;

  highlightedIndex.value =
    (highlightedIndex.value + direction + filteredOptions.value.length) % filteredOptions.value.length;
}

function selectHighlighted() {
  const option = filteredOptions.value[highlightedIndex.value];
  if (option) selectOption(option);
}

function selectOption(option) {
  const value = optionValue(option);
  emit("update:modelValue", value);
  emit("change", value);
  searchText.value = optionPrimary(option);
  isOpen.value = false;
}

function clearSelection() {
  searchText.value = "";
  emit("update:modelValue", "");
  emit("change", "");
  openSuggestions();
}

watch(
  () => [props.modelValue, props.options],
  () => {
    syncSearchText();
  },
  { immediate: true, deep: true }
);
</script>

<style scoped>
.employee-search-select {
  position: relative;
}

.employee-search-input-wrap {
  position: relative;
}

.employee-search-clear {
  align-items: center;
  background: transparent;
  border: 0;
  color: #64748b;
  display: inline-flex;
  height: 2rem;
  justify-content: center;
  position: absolute;
  right: 0.35rem;
  top: 50%;
  transform: translateY(-50%);
  width: 2rem;
}

.employee-search-menu {
  background: #fff;
  border: 1px solid rgba(148, 163, 184, 0.28);
  box-shadow: 0 18px 40px rgba(15, 23, 42, 0.12);
  left: 0;
  max-height: 18rem;
  overflow-y: auto;
  position: absolute;
  right: 0;
  top: calc(100% + 0.35rem);
  z-index: 30;
}

.employee-search-option {
  background: #fff;
  border: 0;
  border-bottom: 1px solid rgba(148, 163, 184, 0.12);
  display: block;
  padding: 0.75rem 0.9rem;
  text-align: left;
  width: 100%;
}

.employee-search-option span {
  color: #0f172a;
  display: block;
  font-weight: 700;
}

.employee-search-option small {
  color: #64748b;
  display: block;
  margin-top: 0.15rem;
}

.employee-search-option:hover,
.employee-search-option.active {
  background: rgba(13, 110, 253, 0.08);
}

.employee-search-empty {
  color: #64748b;
  padding: 0.85rem 0.9rem;
}
</style>
