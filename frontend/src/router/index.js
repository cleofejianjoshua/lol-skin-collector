import { createRouter, createWebHistory } from "vue-router";
import HomeView from "@/views/HomeView.vue";
import LoginView from "@/views/LoginView.vue";
import RegisterView from "@/views/RegisterView.vue";
import DashboardView from "@/views/DashboardView.vue";
import ProfileView from "@/views/ProfileView.vue";
import UpdateProfileView from "@/views/UpdateProfileView.vue";
import GachaView from "@/views/GachaView.vue";
import ShardsView from "@/views/ShardsView.vue";

const routes = [
  { path: "/",               name: "Home",          component: HomeView },
  { path: "/login",          name: "Login",         component: LoginView },
  { path: "/register",       name: "Register",      component: RegisterView },
  { path: "/dashboard",      name: "Dashboard",     component: DashboardView },
  { path: "/profile",        name: "Profile",       component: ProfileView },
  { path: "/profile/update", name: "UpdateProfile", component: UpdateProfileView },
  { path: "/gacha",          name: "Gacha",         component: GachaView },
  { path: "/shards",         name: "Shards",        component: ShardsView },
];


const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Navigation guard — checks auth on every route change
router.beforeEach(async (to, from, next) => {
  const publicRoutes = ["/login", "/register"];

  try {
    const res = await fetch("/api/user", {
      credentials: "include",
      method: "GET",
    });

    const isLoggedIn = res.ok;

    // Already logged in → redirect away from login/register
    if (isLoggedIn && publicRoutes.includes(to.path)) {
      return next("/");
    }

    // Not logged in → redirect to login (except public routes)
    if (!isLoggedIn && !publicRoutes.includes(to.path)) {
      return next("/login");
    }

    next();
  } catch {
    if (!publicRoutes.includes(to.path)) {
      return next("/login");
    }
    next();
  }
});

export default router;