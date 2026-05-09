<template>
  <div class="shards-page">
    <div class="shards-layout-wrapper">
      <!-- Left Slideshow -->
      <aside class="shards-side-panel left">
        <SkinSlideshow :skins="skins" :interval="5000" />
      </aside>

      <!-- Center Content -->
      <div class="shards-main-container">

    <!-- Header -->
    <div class="shards-header">
      <h1 class="shards-title">Shard Forge</h1>
      <p class="shards-subtitle">Click the crystal to earn shards. Spend them on pulls.</p>
    </div>

    <!-- Shard counter -->
    <div class="shard-counter">
      <span class="shard-icon">💎</span>
      <span class="shard-count">{{ shards }}</span>
      <span class="shard-label">Shards</span>
    </div>

    <!-- Click crystal button -->
    <button
      class="crystal-btn"
      :class="{ clicked: isClicked }"
      @click="clickShard"
      @mousedown="isClicked = true"
      @mouseup="isClicked = false"
      @mouseleave="isClicked = false"
    >
      <div class="crystal-glow"></div>
      <div class="crystal-body">
        <span class="crystal-emoji">💎</span>
      </div>
    </button>

    <p class="click-hint">1 click = 1 shard</p>

      </div>

      <!-- Right Slideshow -->
      <aside class="shards-side-panel right">
        <SkinSlideshow :skins="skins" :interval="5000" />
      </aside>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { fetchSkins } from "@/services/api.js";
import SkinSlideshow from "@/components/shared/SkinSlideshow.vue";

const MOCK_POOL = [
  { name: "Spirit Blossom Ahri",  champion: "Ahri",   rarity: "legendary", image_path: "" },
  { name: "Arcane Jinx",          champion: "Jinx",   rarity: "epic",      image_path: "" },
  { name: "Pulsefire Ezreal",     champion: "Ezreal", rarity: "epic",      image_path: "" },
  { name: "Star Guardian Lux",    champion: "Lux",    rarity: "rare",      image_path: "" },
  { name: "Bewitching Jinx",      champion: "Jinx",   rarity: "rare",      image_path: "" },
  { name: "Base Ahri",            champion: "Ahri",   rarity: "common",    image_path: "" },
];

const STORAGE_KEY = "lol_shards";
const shards    = ref(0);
const skins     = ref([]);
const isClicked = ref(false);

onMounted(async () => {
  const saved = localStorage.getItem(STORAGE_KEY); // gets shard value from local storage, just a mini database
  if (saved !== null) shards.value = parseInt(saved, 10);

  // Load skins for side panels
  try {
    const data = await fetchSkins();
    skins.value = data.map(s => ({
      ...s,
      name: s.skin_name || s.name,
      rarity: s.rarity_name || s.rarity
    }));
  } catch (err) {
    console.error("Failed to load skins for shard side panels:", err);
    skins.value = MOCK_POOL;
  }
});

const clickShard = () => {
  shards.value++;
  localStorage.setItem(STORAGE_KEY, shards.value);
};
</script>

<style scoped>
.shards-page {
  min-height: 80vh;
  position: relative;
  overflow-x: hidden;
  padding: 64px 0;
}

.shards-layout-wrapper {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  max-width: 100vw;
  margin: 0;
  padding: 0;
}

.shards-side-panel {
  position: fixed;
  top: 50%;
  transform: translateY(-50%);
  z-index: 5;
  display: block;
  width: 320px;
}

.shards-side-panel.left {
  left: 180px;
}

.shards-side-panel.right {
  right: 180px;
}

.shards-main-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 48px;
  text-align: center;
}

@media (max-width: 1200px) {
  .shards-side-panel { display: none; }
}

.shards-title {
  margin: 0 0 8px;
  font-size: 3rem;
  font-weight: 800;
  background: linear-gradient(135deg, #dbeafe, #818cf8, #a78bfa);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.shards-subtitle {
  margin: 0;
  font-size: 1.1rem;
  color: var(--text-muted);
}

/* Counter */
.shard-counter {
  display: flex;
  align-items: center;
  gap: 14px;
  background: rgba(15, 23, 42, 0.7);
  border: 1px solid rgba(129, 140, 248, 0.25);
  border-radius: 999px;
  padding: 16px 36px;
}

.shard-icon  { font-size: 1.8rem; }

.shard-count {
  font-size: 2.5rem;
  font-weight: 800;
  color: #a5b4fc;
  min-width: 80px;
  text-align: center;
}

.shard-label {
  font-size: 1rem;
  color: var(--text-muted);
  letter-spacing: 0.06em;
}

/* Crystal button */
.crystal-btn {
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

.crystal-btn:hover   { transform: scale(1.06); }
.crystal-btn.clicked { transform: scale(0.93); }

.crystal-glow {
  position: absolute;
  inset: -16px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(129,140,248,0.3), transparent 70%);
  animation: glowPulse 2.5s ease-in-out infinite;
  pointer-events: none;
}

@keyframes glowPulse {
  0%, 100% { opacity: 0.6; transform: scale(1);    }
  50%       { opacity: 1;   transform: scale(1.12); }
}

.crystal-body {
  width: 180px;
  height: 180px;
  border-radius: 50%;
  background: radial-gradient(circle at 32% 28%, #c4b5fd, #7c3aed 50%, #4c1d95);
  box-shadow: 0 0 60px rgba(139,92,246,0.5), 0 20px 50px rgba(0,0,0,0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: box-shadow 0.15s ease;
}

.crystal-btn:hover .crystal-body {
  box-shadow: 0 0 90px rgba(167,139,250,0.8), 0 20px 50px rgba(0,0,0,0.6);
}

.crystal-btn.clicked .crystal-body {
  box-shadow: 0 0 40px rgba(139,92,246,0.4), 0 10px 30px rgba(0,0,0,0.6);
}

.crystal-emoji {
  font-size: 5rem;
  filter: drop-shadow(0 0 16px rgba(167,139,250,0.8));
  pointer-events: none;
}

.click-hint {
  margin: 0;
  font-size: 1rem;
  color: rgba(156,163,175,0.5);
  letter-spacing: 0.06em;
}
</style>
