<template>
  <div>
    <BreadcrumbBar section="Administration" current="Accounts" />

    <div class="premium-hero mb-4">
      <div class="d-flex flex-column flex-md-row justify-content-between align-items-md-center gap-3">
        <div>
          <div class="premium-badge mb-2">Administration</div>
          <h4 class="mb-1 premium-title">Accounts</h4>
          <p class="mb-0 premium-subtitle">Create and manage HRIS sign-ins with a clearer access flow and a cleaner account list.</p>
        </div>
      </div>
    </div>

    <div class="row g-3">
      <div class="col-12">
        <div class="card h-100 border-0 shadow-sm premium-panel">
          <div class="card-header d-flex flex-column flex-md-row align-items-stretch align-items-md-center justify-content-between gap-3 bg-white border-bottom-0 pt-4 pb-0 premium-panel-header">
            <div>
              <h5 class="mb-0">Create Account</h5>
              <small class="text-muted">Add a login for HR Admin, Immediate Supervisor, or Payroll Admin users.</small>
            </div>
            <span class="badge" :class="roleBadgeClass">{{ currentRole }}</span>
          </div>
          <div class="card-body premium-panel-body">
            <div v-if="!canManageAccounts" class="alert alert-light-warning border-warning mb-3" role="alert">
              Your current role can view this module, but only HR Admin accounts can create new logins.
            </div>

            <form novalidate @submit.prevent="handleSubmit">
              <div class="row">
                <div class="col-12 mb-3">
                  <label class="form-label" for="accountEmployee">Who is this account for?</label>
                  <EmployeeSearchSelect
                    v-model="form.employeeCode"
                    input-id="accountEmployee"
                    :options="employeeOptions"
                    value-key="employeeCode"
                    input-class="premium-input"
                    :disabled="!canManageAccounts || isSubmitting"
                    placeholder="Type name, employee code, or email"
                    @change="populateSelectedEmployee"
                  />
                  <small class="text-muted">Choose an employee to auto-fill the account owner details and access role.</small>
                </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label" for="accountFullName">Full Name</label>
                  <input id="accountFullName" v-model="form.fullName" type="text" class="form-control premium-input" placeholder="Employee full name" :disabled="!canManageAccounts || isSubmitting">
                </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label" for="accountUsername">Username</label>
                  <input id="accountUsername" v-model="form.username" type="text" class="form-control premium-input" placeholder="maria.santos" :disabled="!canManageAccounts || isSubmitting">
                </div>

                <div class="col-md-6 mb-3">
                  <label class="form-label" for="accountEmail">Email</label>
                  <input id="accountEmail" v-model="form.email" type="email" class="form-control premium-input" placeholder="maria.santos@company.com" :disabled="!canManageAccounts || isSubmitting">
                </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label" for="accountPassword">Temporary Password</label>
                  <input id="accountPassword" v-model="form.password" type="password" class="form-control premium-input" placeholder="Minimum 8 characters" :disabled="!canManageAccounts || isSubmitting">
                </div>

                <div class="col-md-6 mb-3">
                  <label class="form-label" for="accountRole">Assigned Role</label>
                  <input id="accountRole" :value="form.role || 'Select an employee first'" type="text" class="form-control premium-input" readonly>
                  <small class="text-muted">{{ roleAccessNote }}</small>
                </div>
                <div class="col-md-6 mb-3 d-flex align-items-end">
                  <div class="border rounded-4 px-3 py-2 bg-light w-100 premium-note">
                    <small class="text-muted d-block mb-1">Account status</small>
                    <strong>New accounts are created active by default.</strong>
                  </div>
                </div>
              </div>

              <div class="d-flex flex-wrap gap-2">
                <button type="button" class="btn btn-outline-primary premium-action" :disabled="isSubmitting" @click="resetFormWithMessage">Clear</button>
                <button type="submit" class="btn btn-primary" :disabled="!canManageAccounts || isSubmitting">
                  {{ isSubmitting ? "Creating..." : "Create Account" }}
                </button>
              </div>

              <div class="alert mt-3 mb-0" :class="alertState.class" role="alert">
                {{ alertState.message }}
              </div>
            </form>
          </div>
        </div>
      </div>

      <div class="col-12">
        <div class="card h-100 border-0 shadow-sm premium-panel">
          <div class="card-header d-flex flex-column flex-md-row align-items-stretch align-items-md-center justify-content-between gap-3 bg-white border-bottom-0 pt-4 pb-0 premium-panel-header">
            <div>
              <h5 class="mb-0">Existing Accounts</h5>
              <small class="text-muted">Review usernames, role assignment, and active status.</small>
            </div>
            <button type="button" class="btn btn-sm btn-light-primary" :disabled="isLoading" @click="fetchAccounts">Refresh</button>
          </div>
          <div class="card-body p-0 premium-panel-body">
            <div v-if="tableMessage" class="alert alert-light-warning border-warning m-3 mb-0" role="alert">
              {{ tableMessage }}
            </div>
            <div class="d-none d-md-block table-responsive">
              <table class="table table-hover align-middle mb-0 premium-table">
                <thead>
                  <tr>
                    <th>Full Name</th>
                    <th>Username</th>
                    <th>Email</th>
                    <th>Role</th>
                    <th>Status</th>
                    <th class="text-end">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-if="!accounts.length && !isLoading">
                    <td colspan="6" class="text-center text-muted py-4">No user accounts found yet.</td>
                  </tr>
                  <tr v-for="account in accounts" :key="account.id">
                    <td>{{ account.full_name }}</td>
                    <td>{{ account.username }}</td>
                    <td>{{ account.email }}</td>
                    <td><span class="badge bg-light-secondary text-secondary">{{ account.role }}</span></td>
                    <td>
                      <span class="badge" :class="account.is_active ? 'bg-light-success text-success' : 'bg-light-danger text-danger'">
                        {{ account.is_active ? "Active" : "Inactive" }}
                      </span>
                    </td>
                    <td class="text-end">
                      <button
                        type="button"
                        class="btn btn-sm"
                        :class="account.is_active ? 'btn-outline-danger' : 'btn-outline-success'"
                        :disabled="isLoading || isSubmitting || toggleUserId === account.id"
                        @click="toggleAccountStatus(account)"
                      >
                        {{ toggleUserId === account.id ? "Updating..." : account.is_active ? "Disable" : "Enable" }}
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            <div class="d-md-none px-3 pb-3">
              <div v-if="!accounts.length && !isLoading" class="text-center text-muted py-4">
                No user accounts found yet.
              </div>

              <div v-for="account in accounts" :key="`mobile-${account.id}`" class="border p-3 mb-2 shadow-sm premium-mobile-card">
                <div class="d-flex justify-content-between align-items-start gap-2">
                  <div>
                    <div class="fw-semibold">{{ account.full_name }}</div>
                    <div class="small text-muted">{{ account.username }}</div>
                  </div>
                  <span class="badge" :class="account.is_active ? 'bg-light-success text-success' : 'bg-light-danger text-danger'">
                    {{ account.is_active ? "Active" : "Inactive" }}
                  </span>
                </div>
                <div class="small text-muted mt-2">{{ account.email }}</div>
                <div class="small text-muted">Role: <span class="badge bg-light-secondary text-secondary">{{ account.role }}</span></div>
                <div class="d-grid mt-3">
                  <button
                    type="button"
                    class="btn btn-sm"
                    :class="account.is_active ? 'btn-outline-danger' : 'btn-outline-success'"
                    :disabled="isLoading || isSubmitting || toggleUserId === account.id"
                    @click="toggleAccountStatus(account)"
                  >
                    {{ toggleUserId === account.id ? "Updating..." : account.is_active ? "Disable" : "Enable" }}
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from "vue";
import BreadcrumbBar from "@/components/BreadcrumbBar.vue";
import EmployeeSearchSelect from "@/components/EmployeeSearchSelect.vue";
import { ApiError, apiRequest } from "@/lib/api";
import { useAuthStore } from "@/stores/auth";

