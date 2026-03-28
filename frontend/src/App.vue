<script setup>
import { ref, onMounted, computed } from "vue";
import { useRoute, useRouter } from "vue-router";

const username = ref("Guest");
const flashMessages = ref([]);
const route = useRoute();
const router = useRouter();

const showNavbar = computed(() => route.name !== "LoginSuccess");
const isDashboard = computed(() => route.name === "Dashboard");
const isProfile = computed(() => route.name === "Profile");
const isUpdateProfile = computed(() => route.name === "UpdateProfile");
const isHomeUser = computed(() => route.name === "HomeUser");

const isLoggedIn = computed(() => {
  return username.value && username.value !== "Guest";
});

const loadingUser = ref(true); // loading state for user info

const onLogout = async () => {
  try {
    const res = await fetch("http://127.0.0.1:5000/api/logout", {
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

onMounted(async () => {
  try {
    const res = await fetch("http://127.0.0.1:5000/api/user", {
      credentials: "include"
    });
    const data = await res.json();
    username.value = data.username;
  } catch (e) {
    username.value = "Guest";
  } finally {
    loadingUser.value = false;
  }
});
</script>

<template>
  <div class="app-root">
    
    <!-- NAVBAR -->
    <header v-if="showNavbar" class="top-bar">
      <span class="brand">LOL Skin Gacha Collector</span>

      <!-- NAVBAR CHAIN -->
      <nav v-if="isDashboard || isProfile || isUpdateProfile || isHomeUser" class="nav-links">
        <router-link to="/home">Home</router-link>
        <router-link to="/dashboard">Dashboard</router-link>
        <router-link to="/profile">Profile</router-link>
        <a href="#" @click.prevent="onLogout">Sign out</a>
      </nav>

      <!-- NORMAL NAVBAR -->
      <nav v-else class="nav-links">
        <router-link to="/index">Home</router-link>

        <!-- NOT LOGGED IN -->
        <template v-if="!isLoggedIn">
          <router-link to="/login">Log In</router-link>
          <router-link to="/register">Register</router-link>
        </template>

        <!-- LOGGED IN -->
        <template v-else>
          <span class="welcome-text">Welcome, {{ username }}! | </span>
          <router-link to="/home">Home</router-link>
          <router-link to="/dashboard">Dashboard</router-link>
          <router-link to="/profile">Profile</router-link>
          <a href="#" @click.prevent="onLogout">Sign out</a>
        </template>
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
