import { createApp } from "vue";
import App from "./App.vue";
import "./assets/main.css";       // design tokens + base layout
import "./assets/css/index.css";  // all shared component styles
import router from "./router";

createApp(App).use(router).mount("#app");
