<template>
  <div v-if="!isLoading" class="home-page" :class="{ 'logged-in': isLoggedIn }">
    <!-- Header Section -->
    <header class="home-header">
      <h1 v-if="isLoggedIn">Welcome Back, {{ displayName }}!</h1>
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
        <SkinCard
          v-for="(slot, idx) in displaySlots"
          :key="idx"
          :skin="slot"
          :is-empty="!slot"
          :slot-number="idx + 1"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import QuoteCard from "@/components/shared/QuoteCard.vue";
import SkinCard from "@/components/shared/SkinCard.vue";
import { fetchUser, fetchDisplaySlots } from "@/services/api.js";

const username     = ref("");
const nickname     = ref("");
const isLoading    = ref(true);
const displaySlots = ref([null, null, null, null]);

const displayName = computed(() => nickname.value || username.value);
const isLoggedIn  = computed(() => username.value && username.value !== "Guest");

onMounted(async () => {
  try {
    const [userData, slots] = await Promise.all([
      fetchUser(),
      fetchDisplaySlots().catch(() => []),
    ]);

    username.value = userData.username || "Guest";
    nickname.value = userData.nickname || "";

    if (slots.length) {
      const slotArray = [null, null, null, null];
      for (const s of slots) {
        slotArray[s.slot_index] = s.skin ?? null;
      }
      displaySlots.value = slotArray;
    }
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
  background-clip: text;
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
  display: flex;
  justify-content: center;
  gap: 60px;
  padding: 20px;
  flex-wrap: wrap;
}

.showcase-grid :deep(.skin-card) {
  transition: transform 0.25s ease, box-shadow 0.25s ease;
}

.showcase-grid :deep(.skin-card):hover {
  transform: translateY(-10px);
  box-shadow: 0 30px 60px rgba(0, 0, 0, 0.6);
}

@media (max-width: 1024px) {
  .showcase-grid { gap: 24px; }
}

@media (max-width: 640px) {
  .home-page h1 { font-size: 2rem; }
}
</style>
