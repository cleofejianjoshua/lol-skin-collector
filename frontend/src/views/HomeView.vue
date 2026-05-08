<template>
  <div class="home-page">
    <h1 v-if="isLoggedIn">Welcome Back, {{ username }}!</h1>
    <h1 v-else>Welcome to LOL Skin Gacha Collector</h1>

    <p class="home-subtitle">
      <template v-if="isLoggedIn">
        Good to see you again, ready to collect some skins?
      </template>
      <template v-else>
        Track your skins, remember your favorites, and never forget that one legendary you've always wanted.
      </template>
    </p>

    <QuoteCard />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import QuoteCard from "@/components/shared/QuoteCard.vue";
import { fetchUser } from "@/services/api.js";

const username = ref("");

const isLoggedIn = computed(() => username.value && username.value !== "Guest");

onMounted(async () => {
  const data = await fetchUser();
  username.value = data.username || "Guest";
});
</script>

<style scoped>
.home-page {
  max-width: 640px;
  padding: 32px 24px;
  margin: 0 auto;
  text-align: center;
}

.home-page h1 {
  margin-bottom: 8px;
  font-size: 2rem;
}

.home-subtitle {
  margin: 0 0 24px;
  color: var(--text-muted);
  font-size: 0.95rem;
}
</style>
