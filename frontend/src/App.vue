<template>
  <div class="app-root">
    <header class="top-bar">
      <span class="brand">LOL Skin Gacha Collector</span>
      <nav class="nav-links">
        <router-link to="/index">Home</router-link>
        <router-link to="/login">Log In</router-link>
        <router-link to="/register">Register</router-link>
        <!-- Log Out link would be wired to your auth logic -->
        <a href="#" @click.prevent="onLogout">Log Out</a>
      </nav>
    </header>

    <main class="page-content">
      <router-view />
    </main>

    <!-- Simple placeholder for flash messages;
         later you can bind this to real API responses -->
    <ul v-if="flashMessages.length" class="flash-list">
      <li v-for="(msg, i) in flashMessages" :key="i">{{ msg }}</li>
    </ul>
  </div>
</template>

<script setup>
import { ref } from "vue";

const flashMessages = ref([]);

// Stub for now – later, integrate with your auth/logout API
const onLogout = () => {
  flashMessages.value.push("Logged out (frontend stub).");
};
</script>
