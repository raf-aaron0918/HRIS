<template>
  <div>
    <BreadcrumbBar section="Administration" current="Accounts" />

    <div class="row g-3">
      <div class="col-12">
        <div class="card h-100">
          <div class="card-header d-flex align-items-center justify-content-between">
            <div>
              <h5 class="mb-0">Create Account</h5>
              <small class="text-muted">Add a login for HR Admin, Immediate Supervisor, or Payroll Admin users.</small>
            </div>
            <span class="badge" :class="roleBadgeClass">{{ currentRole }}</span>
          </div>
          <div class="card-body">
            <div v-if="!canManageAccounts" class="alert alert-light-warning border-warning mb-3" role="alert">
              Your current role can view this module, but only HR Admin accounts can create new logins.
            </div>

            <form novalidate @submit.prevent="handleSubmit">
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label class="form-label" for="accountFullName">Full Name</label>
                  <input id="accountFullName" v-model="form.fullName" type="text" class="form-control" placeholder="Employee full name" :disabled="!canManageAccounts || isSubmitting">
                </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label" for="accountUsername">Username</label>
                  <input id="accountUsername" v-model="form.username" type="text" class="form-control" placeholder="maria.santos" :disabled="!canManageAccounts || isSubmitting">
                </div>

                <div class="col-md-6 mb-3">
                  <label class="form-label" for="accountEmail">Email</label>
                  <input id="accountEmail" v-model="form.email" type="email" class="form-control" placeholder="maria.santos@company.com" :disabled="!canManageAccounts || isSubmitting">
                </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label" for="accountPassword">Temporary Password</label>
                  <input id="accountPassword" v-model="form.password" type="password" class="form-control" placeholder="Minimum 8 characters" :disabled="!canManageAccounts || isSubmitting">
                </div>

                <div class="col-md-6 mb-3">
                  <label class="form-label" for="accountRole">Role</label>
                  <select id="accountRole" v-model="form.role" class="form-select" :disabled="!canManageAccounts || isSubmitting">
                    <option v-for="option in roleOptions" :key="option" :value="option">{{ option }}</option>
                  </select>
                </div>
                <div class="col-md-6 mb-3 d-flex align-items-end">
                  <div class="border rounded-3 px-3 py-2 bg-light w-100">
                    <small class="text-muted d-block mb-1">Account status</small>
                    <strong>New accounts are created active by default.</strong>
                  </div>
                </div>
              </div>

              <div class="d-flex flex-wrap gap-2">
                <button type="button" class="btn btn-outline-primary" :disabled="isSubmitting" @click="resetFormWithMessage">Clear</button>
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

      <div class="col-lg-5 d-none">
        <div class="card h-100 border-0 shadow-sm">
          <div class="card-header bg-light-primary border-0">
            <h5 class="mb-0 text-primary">Account Preview</h5>
            <small class="text-muted">Check the login identity before saving it.</small>
          </div>
          <div class="card-body">
            <div class="p-3 rounded bg-light mb-3">
              <div class="d-flex justify-content-between align-items-center mb-2">
                <span class="text-muted">Display Name</span>
                <strong>{{ previewName }}</strong>
              </div>
              <div class="d-flex justify-content-between align-items-center mb-2">
                <span class="text-muted">Username</span>
                <strong>{{ previewUsername }}</strong>
              </div>
              <div class="d-flex justify-content-between align-items-center mb-2">
                <span class="text-muted">Role</span>
                <span class="badge bg-light-secondary text-secondary">{{ form.role }}</span>
              </div>
              <div class="d-flex justify-content-between align-items-center">
                <span class="text-muted">Access</span>
                <span class="badge" :class="form.isActive ? 'bg-light-success text-success' : 'bg-light-danger text-danger'">
                  {{ form.isActive ? "Active" : "Inactive" }}
                </span>
              </div>
            </div>

            <div class="border rounded p-3 mb-3">
              <h6 class="mb-2">Setup Notes</h6>
              <p class="text-muted small mb-2">Use a unique username and company email. The password entered here becomes the user’s first login password.</p>
              <p class="text-muted small mb-0">If you disable the account, the user record stays in the system but sign-in is blocked.</p>
            </div>

            <div class="border rounded p-3">
              <h6 class="mb-2">Recommended Flow</h6>
              <p class="text-muted small mb-2">1. Create the employee in Employee Master.</p>
              <p class="text-muted small mb-2">2. Add the user account here.</p>
              <p class="text-muted small mb-0">3. Share the temporary password and ask the user to sign in.</p>
            </div>
          </div>
        </div>
      </div>

      <div class="col-12">
        <div class="card h-100">
          <div class="card-header d-flex align-items-center justify-content-between">
            <div>
              <h5 class="mb-0">Existing Accounts</h5>
              <small class="text-muted">Review usernames, role assignment, and active status.</small>
            </div>
            <button type="button" class="btn btn-sm btn-light-primary" :disabled="isLoading" @click="fetchAccounts">Refresh</button>
          </div>
          <div class="card-body p-0">
            <div v-if="tableMessage" class="alert alert-light-warning border-warning m-3 mb-0" role="alert">
              {{ tableMessage }}
            </div>
            <div class="table-responsive">
              <table class="table table-hover mb-0">
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
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from "vue";
import BreadcrumbBar from "@/components/BreadcrumbBar.vue";
import { ApiError, apiRequest } from "@/lib/api";
import { useAuthStore } from "@/stores/auth";

const authStore = useAuthStore();
const accounts = ref([]);
const isLoading = ref(false);
const isSubmitting = ref(false);
const toggleUserId = ref(null);
const tableMessage = ref("");

const roleOptions = ["HR Admin", "Immediate Supervisor", "Payroll Admin"];

const alertState = reactive({
  class: "alert-light-primary border-primary",
  message: "Create a login for staff who need access to the HRIS modules.",
});

const form = reactive(createEmptyForm());

function createEmptyForm() {
  return {
    fullName: "",
    username: "",
    email: "",
    password: "",
    role: roleOptions[0],
    isActive: true,
  };
}

const currentRole = computed(() => authStore.currentUser?.role || "Authorized User");
const canManageAccounts = computed(() => currentRole.value === "HR Admin");

const previewName = computed(() => form.fullName.trim() || "No name yet");
const previewUsername = computed(() => form.username.trim() || "No username yet");

const roleBadgeClass = computed(() =>
  canManageAccounts.value ? "bg-light-success text-success" : "bg-light-warning text-warning"
);

function setAlert(type, message) {
  alertState.class = `alert-light-${type} border-${type}`;
  alertState.message = message;
}

function resetForm() {
  Object.assign(form, createEmptyForm());
}

function resetFormWithMessage() {
  resetForm();
  setAlert("primary", "Create a login for staff who need access to the HRIS modules.");
}

function validateForm() {
  if (!form.fullName.trim() || !form.username.trim() || !form.email.trim() || !form.password.trim()) {
    setAlert("danger", "Please complete the full name, username, email, and temporary password fields.");
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
  fetchAccounts();
});
</script>
