import { createApp, nextTick } from "vue";
import { createPinia } from "pinia";
import App from "./App.vue";
import router from "./router";
import { useAuthStore } from "@/stores/auth";
import "./styles/bridge.css";

function applyThemeDefaults() {
  if (typeof window.layout_change === "function") {
    window.layout_change("light");
  }
  if (typeof window.change_box_container === "function") {
    window.change_box_container("false");
  }
  if (typeof window.layout_rtl_change === "function") {
    window.layout_rtl_change("false");
  }
  if (typeof window.preset_change === "function") {
    window.preset_change("preset-1");
  }
  if (typeof window.font_change === "function") {
    window.font_change("Public-Sans");
  }
  if (window.feather && typeof window.feather.replace === "function") {
    window.feather.replace();
  }
}

const app = createApp(App);
const pinia = createPinia();

app.use(pinia);
app.use(router);

const authStore = useAuthStore(pinia);
authStore.hydrate();

router.afterEach(() => {
  nextTick(() => {
    applyThemeDefaults();
  });
});

app.mount("#app");

applyThemeDefaults();
