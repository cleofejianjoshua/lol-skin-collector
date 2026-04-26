import { createRouter, createWebHistory } from "vue-router";
import HomePage from "../components/HomePage.vue";
import LoginPage from "../components/LoginPage.vue";
import RegisterPage from "../components/RegisterPage.vue";
import Dashboard from "../components/Dashboard.vue";
import ProfilePage from "../components/ProfilePage.vue";
import UpdateProfile from "../components/UpdateProfile.vue";
import HomeUser from "../components/HomeUser.vue";

const routes = [
  { path: "/", name: "Home", component: HomeUser },
  { path: "/index", name: "Index", component: HomePage },
  { path: "/login", name: "Login", component: LoginPage },
  { path: "/register", name: "Register", component: RegisterPage },
  { path: "/dashboard", name: "Dashboard", component: Dashboard },
  { path: "/profile", name: "Profile", component: ProfilePage },
  { path: "/profile/update", name: "UpdateProfile", component: UpdateProfile }

];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Navigation guard to check authentication
router.beforeEach(async (to, from, next) => {
  // Check if user is logged in
  try {
    const res = await fetch('/api/user', {
      credentials: 'include',
      method: 'GET',
      headers: { 'Content-Type': 'application/json' }
    });

    const isLoggedIn = res.ok;

    // Redirect to home if trying to access login/register while logged in
    if (isLoggedIn && (to.path === '/login' || to.path === '/register')) {
      return next('/');
    }

    // Redirect to login if trying to access protected page while not logged in
    if (!isLoggedIn && to.path !== '/login' && to.path !== '/register') {
      return next('/login');
    }

    next();
  } catch (err) {
    // If fetch fails, assume not logged in
    if (to.path !== '/login' && to.path !== '/register') {
      return next('/login');
    }
    next();
  }
});

export default router;