const authStore = useAuthStore();
const accounts = ref([]);
const employeeOptions = ref([]);
const employeeData = ref({});
const isLoading = ref(false);
const isSubmitting = ref(false);
const toggleUserId = ref(null);
const tableMessage = ref("");

const alertState = reactive({
  class: "alert-light-primary border-primary",
  message: "Create a login for staff who need access to the HRIS modules.",
});

const form = reactive(createEmptyForm());

function createEmptyForm() {
  return {
    employeeCode: "",
    fullName: "",
    username: "",
    email: "",
    password: "",
    role: "",
    isActive: true,
  };
}

const currentRole = computed(() => authStore.currentUser?.role || "Authorized User");
const canManageAccounts = computed(() => currentRole.value === "HR Admin");

const roleBadgeClass = computed(() =>
  canManageAccounts.value ? "bg-light-success text-success" : "bg-light-warning text-warning"
);
const roleAccessNote = computed(() => {
  if (form.role === "HR Admin") return "Access: employee records, attendance, leave, payroll, reports, and account management.";
  if (form.role === "Payroll Admin") return "Access: payroll, reports, attendance summaries, and payroll-related records.";
  if (form.role === "Immediate Supervisor") return "Access: team attendance and leave review workflows.";
  return "The access role is assigned from the selected employee's position or department.";
});

