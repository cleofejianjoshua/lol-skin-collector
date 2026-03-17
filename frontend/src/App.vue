<script setup>
import { ref, onMounted, computed } from "vue";
import { useRoute, useRouter } from "vue-router";

const username = ref("Loading...")
const flashMessages = ref([])
const route = useRoute();
const router = useRouter();

const showNavbar = computed(() => route.name !== "LoginSuccess");
const isDashboard = computed(() => route.name === "Dashboard");

const onLogout = () => {
  username.value = "Guest"
  router.push({ name: "Home" });
}

onMounted(async () => {
  const res = await fetch("http://127.0.0.1:5000/api/user")
  const data = await res.json()
  username.value = data.username
})
</script>

<template>
  <div class="app-root">
    <header v-if="showNavbar" class="top-bar">
      <span class="brand">LOL Skin Gacha Collector</span>

      <!-- Dashboard navbar -->
      <nav v-if="isDashboard" class="nav-links">
        <router-link to="/index">Home</router-link>
        <router-link to="/dashboard">Dashboard</router-link>
        <a href="#" @click.prevent="onLogout">Sign out</a>
      </nav>

      <!-- Home/Login/Register navbar -->
      <nav v-else class="nav-links">
        <router-link to="/index">Home</router-link>
        <router-link to="/login">Log In</router-link>
        <router-link to="/register">Register</router-link>
        <a href="#" @click.prevent="onLogout">Sign out</a>
      </nav>
    </header>

    <main class="page-content">
      <router-view />
    </main>

    <ul v-if="flashMessages.length" class="flash-list">
      <li v-for="(msg, i) in flashMessages" :key="i">
        {{ msg }}
      </li>
    </ul>
  </div>
</template>