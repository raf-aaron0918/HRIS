<template>
  <div class="auth-main">
    <div class="auth-wrapper v3">
      <div class="auth-form">
        <div class="card my-5">
          <div class="card-body">
            <div class="mb-4">
              <h3 class="mb-2"><b>Sign in to HRIS</b></h3>
              <p class="text-muted mb-0">
                Use your company account to access employee records, attendance, leave, payroll, and reports.
              </p>
            </div>
            <div class="form-group mb-3">
              <label class="form-label">Email or Employee ID</label>
              <input v-model="form.identifier" type="text" class="form-control" placeholder="Enter your email or employee ID" />
            </div>
            <div class="form-group mb-3">
              <label class="form-label">Password</label>
              <input v-model="form.password" type="password" class="form-control" placeholder="Enter your password" />
            </div>
            <div class="d-flex mt-1 justify-content-between align-items-center">
              <div class="form-check">
                <input id="rememberMe" v-model="form.remember" class="form-check-input input-primary" type="checkbox" />
                <label class="form-check-label text-muted" for="rememberMe">Remember me</label>
              </div>
              <a href="#" class="link-primary">Forgot Password?</a>
            </div>
            <div class="d-grid mt-4">
              <button type="button" class="btn btn-primary" :disabled="isSubmitting" @click="handleLogin">
                {{ isSubmitting ? "Signing In..." : "Sign In" }}
              </button>
            </div>
            <div v-if="message" class="alert mt-4 mb-0" :class="messageClass">{{ message }}</div>
          </div>
        </div>
        <div class="auth-footer row">
          <div class="col my-1">
            <p class="m-0 text-muted">HRIS secure access for authorized users and administrators.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, reactive, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import { ApiError } from "@/lib/api";
import { useAuthStore } from "@/stores/auth";

const router = useRouter();
const route = useRoute();
const authStore = useAuthStore();
const message = ref("");
const messageType = ref("success");
const isSubmitting = ref(false);
const form = reactive({
  identifier: "",
  password: "",
  remember: true,
});

const messageClass = computed(() =>
  messageType.value === "danger"
    ? "alert-light-danger border-danger"
    : "alert-light-success border-success"
);

async function handleLogin() {
  if (!form.identifier.trim() || !form.password.trim()) {
    messageType.value = "danger";
    message.value = "Enter your username and password to continue.";
    return;
  }

  isSubmitting.value = true;
  message.value = "";

  try {
    const user = await authStore.login({
      username: form.identifier.trim(),
      password: form.password,
    });

    messageType.value = "success";
    message.value = `Welcome back, ${user.full_name}. Redirecting to the HR dashboard.`;

    window.setTimeout(() => {
      router.push(typeof route.query.redirect === "string" ? route.query.redirect : "/dashboard");
    }, 350);
  } catch (error) {
    messageType.value = "danger";
    if (error instanceof ApiError && error.status === 401) {
      message.value = "Incorrect username or password.";
    } else {
      message.value = "The API is unavailable. Start the FastAPI backend and try again.";
    }
  } finally {
    isSubmitting.value = false;
  }
}
</script>