function setAlert(type, message) {
  alertState.class = `alert-light-${type} border-${type}`;
  alertState.message = message;
}

function resetForm() {
  Object.assign(form, createEmptyForm());
}

function makeUsername(employee) {
  const firstName = String(employee.first_name || "").trim().toLowerCase();
  const lastName = String(employee.last_name || "").trim().toLowerCase();
  const code = String(employee.employee_code || "").trim().toLowerCase();
  const baseName = [firstName, lastName].filter(Boolean).join(".");
  return (baseName || code).replace(/[^a-z0-9._-]/g, "");
}

function deriveAccountRole(employee) {
  const roleSource = `${employee.position || ""} ${employee.department || ""}`.toLowerCase();

  if (roleSource.includes("payroll")) return "Payroll Admin";
  if (roleSource.includes("hr admin") || roleSource.includes("hr manager") || roleSource.includes("hr officer")) return "HR Admin";
  if (roleSource.includes("human resource") || roleSource.includes("human resources")) return "HR Admin";
  if (roleSource.includes("supervisor") || roleSource.includes("manager") || roleSource.includes("lead") || roleSource.includes("head")) {
    return "Immediate Supervisor";
  }

  return "Immediate Supervisor";
}

function populateSelectedEmployee() {
  const employee = employeeData.value[form.employeeCode];
  if (!employee) return;

  form.fullName = employee.name;
  form.email = employee.email;
  form.username = employee.username;
  form.role = employee.role;
  setAlert("info", `${employee.name} selected. ${employee.role} access will be assigned automatically.`);
}

async function fetchEmployees() {
  if (!authStore.accessToken) return;

  try {
    const response = await apiRequest("/employees", {
      token: authStore.accessToken,
    });
    const employees = response.items || [];
    employeeOptions.value = employees.map((employee) => ({
      employeeCode: employee.employee_code,
      name: `${employee.first_name} ${employee.last_name}`,
      email: employee.email,
    }));
    employeeData.value = Object.fromEntries(
      employees.map((employee) => [
        employee.employee_code,
        {
          employeeCode: employee.employee_code,
          name: `${employee.first_name} ${employee.last_name}`,
          email: employee.email,
          username: makeUsername(employee),
          department: employee.department,
          position: employee.position,
          role: deriveAccountRole(employee),
        },
      ])
    );
  } catch {
    employeeOptions.value = [];
    employeeData.value = {};
  }
}

function resetFormWithMessage() {
  resetForm();
  setAlert("primary", "Create a login for staff who need access to the HRIS modules.");
}

function validateForm() {
  if (!form.employeeCode) {
    setAlert("danger", "Please choose who this account is for.");
    return false;
  }

  if (!form.fullName.trim() || !form.username.trim() || !form.email.trim() || !form.password.trim()) {
    setAlert("danger", "Please complete the full name, username, email, and temporary password fields.");
    return false;
  }

  if (!form.role) {
    setAlert("danger", "The selected employee does not have an assigned access role.");
    return false;
  }

  if (form.password.trim().length < 8) {
    setAlert("danger", "Temporary password must be at least 8 characters.");
    return false;
  }

  return true;
}

async function fetchAccounts() {
  if (!authStore.accessToken) {
    tableMessage.value = "Sign in first to load account records.";
    return;
  }

  isLoading.value = true;
  tableMessage.value = "";

  try {
    const response = await apiRequest("/users", {
      token: authStore.accessToken,
    });
    accounts.value = response.items;
  } catch (error) {
    if (error instanceof ApiError && error.status === 401) {
      tableMessage.value = "Your session expired. Please sign in again.";
      authStore.logout();
    } else if (error instanceof ApiError && error.status === 403) {
      tableMessage.value = "Only HR Admin users can load and manage account records.";
      accounts.value = [];
    } else {
      tableMessage.value = "Could not reach the HRIS API for account records.";
    }
  } finally {
    isLoading.value = false;
  }
}

