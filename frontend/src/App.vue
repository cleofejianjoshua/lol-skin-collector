<script setup>
import { ref, onMounted, computed, watch } from "vue";
import { useRoute, useRouter } from "vue-router";

const username = ref("Guest");
const flashMessages = ref([]);
const route = useRoute();
const router = useRouter();

const isLoggedIn = computed(() => {
  return username.value && username.value !== "Guest";
});

const loadingUser = ref(true);

const fetchUser = async () => {
  try {
    const res = await fetch("/api/user", {
      credentials: "include"
    });
    const data = await res.json();
    if (data.username) {
      username.value = data.username;
    } else {
      username.value = "Guest";
    }
  } catch (e) {
    username.value = "Guest";
  } finally {
    loadingUser.value = false;
  }
};

const onLogout = async () => {
  try {
    const res = await fetch("/auth/logout", {
      method: "POST",
      credentials: "include"
    });

    const data = await res.json();
    console.log(data.message);

    username.value = "Guest";
    router.push({ name: "Login" });
  } catch (err) {
    console.error("Logout failed:", err);
  }
};

onMounted(() => {
  fetchUser();
});

// Refetch user when route changes (after login)
watch(() => route.fullPath, () => {
  fetchUser();
});
</script>

<template>
  <div class="app-root">
    
    <!-- NAVBAR -->
    <header v-if="!loadingUser" class="top-bar">
      <span class="brand">LOL Skin Gacha Collector</span>

      <!-- LOGGED IN NAVBAR -->
      <nav v-if="isLoggedIn" class="nav-links">
        <span class="welcome-text">Welcome, {{ username }}! | </span>
        <router-link to="/">Home</router-link>
        <router-link to="/dashboard">Dashboard</router-link>
        <router-link to="/profile">Profile</router-link>
        <a href="#" @click.prevent="onLogout">Sign out</a>
      </nav>

      <!-- NOT LOGGED IN NAVBAR -->
      <nav v-else class="nav-links">
        <router-link to="/login">Log In</router-link>
        <router-link to="/register">Register</router-link>
      </nav>
    </header>

    <!-- PAGE CONTENT -->
    <main class="page-content">
      <router-view />
    </main>

    <!-- FLASH MESSAGES (optional) -->
    <ul v-if="flashMessages.length" class="flash-list">
      <li v-for="(msg, i) in flashMessages" :key="i">
        {{ msg }}
      </li>
    </ul>

  </div>
</template>

<style>
/* Global button hover effects */
.primary-btn,
button.primary-btn,
.nav-links a,
.nav-links .link-button,
.link-button {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.primary-btn:hover,
button.primary-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(96, 165, 250, 0.4);
}

.nav-links a:hover,
.nav-links .link-button:hover,
.link-button:hover {
  transform: translateY(-1px);
}
</style>
