<template>
  <div class="forge-page">
    <div class="forge-layout-wrapper">
      <!-- Left Slideshow -->
      <aside class="forge-side-panel left">
        <SkinSlideshow :skins="skins" :interval="5000" />
      </aside>

      <!-- Center Content -->
      <div class="forge-main-container">

        <!-- Header -->
        <div class="forge-header">
          <h1 class="forge-title">Gold Forge</h1>
          <p class="forge-subtitle">Click the coin to earn gold. Spend it on pulls.</p>
        </div>

        <!-- Gold counter -->
        <div class="gold-counter">
          <span class="gold-icon">🪙</span>
          <span class="gold-count">{{ gold }}</span>
          <span class="gold-label">Gold</span>
        </div>

        <!-- Click coin button -->
        <button
          class="coin-btn"
          :class="{ clicked: isClicked }"
          @click="clickGold"
          @mousedown="isClicked = true"
          @mouseup="isClicked = false"
          @mouseleave="isClicked = false"
        >
          <div class="coin-body">
            <span class="coin-emoji">🪙</span>
          </div>
        </button>

        <p class="click-hint">1 click = 1 gold</p>

        <p v-if="error" class="error-text">{{ error }}</p>

      </div>

      <!-- Right Slideshow -->
      <aside class="forge-side-panel right">
        <SkinSlideshow :skins="skins" :interval="5000" />
      </aside>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from "vue";
import { fetchSkins, fetchGold, addGold } from "@/services/api.js";
import SkinSlideshow from "@/components/shared/SkinSlideshow.vue";

const MOCK_POOL = [
  { name: "Spirit Blossom Ahri",  champion: "Ahri",   rarity: "legendary", image_path: "" },
  { name: "Arcane Jinx",          champion: "Jinx",   rarity: "epic",      image_path: "" },
  { name: "Pulsefire Ezreal",     champion: "Ezreal", rarity: "epic",      image_path: "" },
  { name: "Star Guardian Lux",    champion: "Lux",    rarity: "rare",      image_path: "" },
  { name: "Bewitching Jinx",      champion: "Jinx",   rarity: "rare",      image_path: "" },
  { name: "Base Ahri",            champion: "Ahri",   rarity: "common",    image_path: "" },
];

const gold          = ref(0);
const skins         = ref([]);
const isClicked     = ref(false);
const error         = ref("");
const pendingClicks = ref(0);
let syncTimer       = null;

onMounted(async () => {
  // Load gold from DB
  try {
    const data = await fetchGold();
    gold.value = data.gold ?? 0;
  } catch (err) {
    console.error("Failed to load gold:", err);
    error.value = "Failed to load gold balance.";
  }

  // Load skins for side panels
  try {
    const data = await fetchSkins();
    skins.value = data.map(s => ({
      ...s,
      name: s.skin_name || s.name,
      rarity: s.rarity_name || s.rarity
    }));
  } catch (err) {
    console.error("Failed to load skins for side panels:", err);
    skins.value = MOCK_POOL;
  }
});

onUnmounted(() => {
  if (syncTimer) clearTimeout(syncTimer);
  // Optional: final sync if leaving page with pending clicks
  if (pendingClicks.value > 0) syncToDB();
});

const clickGold = () => {
  gold.value++;
  pendingClicks.value++;
  error.value = "";

  // Debounce sync to DB
  if (syncTimer) clearTimeout(syncTimer);
  syncTimer = setTimeout(syncToDB, 1000); // Sync after 1s of no clicking
};

async function syncToDB() {
  if (pendingClicks.value === 0) return;
  
  const amountToSync = pendingClicks.value;
  pendingClicks.value = 0; // reset local pending
  
  try {
    const data = await addGold(amountToSync);
    // Overwrite only if we aren't currently clicking
    if (pendingClicks.value === 0) {
      gold.value = data.gold;
    }
  } catch (err) {
    console.error("Failed to sync gold:", err);
    error.value = "Sync error. Some gold may not have saved.";
    // Re-add to pending if failed? Or just leave it.
  }
}
</script>

<style scoped>
.forge-page {
  min-height: 80vh;
  position: relative;
  overflow-x: hidden;
  padding: 64px 0;
}

.forge-layout-wrapper {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  max-width: 100vw;
  margin: 0;
  padding: 0;
}

.forge-side-panel {
  position: fixed;
  top: 50%;
  transform: translateY(-50%);
  z-index: 5;
  display: block;
  width: 320px;
}

.forge-side-panel.left  { left: 180px; }
.forge-side-panel.right { right: 180px; }

.forge-main-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 48px;
  text-align: center;
}

@media (max-width: 1200px) {
  .forge-side-panel { display: none; }
}

.forge-title {
  margin: 0 0 8px;
  font-size: 3rem;
  font-weight: 800;
  background: linear-gradient(135deg, #fef9c3, #facc15, #ca8a04);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.forge-subtitle {
  margin: 0;
  font-size: 1.1rem;
  color: var(--text-muted);
}

/* Counter */
.gold-counter {
  display: flex;
  align-items: center;
  gap: 14px;
  background: rgba(15, 23, 42, 0.7);
  border: 1px solid rgba(250, 204, 21, 0.3);
  border-radius: 999px;
  padding: 16px 36px;
}

.gold-icon  { font-size: 1.8rem; }

.gold-count {
  font-size: 2.5rem;
  font-weight: 800;
  color: #fde68a;
  min-width: 80px;
  text-align: center;
}

.gold-label {
  font-size: 1rem;
  color: var(--text-muted);
  letter-spacing: 0.06em;
}

/* Coin button */
.coin-btn {
  position: relative;
  width: 220px;
  height: 220px;
  border-radius: 50%;
  border: none;
  background: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.1s ease;
  user-select: none;
}

.coin-btn:hover   { transform: scale(1.06); }
.coin-btn.clicked { transform: scale(0.93); }


.coin-body {
  width: 180px;
  height: 180px;
  border-radius: 50%;
  background: radial-gradient(circle at 32% 28%, #fef08a, #eab308 50%, #713f12);
  box-shadow: 0 10px 30px rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.15s ease;
}

.coin-btn:hover .coin-body {
  box-shadow: 0 15px 40px rgba(0,0,0,0.6);
}

.coin-btn.clicked .coin-body {
  box-shadow: 0 5px 15px rgba(0,0,0,0.4);
}

.coin-emoji {
  font-size: 5rem;
  pointer-events: none;
}

.click-hint {
  margin: 0;
  font-size: 1rem;
  color: rgba(156,163,175,0.5);
  letter-spacing: 0.06em;
}

.error-text {
  margin: 0;
  font-size: 0.9rem;
  color: #f87171;
}
</style>
