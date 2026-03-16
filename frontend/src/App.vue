<script setup>
import { ref, onMounted } from "vue"

const username = ref("Loading...")
const flashMessages = ref([])

const onLogout = () => {
  username.value = "Guest"
}

onMounted(async () => {
  const res = await fetch("http://127.0.0.1:5000/api/user")
  const data = await res.json()
  username.value = data.username
})
</script>

<template>
  <div class="app-root">
    <header class="top-bar">
      <span class="brand">LOL Skin Gacha Collector</span>

      <nav class="nav-links">
        <router-link to="/index">Home</router-link>
        <router-link to="/login">Log In</router-link>
        <router-link to="/register">Register</router-link>
        <a href="#" @click.prevent="onLogout">Log Out</a>
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