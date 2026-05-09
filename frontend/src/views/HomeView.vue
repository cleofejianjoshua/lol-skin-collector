<template>
  <div v-if="!isLoading" class="home-page" :class="{ 'logged-in': isLoggedIn }">
    <!-- Header Section -->
    <header class="home-header">
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

      <QuoteCard v-if="isLoggedIn" class="home-quote" />
      <QuoteCard v-else />
    </header>

    <!-- Showcase Section (Only when logged in) -->
    <div v-if="isLoggedIn" class="showcase-container">
      <div class="showcase-grid">
        <div v-for="i in 4" :key="i" class="showcase-card">
          <div class="card-inner">
            <div class="empty-state">
              <div class="plus-circle">+</div>
              <p>No skin displayed</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import QuoteCard from "@/components/shared/QuoteCard.vue";
import { fetchUser } from "@/services/api.js";

const username = ref("");
const isLoading = ref(true);

const isLoggedIn = computed(() => username.value && username.value !== "Guest");

onMounted(async () => {
  try {
    const data = await fetchUser();
    username.value = data.username || "Guest";
  } finally {
    isLoading.value = false;
  }
});
</script>

<style scoped>
.home-page {
  max-width: 640px;
  padding: 48px 24px;
  margin: 0 auto;
  text-align: center;
  transition: max-width 0.5s ease;
}

.home-page.logged-in {
  max-width: 98vw;
  width: 100%;
}

.home-header {
  margin-bottom: 24px;
}

.home-page h1 {
  margin: 0 0 4px;
  font-size: 1.4rem;
  font-weight: 800;
  background: linear-gradient(135deg, #f9fafb, #93c5fd);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.home-subtitle {
  margin: 0 0 12px;
  color: var(--text-muted);
  font-size: 0.82rem;
}

.home-quote {
  max-width: 320px;
  margin: 0 auto;
  font-size: 0.75rem;
  opacity: 0.6;
}

/* Showcase Grid */
.showcase-container {
  margin-top: 0;
}

.showcase-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 60px;
  padding: 20px;
}

.showcase-card {
  min-height: 58vh;
  background: rgba(15, 23, 42, 0.6);
  border: 2px solid rgba(148, 163, 184, 0.2);
  border-radius: 40px;
  position: relative;
  overflow: hidden;
  transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
  backdrop-filter: blur(16px);
}

.showcase-card:hover {
  transform: translateY(-8px);
  border-color: var(--accent);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4), 0 0 20px rgba(59, 130, 246, 0.2);
}

.card-inner {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  color: rgba(148, 163, 184, 0.3);
  transition: color 0.3s ease;
}

.showcase-card:hover .empty-state {
  color: var(--accent);
}

.plus-circle {
  width: 54px;
  height: 54px;
  border-radius: 50%;
  border: 2px dashed currentColor;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  font-weight: 300;
}

.empty-state p {
  margin: 0;
  font-size: 0.9rem;
  font-weight: 600;
  letter-spacing: 0.05em;
  text-transform: uppercase;
}

@media (max-width: 1024px) {
  .showcase-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 640px) {
  .showcase-grid {
    grid-template-columns: 1fr;
  }
  .home-page h1 {
    font-size: 2rem;
  }
}
</style>