async function handleSubmit() {
  if (!canManageAccounts.value) {
    setAlert("danger", "Only HR Admin users can create accounts.");
    return;
  }

  if (!validateForm()) {
    return;
  }

  isSubmitting.value = true;

  try {
    const user = await apiRequest("/users", {
      method: "POST",
      token: authStore.accessToken,
      body: JSON.stringify({
        username: form.username.trim(),
        full_name: form.fullName.trim(),
        email: form.email.trim().toLowerCase(),
        password: form.password,
        role: form.role,
        is_active: true,
      }),
    });

    accounts.value = [user, ...accounts.value.filter((account) => account.id !== user.id)];
    resetForm();
    setAlert("success", `${user.full_name} can now sign in with the username ${user.username}.`);
    await fetchAccounts();
  } catch (error) {
    if (error instanceof ApiError && error.status === 401) {
      setAlert("danger", "Your session expired. Please sign in again.");
      authStore.logout();
    } else if (error instanceof ApiError && error.status === 403) {
      setAlert("danger", "Only HR Admin users can create accounts.");
    } else if (error instanceof ApiError && error.status === 409) {
      setAlert("danger", error.message);
    } else if (error instanceof ApiError && error.status === 422) {
      setAlert("danger", "Please review the account fields. The API rejected one or more values.");
    } else {
      setAlert("danger", "Could not create the account. Please make sure the FastAPI backend is running.");
    }
  } finally {
    isSubmitting.value = false;
  }
}

async function toggleAccountStatus(account) {
  toggleUserId.value = account.id;

  try {
    const updatedUser = await apiRequest(`/users/${account.id}/status`, {
      method: "PUT",
      token: authStore.accessToken,
      body: JSON.stringify({
        is_active: !account.is_active,
      }),
    });

    accounts.value = accounts.value.map((item) => (item.id === updatedUser.id ? updatedUser : item));
    setAlert(
      "success",
      `${updatedUser.full_name} is now ${updatedUser.is_active ? "active" : "inactive"}.`
    );
  } catch (error) {
    if (error instanceof ApiError && error.status === 401) {
      setAlert("danger", "Your session expired. Please sign in again.");
      authStore.logout();
    } else if (error instanceof ApiError && error.status === 403) {
      setAlert("danger", "Only HR Admin users can update account status.");
    } else {
      setAlert("danger", "Could not update the account status. Please make sure the FastAPI backend is running.");
    }
  } finally {
    toggleUserId.value = null;
  }
}

onMounted(() => {
  fetchEmployees();
  fetchAccounts();
});
</script>

<style scoped>
.premium-hero {
  border: 1px solid rgba(16, 24, 40, 0.08);
  border-radius: 1.5rem;
  padding: 1.25rem 1.5rem;
  background:
    linear-gradient(135deg, rgba(13, 110, 253, 0.08), rgba(13, 110, 253, 0.02)),
    #fff;
  box-shadow: 0 10px 30px rgba(15, 23, 42, 0.05);
}

.premium-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  border-radius: 999px;
  padding: 0.35rem 0.75rem;
  background: rgba(13, 110, 253, 0.08);
  color: #0d6efd;
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}

.premium-title {
  font-weight: 800;
  letter-spacing: -0.03em;
}

.premium-subtitle {
  color: #64748b;
  max-width: 56rem;
}

.premium-panel {
  border-radius: 1.35rem;
  border: 1px solid rgba(16, 24, 40, 0.06);
  overflow: hidden;
}

.premium-panel-header {
  padding-bottom: 1rem;
}

.premium-panel-body {
  background:
    radial-gradient(circle at top left, rgba(13, 110, 253, 0.05), transparent 35%),
    #fff;
}

.premium-input {
  border-color: rgba(148, 163, 184, 0.22);
}

.premium-input:focus {
  box-shadow: none;
  border-color: #0d6efd;
}

.premium-note {
  border-color: rgba(148, 163, 184, 0.18) !important;
  background: linear-gradient(180deg, #fff 0%, #fbfdff 100%) !important;
}

.premium-action {
  border-color: rgba(13, 110, 253, 0.22);
}

.premium-table thead th {
  color: #475569;
  font-size: 0.78rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  border-bottom-color: rgba(148, 163, 184, 0.2);
}

.premium-table tbody td {
  padding-top: 1rem;
  padding-bottom: 1rem;
}

.premium-mobile-card {
  border-radius: 0;
  border-color: rgba(148, 163, 184, 0.18) !important;
  background: linear-gradient(180deg, #fff 0%, #fbfdff 100%);
}

@media (max-width: 767.98px) {
  .premium-hero {
    padding: 1rem 1.1rem;
    border-radius: 1.15rem;
  }

  .premium-panel-header {
    padding-top: 1.1rem !important;
  }
}
</style>
