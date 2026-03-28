import { createRouter, createWebHistory } from "vue-router";
import HomePage from "../components/HomePage.vue";
import LoginPage from "../components/LoginPage.vue";
import RegisterPage from "../components/RegisterPage.vue";
import LoginSuccess from "../components/LoginSuccess.vue";
import Dashboard from "../components/Dashboard.vue";
import ProfilePage from "../components/ProfilePage.vue";
import UpdateProfile from "../components/UpdateProfile.vue";
import HomeUser from "../components/HomeUser.vue";
  
const routes = [
  { path: "/", name: "Home", component: HomePage },
  { path: "/index", redirect: "/" },
  { path: "/login", name: "Login", component: LoginPage },
  { path: "/register", name: "Register", component: RegisterPage },
  { path: "/dashboard", name: "Dashboard", component: Dashboard },
  { path: "/login/success", name: "LoginSuccess", component: LoginSuccess },
  { path: "/profile", name: "Profile", component: ProfilePage },
  { path: "/profile/update", name: "UpdateProfile", component: UpdateProfile },
  { path: "/home", name: "HomeUser", component: HomeUser }

];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;