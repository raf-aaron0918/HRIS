import { computed, ref } from "vue";
import { defineStore } from "pinia";
import { apiRequest } from "@/lib/api";

const TOKEN_KEY = "hris.accessToken";
const USER_KEY = "hris.currentUser";

export const useAuthStore = defineStore("auth", () => {
  const accessToken = ref("");
  const currentUser = ref(null);
  const hydrated = ref(false);

  const isAuthenticated = computed(() => Boolean(accessToken.value));

  function persistSession() {
    if (typeof window === "undefined") return;

    if (accessToken.value) {
      window.localStorage.setItem(TOKEN_KEY, accessToken.value);
    } else {
      window.localStorage.removeItem(TOKEN_KEY);
    }

    if (currentUser.value) {
      window.localStorage.setItem(USER_KEY, JSON.stringify(currentUser.value));
    } else {
      window.localStorage.removeItem(USER_KEY);
    }
  }

  function hydrate() {
    if (typeof window === "undefined") {
      hydrated.value = true;
      return;
    }

    accessToken.value = window.localStorage.getItem(TOKEN_KEY) || "";

    const savedUser = window.localStorage.getItem(USER_KEY);
    currentUser.value = savedUser ? JSON.parse(savedUser) : null;
    hydrated.value = true;
  }

  async function login(credentials) {
    const data = await apiRequest("/auth/login", {
      method: "POST",
      body: JSON.stringify(credentials),
    });

    accessToken.value = data.access_token;
    currentUser.value = data.user;
    persistSession();

    return data.user;
  }

  async function loadCurrentUser() {
    if (!accessToken.value) return null;

    const user = await apiRequest("/auth/me", {
      token: accessToken.value,
    });

    currentUser.value = user;
    persistSession();
    return user;
  }

  function logout() {
    accessToken.value = "";
    currentUser.value = null;
    persistSession();
  }

  return {
    accessToken,
    currentUser,
    hydrated,
    isAuthenticated,
    hydrate,
    loadCurrentUser,
    login,
    logout,
  };
});
