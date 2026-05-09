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
        <div
          v-for="(slot, idx) in displaySlots"
          :key="idx"
          class="showcase-card"
          :class="slot ? slot.rarity : ''"
        >
          <div class="card-inner">
            <!-- Filled slot -->
            <template v-if="slot">
              <div class="slot-art-bg" :class="slot.rarity"></div>
              <div class="slot-skin-info">
                <p class="slot-champ">{{ slot.champion }}</p>
                <p class="slot-name">{{ slot.name }}</p>
                <span class="slot-rarity-pill" :class="slot.rarity">{{ slot.rarity.toUpperCase() }}</span>
              </div>
              <p class="slot-num-label">Slot {{ idx + 1 }}</p>
            </template>
            <!-- Empty slot -->
            <div v-else class="empty-state">
              <div class="plus-circle">+</div>
              <p>Slot {{ idx + 1 }}</p>
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

const SLOTS_KEY = "lol_display_slots";

const username     = ref("");
const nickname     = ref("");
const isLoading    = ref(true);
const displaySlots = ref([null, null, null, null]);

const displayName = computed(() => nickname.value || username.value);
const isLoggedIn  = computed(() => username.value && username.value !== "Guest");

function loadSlots() {
  const saved = localStorage.getItem(SLOTS_KEY);
  if (saved) displaySlots.value = JSON.parse(saved);
}

onMounted(async () => {
  loadSlots();
  try {
    const data = await fetchUser();
    username.value = data.username || "Guest";
    nickname.value = data.nickname || "";
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

.showcase-card.rare      { border-color: rgba(59,130,246,0.4); }
.showcase-card.epic      { border-color: rgba(168,85,247,0.45); }
.showcase-card.legendary { border-color: rgba(234,179,8,0.5); box-shadow: 0 0 30px rgba(234,179,8,0.15); }

.showcase-card:hover {
  transform: translateY(-8px);
  border-color: var(--accent);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4), 0 0 20px rgba(59, 130, 246, 0.2);
}

.card-inner {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  overflow: hidden;
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

/* Filled slot styles */
.slot-art-bg {
  position: absolute;
  inset: 0;
  border-radius: 38px;
}
.slot-art-bg.common    { background: linear-gradient(160deg, #1e293b 0%, #0f172a 100%); }
.slot-art-bg.rare      { background: linear-gradient(160deg, #1e3a8a 0%, #0f172a 100%); }
.slot-art-bg.epic      { background: linear-gradient(160deg, #581c87 0%, #1e293b 100%); }
.slot-art-bg.legendary { background: linear-gradient(160deg, #92400e 0%, #1e293b 100%); }

.slot-skin-info {
  position: relative;
  z-index: 2;
  text-align: center;
  margin-top: auto;
  padding: 20px 16px 8px;
  background: linear-gradient(to top, rgba(5,10,25,0.95) 0%, transparent 100%);
  width: 100%;
}

.slot-champ {
  margin: 0 0 2px;
  font-size: 0.65rem;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.slot-name {
  margin: 0 0 8px;
  font-size: 0.88rem;
  font-weight: 700;
  color: var(--text-main);
  line-height: 1.2;
}

.slot-rarity-pill {
  font-size: 0.6rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  padding: 3px 9px;
  border-radius: 999px;
}
.slot-rarity-pill.common    { background: rgba(156,163,175,0.15); color: #d1d5db; border: 1px solid rgba(156,163,175,0.3); }
.slot-rarity-pill.rare      { background: rgba(59,130,246,0.15);  color: #93c5fd; border: 1px solid rgba(59,130,246,0.4); }
.slot-rarity-pill.epic      { background: rgba(168,85,247,0.15);  color: #d8b4fe; border: 1px solid rgba(168,85,247,0.4); }
.slot-rarity-pill.legendary { background: rgba(234,179,8,0.15);   color: #fde68a; border: 1px solid rgba(234,179,8,0.5); }

.slot-num-label {
  position: absolute;
  top: 14px; left: 14px;
  z-index: 3;
  margin: 0;
  font-size: 0.65rem;
  font-weight: 700;
  color: rgba(148,163,184,0.5);
  text-transform: uppercase;
  letter-spacing: 0.08em;
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
