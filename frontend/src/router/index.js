import { createRouter, createWebHistory } from "vue-router";
import HomePage from "../components/HomePage.vue";
import LoginPage from "../components/LoginPage.vue";
import RegisterPage from "../components/RegisterPage.vue";
import LoginSuccess from "../components/LoginSuccess.vue";
import Dashboard from "../components/Dashboard.vue";
  
const routes = [
  { path: "/", name: "Home", component: HomePage },
  { path: "/index", redirect: "/" },
  { path: "/login", name: "Login", component: LoginPage },
  { path: "/register", name: "Register", component: RegisterPage },
  { path: "/dashboard", name: "Dashboard", component: Dashboard },
  { path: "/login-success", name: "LoginSuccess", component: LoginSuccess },

];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;