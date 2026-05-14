<template>
  <div v-if="!isLoading" class="home-page" :class="{ 'logged-in': isLoggedIn }">
    <!-- search others -->
    <div class="social-search-container" v-if="isLoggedIn">
      <div class="top-search-bar">
        <input 
          v-model="searchQuery" 
          type="text" 
          placeholder="Search player..." 
          class="search-input"
          @keyup.enter="handleSearch"
        />
        <button class="search-trigger-btn" @click="handleSearch">Search</button>
      </div>
      <button v-if="isViewingOthers" @click="resetToMyShowcase" class="back-btn small">
        Back to my Showcase
      </button>
    </div>

    <!-- header section -->
    <header class="home-header">
      <h1 v-if="isLoggedIn">
        <template v-if="isViewingOthers">Viewing {{ viewedUsername }}'s Showcase</template>
        <template v-else>Welcome Back, {{ displayName }}!</template>
      </h1>
      <h1 v-else>Welcome to LOL Skin Gacha Collector</h1>

      <p class="home-subtitle">
        <template v-if= "!isViewingOthers && isLoggedIn">
          Good to see you again, ready to collect some skins?
        </template>
      </p>

      <QuoteCard v-if="isLoggedIn" class="home-quote" />
      <QuoteCard v-else />
    </header>

    <!-- showcase section -->
    <div v-if="isLoggedIn" class="showcase-container">
      <div class="showcase-grid">
        <SkinCard
          v-for="(slot, idx) in displaySlots"
          :key="idx"
          :skin="slot"
          :isShard="!slot"
          :is-empty="!slot"
          :slot-number="idx + 1"
          :read-only="isViewingOthers"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import QuoteCard from "@/components/shared/QuoteCard.vue";
import SkinCard from "@/components/shared/SkinCard.vue";
import { fetchUser, fetchDisplaySlots, fetchOtherDisplaySlots, fetchOtherUser } from "@/services/api.js";

const username     = ref("");
const nickname     = ref("");
const isLoading    = ref(true);
const displaySlots = ref([null, null, null, null]);
const searchQuery = ref("");
const isViewingOthers = ref(false);
const viewedUsername = ref("");

const displayName = computed(() => {
  if (isViewingOthers.value) return viewedUsername.value;
  return nickname.value || username.value;
});
const isLoggedIn  = computed(() => username.value && username.value !== "Guest");

const handleSearch = async () => {
  if (!searchQuery.value) return;

  if (searchQuery.value === username.value) {
    resetToMyShowcase();
    return;
  }
  
  try {
    const slots = await fetchOtherDisplaySlots(searchQuery.value);
    const slotArray = [null, null, null, null];
    for (const s of slots) {
      slotArray[s.slot_index] = s.skin ?? null;
    }
    displaySlots.value = slotArray;
    viewedUsername.value = searchQuery.value;
    isViewingOthers.value = true;
  } catch (err) {
    alert("User not found or error fetching slots.");
  }
};

const loadMySlots = async () => {
  try {
    const slots = await fetchDisplaySlots();
    const slotArray = [null, null, null, null];
    if (slots.length) {
      for (const s of slots) {
        slotArray[s.slot_index] = s.skin ?? null;
      }
    }
    displaySlots.value = slotArray;
  } catch (err) {
    console.error("Error loading slots:", err);
  }
};

const resetToMyShowcase = async () => {
  isViewingOthers.value = false;
  searchQuery.value = "";
  await loadMySlots();
};

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
  position: relative;
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

/* search styles */
.social-search-container {
  position: absolute;
  top: 20px;
  left: 20px;
  z-index: 100;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 8px;
}

.top-search-bar {
  display: flex;
  align-items: center;
  gap: 10px;
}

.search-input {
  width: 100%;
  max-width: 220px;
  background: rgba(15, 23, 42, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.1);
  padding: 8px 10px;
  border-radius: 999px;
  color: #fff;
  font-size: 0.85rem;
  transition: all 0.2s ease;
}

.search-input:focus {
  outline: none;
  background: rgba(30, 41, 59, 0.8);
  border-color: rgba(59, 130, 246, 0.5);
  box-shadow: 0 0 15px rgba(59, 130, 246, 0.15);
}

.search-trigger-btn {
  background: radial-gradient(circle at 20% 0, #dbeafe, #60a5fa 40%, #1d4ed8);
  color: #0b1120;
  border: none;
  border-radius: 999px;
  padding: 8px 20px;
  font-size: 0.8rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
}

.search-trigger-btn:hover {
  filter: brightness(1.1);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

.back-btn {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: var(--text-muted);
  padding: 8px 24px;
  border-radius: 999px;
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.back-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  color: #fff;
  border-color: rgba(255, 255, 255, 0.2);
}

.back-btn.small {
  padding: 8px 26px;
  font-size: 0.8rem;
}

.home-quote {
  max-width: 320px;
  margin: 0 auto;
  font-size: 0.75rem;
  opacity: 0.6;
}

/* showcase Grid */
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
