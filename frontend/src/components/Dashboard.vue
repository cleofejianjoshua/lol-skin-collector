<template>
  <div class="login-page">
    <div class="cards">
      <div class="brand">
        <div class="logo-circle">
          <span class="logo-text">LC</span>
        </div>
        <div class="brand-text">
          <h1>Dashboard Placeholder</h1>
          <p>Placeholder text for the dashboard</p>
        </div>
      </div>
      
      <p class="home-subtitle">
        Welcome to your dashboard. (You can view skins here later.)
      </p>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();

onMounted(async () => {
  try {
    const res = await fetch("/api/dashboard", { credentials: "include" });
    if (!res.ok) {
      router.push({ name: "Login" });
    }
  } catch {
    router.push({ name: "Login" });
  }
});
</script>

<style scoped>
.home-subtitle {
  margin: 0;
  color: var(--text-muted);
  font-size: 0.95rem;
  text-align: center;
}
</style>