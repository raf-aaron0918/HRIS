<template>
  <div>
    <BreadcrumbBar section="HR Modules" current="Employee Master" />

    <div class="row g-3 mb-4">
      <div class="col-6 col-md-6 col-xl-3">
        <div class="card border-0 shadow-sm h-100">
          <div class="card-body">
            <small class="text-muted d-block mb-2">Total Employees</small>
            <div class="d-flex align-items-end justify-content-between">
              <div>
                <h3 class="mb-1">{{ overview.totalEmployees }}</h3>
                <span class="text-muted small">All employee records</span>
              </div>
              <span class="badge bg-light-primary text-primary">Total</span>
            </div>
          </div>
        </div>
      </div>

      <div class="col-6 col-md-6 col-xl-3">
        <div class="card border-0 shadow-sm h-100">
          <div class="card-body">
            <small class="text-muted d-block mb-2">Active Access</small>
            <div class="d-flex align-items-end justify-content-between">
              <div>
                <h3 class="mb-1">{{ overview.activeAccounts }}</h3>
                <span class="text-muted small">Currently active</span>
              </div>
              <span class="badge bg-light-success text-success">Active</span>
            </div>
          </div>
        </div>
      </div>

      <div class="col-6 col-md-6 col-xl-3">
        <div class="card border-0 shadow-sm h-100">
          <div class="card-body">
            <small class="text-muted d-block mb-2">Onboarding</small>
            <div class="d-flex align-items-end justify-content-between">
              <div>
                <h3 class="mb-1">{{ overview.onboardingEmployees }}</h3>
                <span class="text-muted small">In progress</span>
              </div>
              <span class="badge bg-light-info text-info">Pending</span>
            </div>
          </div>
        </div>
      </div>

      <div class="col-6 col-md-6 col-xl-3">
        <div class="card border-0 shadow-sm h-100">
          <div class="card-body">
            <small class="text-muted d-block mb-2">Missing Docs</small>
            <div class="d-flex align-items-end justify-content-between">
              <div>
                <h3 class="mb-1">{{ overview.missingDocuments }}</h3>
                <span class="text-muted small">Needs attention</span>
              </div>
              <span class="badge bg-light-warning text-warning">Alert</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="row g-3">
      <div class="col-12">
        <div class="card border-0 shadow-sm">
          <div class="card-header bg-white border-bottom-0 pt-4 pb-0">
            <div class="d-flex flex-column flex-md-row justify-content-between align-items-md-center gap-3">
              <div>
                <h5 class="mb-0">Employee Directory</h5>
                <small class="text-muted">{{ employeeCountLabel }}</small>
              </div>
              <div class="d-flex gap-2">
                <div class="input-group" style="max-width: 300px;">
                  <span class="input-group-text bg-light border-end-0"><i class="ti ti-search"></i></span>
                  <input v-model="employeeSearch" type="text" class="form-control border-start-0 ps-0 bg-light" placeholder="Search employees...">
                </div>
                <RouterLink v-if="canManageEmployees" to="/employee/new" class="btn btn-primary d-flex align-items-center gap-2 text-nowrap">
                  <i class="ti ti-user-plus"></i> New Employee
                </RouterLink>
              </div>
            </div>
          </div>

          <div class="card-body p-0">
            <div class="px-3 pt-3 d-flex flex-nowrap overflow-auto gap-2 pb-2 mobile-filter-scroll">
              <button
                v-for="filter in directoryFilters"
                :key="filter.value"
                class="btn btn-sm rounded-pill px-3"
                :class="activeDirectoryFilter === filter.value ? 'btn-primary' : 'btn-outline-secondary'"
                @click="activeDirectoryFilter = filter.value"
              >
                {{ filter.label }}
              </button>
            </div>

            <div v-if="isDirectoryLoading" class="text-center py-5">
              <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading directory...</span>
              </div>
            </div>

            <div v-else-if="directoryError" class="alert alert-danger mx-3 mb-3">
              {{ directoryError }}
            </div>

            <div v-else class="mt-3">
              <div v-if="filteredDirectory.length === 0" class="text-center py-4 text-muted">
                No employees match your search or filter criteria.
              </div>

              <template v-else>
                <div class="d-none d-md-block">
                  <div class="table-responsive">
                    <table class="table table-hover align-middle mb-0">
                      <thead class="table-light">
                        <tr>
                          <th>ID</th>
                          <th>Employee</th>
                          <th>Assignment</th>
                          <th>Status</th>
                          <th>Lifecycle</th>
                          <th>Docs</th>
                          <th>Contact</th>
                          <th class="text-end">Action</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr v-for="row in filteredDirectory" :key="row.id">
                          <td data-label="Employee ID">{{ row.id }}</td>
                          <td data-label="Name">{{ row.name }}</td>
                          <td data-label="Assignment">{{ row.assignment }}</td>
                          <td data-label="Status"><span class="badge" :class="row.statusClass">{{ row.statusLabel }}</span></td>
                          <td data-label="Lifecycle"><span class="badge" :class="row.lifecycleClass">{{ row.lifecycleLabel }}</span></td>
                          <td data-label="Documents">{{ row.documents }} / 4</td>
                          <td data-label="Email">{{ row.email }}</td>
                          <td data-label="Action" class="text-end">
                            <RouterLink :to="'/employee/' + row.id" class="btn btn-sm btn-outline-primary">View</RouterLink>
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>

                <div class="d-md-none">
                  <div v-for="row in filteredDirectory" :key="row.id" class="border rounded p-3 mb-2 shadow-sm">
                    <div class="d-flex justify-content-between align-items-start gap-2">
                      <div>
                        <div class="fw-semibold">{{ row.name }}</div>
                        <div class="small text-muted">{{ row.id }}</div>
                      </div>
                      <RouterLink :to="'/employee/' + row.id" class="btn btn-sm btn-outline-primary">View</RouterLink>
                    </div>
                    <div class="small text-muted mt-2">{{ row.assignment }}</div>
                  </div>
                </div>
              </template>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from "vue";
