import { createRouter, createWebHistory } from "vue-router";
import HomeView from "@/views/HomeView.vue";
import LoginView from "@/views/LoginView.vue";
import RegisterView from "@/views/RegisterView.vue";
import CollectionView from "@/views/CollectionView.vue";
import ProfileView from "@/views/ProfileView.vue";
import UpdateProfileView from "@/views/UpdateProfileView.vue";
import GachaView from "@/views/GachaView.vue";
import GoldForgeView from "@/views/GoldForgeView.vue";

const routes = [
  { path: "/", name: "Home", component: HomeView },
  { path: "/login", name: "Login", component: LoginView },
  { path: "/register", name: "Register", component: RegisterView },
  { path: "/collection", name: "Collection", component: CollectionView },
  { path: "/profile", name: "Profile", component: ProfileView },
  { path: "/profile/update", name: "UpdateProfile", component: UpdateProfileView },
  { path: "/gacha", name: "Gacha", component: GachaView },
  { path: "/gold-forge", name: "GoldForge", component: GoldForgeView },
];


const router = createRouter({
  history: createWebHistory(),
  routes,
});

// navigation guard, checks auth on every route change
router.beforeEach(async (to, from, next) => {
  const publicRoutes = ["/login", "/register"];

  try {
    const res = await fetch("/api/user", {
      credentials: "include",
      method: "GET",
    });

    const isLoggedIn = res.ok;

    // already logged in, redirect away from login/register
    if (isLoggedIn && publicRoutes.includes(to.path)) {
      return next("/");
    }

    // not logged in, redirect to login
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