import { RouterLink } from "vue-router";
import BreadcrumbBar from "@/components/BreadcrumbBar.vue";
import { ApiError, apiRequest } from "@/lib/api";
import { useAuthStore } from "@/stores/auth";

const authStore = useAuthStore();
const canManageEmployees = computed(() => authStore.currentUser?.role === "HR Admin");

const baseDirectory = ref([]);
const directoryError = ref("");
const isDirectoryLoading = ref(false);

const directoryFilters = [
  { value: "all", label: "All" },
  { value: "active", label: "Active Access" },
  { value: "probationary", label: "Probationary" },
  { value: "separated", label: "Separated" },
  { value: "missing-docs", label: "Missing Docs" },
];

const employeeSearch = ref("");
const activeDirectoryFilter = ref("all");

const overview = computed(() => ({
  totalEmployees: baseDirectory.value.length,
  activeAccounts: baseDirectory.value.filter((row) => row.account === "active").length,
  onboardingEmployees: baseDirectory.value.filter((row) => row.lifecycle === "onboarding").length,
  missingDocuments: baseDirectory.value.filter((row) => row.documents < 4).length,
}));

const filteredDirectory = computed(() => {
  let result = baseDirectory.value;

  if (activeDirectoryFilter.value !== "all") {
    switch (activeDirectoryFilter.value) {
      case "active":
        result = result.filter((row) => row.account === "active");
        break;
      case "probationary":
        result = result.filter((row) => row.employment === "probationary");
        break;
      case "separated":
        result = result.filter((row) => row.account === "separated" || row.lifecycle === "offboarding");
        break;
      case "missing-docs":
        result = result.filter((row) => row.documents < 4);
        break;
    }
  }

  const query = employeeSearch.value.toLowerCase().trim();
  if (query) {
    result = result.filter(
      (row) =>
        row.name.toLowerCase().includes(query) ||
        row.id.toLowerCase().includes(query) ||
        row.assignment.toLowerCase().includes(query) ||
        row.email.toLowerCase().includes(query)
    );
  }

  return result;
});

const employeeCountLabel = computed(() => {
  const count = filteredDirectory.value.length;
  return count === 1 ? "1 employee" : `${count} employees`;
});

function normalizeEmployeeRow(employee) {
  const isRegular = employee.employment_status === "Regular";
  const lifecycle = isRegular ? "completed" : "onboarding";

  return {
    id: employee.employee_code,
    name: `${employee.first_name} ${employee.last_name}`,
    assignment: `${employee.department} / ${employee.position} / ${employee.branch || "Main Branch"}`,
    account: (employee.account_status || (isRegular ? "Active" : employee.employment_status)).toLowerCase(),
    employment: employee.employment_status.toLowerCase(),
    lifecycle: employee.offboarding_reason ? "offboarding" : lifecycle,
    documents: 3,
    email: employee.email,
    statusLabel: employee.account_status || (isRegular ? "Active" : employee.employment_status),
    statusClass:
      (employee.account_status || (isRegular ? "Active" : employee.employment_status)) === "Active"
        ? "bg-light-success text-success"
        : (employee.account_status || "") === "Separated"
          ? "bg-light-danger text-danger"
          : "bg-light-warning text-warning",
    lifecycleLabel: employee.offboarding_reason ? "Offboarding" : lifecycle === "completed" ? "Completed" : "Onboarding",
    lifecycleClass: employee.offboarding_reason
      ? "bg-light-danger text-danger"
      : lifecycle === "completed"
        ? "bg-light-info text-info"
        : "bg-light-warning text-warning",
  };
}

async function fetchEmployees() {
  const token = authStore.accessToken;

  if (!token) {
    directoryError.value = "Sign in first to load employee records.";
    return;
  }

  isDirectoryLoading.value = true;
  directoryError.value = "";

  try {
    const response = await apiRequest("/employees", {
      token,
    });

    const rawItems = Array.isArray(response) ? response : response?.items || [];
    const apiRows = rawItems.map((employee) => normalizeEmployeeRow(employee));

    baseDirectory.value = apiRows;
  } catch (error) {
    if (error instanceof ApiError && error.status === 401) {
      directoryError.value = "Your session expired. Please sign in again.";
      authStore.logout();
    } else {
      const detail = error instanceof Error ? error.message : "Unknown error";
      directoryError.value = detail || "Could not reach the HRIS API. No local employee records are shown.";
      baseDirectory.value = [];
    }
  } finally {
    isDirectoryLoading.value = false;
  }
}

onMounted(() => {
  fetchEmployees();
});
</script>
