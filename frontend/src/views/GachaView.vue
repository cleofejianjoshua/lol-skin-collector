<template>
  <div class="gacha-page">
    <div class="gacha-layout-wrapper">
      <!-- Left Slideshow -->
      <aside class="gacha-side-panel left">
        <SkinSlideshow :skins="skins" :interval="5000" />
      </aside>

      <!-- Center Content -->
      <div class="gacha-main-container">
    <!-- Page Glow Overlay -->
    <div
      class="page-glow"
      :class="{
        'pulsing': isPulling,
        ['reveal-' + result?.skin?.rarity]: revealed
      }"
    ></div>

    <!-- Header -->
    <div class="gacha-header">
      <h1 class="gacha-title">Skin Gacha</h1>
    </div>

    <!-- Shard balance + cost -->
    <div class="shard-info">
      <div class="shard-balance">
        <span class="shard-icon">💎</span>
        <span>{{ shards }} Shards</span>
      </div>
      <span class="shard-divider">·</span>
      <span class="shard-cost">Cost: <strong>{{ PULL_COST }} Shards</strong> per pull</span>
    </div>

    <!-- Rarity odds -->
    <div class="odds-card">
      <div class="odds-list-horizontal">
        <div class="odds-item" v-for="r in rarities" :key="r.name">
          <span class="odds-dot" :class="r.name"></span>
          <span class="odds-label-compact">{{ r.label }}:</span>
          <span class="odds-pct-compact">{{ r.pct }}</span>
        </div>
      </div>
    </div>

    <!-- Pull area -->
    <div class="pull-area">

      <!-- Card -->
      <div class="card-container" :class="{ flipped: revealed }">

        <!-- Back: pull button -->
        <div class="card-face card-back">
          <button
            class="pull-btn"
            :class="{ pulling: isPulling, disabled: notEnoughShards }"
            :disabled="isPulling || notEnoughShards"
            @click="triggerPull"
          >
            <div class="pull-orb">
              <span class="pull-label">{{ isPulling ? '...' : 'PULL' }}</span>
            </div>
          </button>
          <p class="card-hint">{{ isPulling ? 'Summoning...' : 'Click to summon' }}</p>
        </div>

        <!-- Front: result -->
        <div class="card-face card-front" :class="result?.skin?.rarity">
          <div v-if="result" class="result-inner">
            <div class="rarity-shimmer"></div>

            <span class="rarity-badge" :class="result.skin.rarity">
              <span v-if="result.skin.rarity === 'ultimate'" class="ultimate-dot"></span>
              {{ result.skin.rarity.toUpperCase() }}
            </span>

            <!-- Skin Art -->
            <div class="skin-art-container">
              <img
                v-if="result.skin.image_path"
                :src="result.skin.image_path"
                :alt="result.skin.name"
                class="skin-img"
              />
              <div v-else class="skin-img-placeholder" :class="result.skin.rarity"></div>
            </div>

            <div class="skin-info">
              <p class="skin-champion">{{ result.skin.champion }}</p>
              <h2 class="skin-name">{{ result.skin.name }}</h2>
              <p v-if="result.is_duplicate" class="duplicate-tag">✦ Duplicate</p>
            </div>

          </div>
        </div>

      </div>

      <!-- Not enough shards warning -->
      <p v-if="notEnoughShards && !revealed" class="error-text">
        Not enough shards. Go earn more!
      </p>

      <!-- Post-reveal actions -->
      <div v-if="revealed" class="pull-actions">
        <button class="primary-btn" @click="resetPull">Pull Again</button>
      </div>

    </div>



      </div>

      <!-- Right Slideshow -->
      <aside class="gacha-side-panel right">
        <SkinSlideshow :skins="skins" :interval="5000" />
      </aside>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { gachaPull, fetchSkins } from "@/services/api.js";
import SkinSlideshow from "@/components/shared/SkinSlideshow.vue";

const PULL_COST   = 10;
const STORAGE_KEY = "lol_shards";

const shards    = ref(0);
const skins     = ref([]);
const isPulling = ref(false);
const revealed  = ref(false);
const result    = ref(null);
const demoMode  = ref(false);

const pullSound = typeof Audio !== 'undefined' ? new Audio('/sounds/sound_select.mp3') : null;
if (pullSound) pullSound.volume = 0.5;

const revealSound = typeof Audio !== 'undefined' ? new Audio('/sounds/sound_open.mp3') : null;
if (revealSound) revealSound.volume = 0.5;

const clickSound = typeof Audio !== 'undefined' ? new Audio('/sounds/sound_click.mp3') : null;
if (clickSound) revealSound.volume = 0.5;

const notEnoughShards = computed(() => shards.value < PULL_COST);

const rarities = [
  { name: "common",    label: "Common",    pct: "40%" },
  { name: "rare",      label: "Rare",      pct: "32%" },
  { name: "epic",      label: "Epic",      pct: "18%" },
  { name: "legendary", label: "Legendary", pct: "9%"  },
  { name: "ultimate",  label: "Ultimate",  pct: "1%"  }
];

onMounted(async () => {
  const saved = localStorage.getItem(STORAGE_KEY);
  if (saved !== null) shards.value = parseInt(saved, 10);

  // Load skins for side panels
  try {
    const data = await fetchSkins();
    // Map backend keys (skin_name -> name) if necessary
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

// Mock pool for demo (no backend skins yet)
const MOCK_POOL = [
  { name: "Elementalist Lux",     champion: "Lux",    rarity: "ultimate",  image_path: "" },
  { name: "Spirit Blossom Ahri",  champion: "Ahri",   rarity: "legendary", image_path: "" },
  { name: "Arcane Jinx",          champion: "Jinx",   rarity: "epic",      image_path: "" },
  { name: "Pulsefire Ezreal",     champion: "Ezreal", rarity: "epic",      image_path: "" },
  { name: "Star Guardian Lux",    champion: "Lux",    rarity: "rare",      image_path: "" },
  { name: "Bewitching Jinx",      champion: "Jinx",   rarity: "rare",      image_path: "" },
  { name: "Base Ahri",            champion: "Ahri",   rarity: "common",    image_path: "" },
  { name: "Base Jinx",            champion: "Jinx",   rarity: "common",    image_path: "" },
  { name: "Base Lux",             champion: "Lux",    rarity: "common",    image_path: "" },
];

const WEIGHTS = { common: 0, rare: 0, epic: 0, legendary: 0, ultimate: 100 };

function mockPull() {
  const total = Object.values(WEIGHTS).reduce((a, b) => a + b, 0);
  let roll = Math.random() * total;
  let rarity = "common";
  for (const [r, w] of Object.entries(WEIGHTS)) {
    roll -= w;
    if (roll <= 0) { rarity = r; break; }
  }
  const pool = MOCK_POOL.filter(s => s.rarity === rarity);
  return { skin: pool[Math.floor(Math.random() * pool.length)], is_duplicate: false };
}

const triggerPull = async () => {
  if (isPulling.value || revealed.value || notEnoughShards.value) return;
  isPulling.value = true;

  if (pullSound) {
    pullSound.currentTime = 0;
    pullSound.play().catch(e => console.log("Audio play failed:", e));
  }

  const delay = new Promise(res => setTimeout(res, 2000));

  try {
    const [data] = await Promise.all([gachaPull(), delay]);

    // Map backend response to match mock shape
    result.value = {
      skin: {
        ...data.skin,
        name:  data.skin.name  || data.skin.skin_name,
        rarity: data.skin.rarity || data.skin.rarity_name,
      },
      is_duplicate: data.is_duplicate,
    };
    demoMode.value = false;
  } catch {
    await delay;
    result.value   = mockPull();  // fallback to mock on backend failure
    demoMode.value = true;
  }

  shards.value -= PULL_COST;
  localStorage.setItem(STORAGE_KEY, shards.value);

  isPulling.value = false;
  revealed.value  = true;

  if (revealSound) {
    revealSound.currentTime = 0;
    revealSound.play().catch(e => console.log("Audio play failed:", e));
  }
};

const resetPull = () => {
  revealed.value  = false;
  isPulling.value = false;
  // Clear result after flip-back animation finishes (1.2s)
  setTimeout(() => {
    if (!revealed.value) result.value = null;
  }, 1200);
  if (clickSound) {
    clickSound.currentTime = 0;
    clickSound.play().catch(e => console.log("Audio play failed:", e));
  }
};
</script>

<style scoped>
/* Page Layout */
.gacha-page {
  min-height: 80vh;
  position: relative;
  overflow-x: hidden;
  padding: 20px 0;
}

.gacha-layout-wrapper {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  max-width: 100vw;
  margin: 0;
  padding: 0;
}

.gacha-side-panel {
  position: fixed;
  top: 50%;
  transform: translateY(-50%);
  z-index: 5;
  display: block;
  width: 320px;
}

.gacha-side-panel.left {
  left: 180px;
}

.gacha-side-panel.right {
  right: 180px;
}

.gacha-main-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

@media (max-width: 1200px) {
  .gacha-side-panel { display: none; }
}

.page-glow {
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 0;
  opacity: 0;
  transition: opacity 0.5s ease;
}

.page-glow.pulsing {
  background: radial-gradient(circle, rgba(255, 255, 255, 0.45) 0%, transparent 75%);
  animation: smoothPulse 2.2s ease-in-out infinite;
}

@keyframes smoothPulse {
  0%, 100% { opacity: 0.5; }
  50%       { opacity: 1; }
}

/* Rarity Reveal Flashes */
.page-glow.reveal-common    { animation: flashCommon 2s ease-out forwards; opacity: 1; }
.page-glow.reveal-rare      { animation: flashRare 2s ease-out forwards; opacity: 1; }
.page-glow.reveal-epic      { animation: flashEpic 2s ease-out forwards; opacity: 1; }
.page-glow.reveal-legendary { animation: flashLegendary 2s ease-out forwards; opacity: 1; }
.page-glow.reveal-ultimate  { animation: flashUltimate 2s ease-out forwards; opacity: 1; }

@keyframes flashCommon {
  0% { background: rgba(255, 255, 255, 0.4); }
  15% { background: rgba(156, 163, 175, 0.3); }
  100% { background: transparent; }
}
@keyframes flashRare {
  0% { background: rgba(255, 255, 255, 0.5); }
  15% { background: rgba(59, 130, 246, 0.35); }
  100% { background: transparent; }
}
@keyframes flashEpic {
  0% { background: rgba(255, 255, 255, 0.6); }
  15% { background: rgba(168, 85, 247, 0.4); }
  100% { background: transparent; }
}
@keyframes flashLegendary {
  0% { background: rgba(255, 255, 255, 0.7); }
  15% { background: rgba(234, 179, 8, 0.5); }
  100% { background: transparent; }
}
@keyframes flashUltimate {
  0% { background: rgba(255, 255, 255, 0.9); }
  15% { background: rgba(239, 68, 68, 0.6); }
  100% { background: transparent; }
}

.gacha-header { text-align: center; }

.gacha-title {
  margin: 0 0 4px;
  font-size: 1.6rem;
  font-weight: 800;
  background: linear-gradient(135deg, #dbeafe, #60a5fa, #a78bfa);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* Shard info bar */
.shard-info {
  display: flex;
  align-items: center;
  gap: 10px;
  background: rgba(15, 23, 42, 0.6);
  border: 1px solid var(--border-subtle);
  border-radius: 999px;
  padding: 6px 16px;
  font-size: 0.8rem;
  color: var(--text-muted);
}

.shard-balance {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #a5b4fc;
  font-weight: 600;
}

.shard-icon { font-size: 0.85rem; }
.shard-divider { color: var(--border-subtle); }
.shard-cost strong { color: var(--text-main); }

/* Pull area */
.pull-area {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

/* 3D card flip */
.card-container {
  width: 308px;
  height: 560px;
  perspective: 1200px;
  transform-style: preserve-3d;
}

.card-face {
  position: absolute;
  inset: 0;
  border-radius: 20px;
  backface-visibility: hidden;
  -webkit-backface-visibility: hidden;
  transition: transform 1.2s cubic-bezier(0.4, 0, 0.2, 1);
  overflow: hidden;
  will-change: transform;
  box-sizing: border-box;
}

.card-back {
  transform: rotateY(0deg);
  background: rgba(13, 18, 33, 0.8);
  border: 1px solid rgba(59, 130, 246, 0.2);
  backdrop-filter: blur(12px);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 20px;
}

.card-front {
  transform: rotateY(180deg) translateZ(1px);
  background: rgba(13, 18, 33, 0.9);
  border: 1px solid var(--border-subtle);
}

.card-container.flipped .card-back  { transform: rotateY(-180deg); }
.card-container.flipped .card-front { transform: rotateY(0deg); }

/* Rarity border on front */
.card-front.common    { border-color: rgba(156,163,175,0.3); }
.card-front.rare      { border-color: rgba(59,130,246,0.5);  box-shadow: 0 0 30px rgba(59,130,246,0.2); }
.card-front.epic      { border-color: rgba(168,85,247,0.5);  box-shadow: 0 0 40px rgba(168,85,247,0.25); }
.card-front.legendary { border-color: rgba(234,179,8,0.6);   box-shadow: 0 0 60px rgba(234,179,8,0.35); }
.card-front.ultimate  { border-color: rgba(239,68,68,0.8);  box-shadow: 0 0 80px rgba(239,68,68,0.5); }

/* Pull button / orb */
.pull-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0;
}

.pull-btn.disabled { opacity: 0.4; cursor: not-allowed; }

.pull-orb {
  width: 110px;
  height: 110px;
  border-radius: 50%;
  background: radial-gradient(circle at 32% 28%, #93c5fd, #3b82f6 50%, #1d4ed8);
  box-shadow: 0 0 36px rgba(59,130,246,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.15s ease, box-shadow 0.15s ease;
}

.pull-btn:not(.disabled):hover .pull-orb {
  transform: scale(1.08);
  box-shadow: 0 0 60px rgba(96,165,250,0.75);
}

.pull-btn:not(.disabled):active .pull-orb {
  transform: scale(0.94);
  box-shadow: 0 0 20px rgba(59,130,246,0.3);
}

.pull-btn.pulling .pull-orb {
  animation: orbPulse 0.8s ease-in-out infinite;
}

@keyframes orbPulse {
  0%, 100% { box-shadow: 0 0 36px rgba(59,130,246,0.5); }
  50%       { box-shadow: 0 0 70px rgba(96,165,250,0.85); }
}

.pull-label {
  font-size: 0.85rem;
  font-weight: 800;
  letter-spacing: 0.15em;
  color: #dbeafe;
}

.card-hint {
  margin: 0;
  font-size: 0.78rem;
  color: var(--text-muted);
}

/* Result card front */
.result-inner {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: flex-end;
  padding: 20px;
  position: relative;
  overflow: hidden;
}

.rarity-shimmer {
  position: absolute;
  inset: -100%;
  background: linear-gradient(
    135deg,
    transparent 35%,
    rgba(255, 255, 255, 0.1) 45%,
    rgba(255, 255, 255, 0.25) 50%,
    rgba(255, 255, 255, 0.1) 55%,
    transparent 65%
  );
  transform: translateX(-100%) rotate(25deg);
  pointer-events: none;
}

.flipped .rarity-shimmer {
  animation: shimmerSweep 2s cubic-bezier(0.4, 0, 0.2, 1) 0.8s forwards;
}

@keyframes shimmerSweep {
  0%   { transform: translateX(-150%) rotate(25deg) scale(2); }
  100% { transform: translateX(150%)  rotate(25deg) scale(2); }
}

.rarity-badge {
  position: absolute;
  top: 20px; left: 20px;
  font-size: 0.62rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  padding: 4px 10px;
  border-radius: 999px;
}

.rarity-badge.common    { background: rgba(30,30,35,0.85);   color: #d1d5db; border: 1px solid rgba(156,163,175,0.3); }
.rarity-badge.rare      { background: rgba(15,30,60,0.85);   color: #93c5fd; border: 1px solid rgba(59,130,246,0.4); }
.rarity-badge.epic      { background: rgba(40,10,65,0.85);   color: #d8b4fe; border: 1px solid rgba(168,85,247,0.4); }
.rarity-badge.legendary { background: rgba(55,35,5,0.9);     color: #fde68a; border: 1px solid rgba(234,179,8,0.5); }
.rarity-badge.ultimate  { background: rgba(60,8,8,0.9);      color: #ef4444; border: 1px solid rgba(239,68,68,0.6); box-shadow: 0 0 15px rgba(239,68,68,0.4); display: flex; align-items: center; gap: 6px; }

.ultimate-dot {
  width: 6px;
  height: 6px;
  background: #ef4444;
  border-radius: 50%;
  box-shadow: 0 0 8px #ef4444;
}

/* Skin art */
.skin-art-container {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: -1;
}

.skin-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
}


.skin-img-placeholder {
  width: 100%;
  height: 100%;
  background: linear-gradient(to bottom, #1e293b, #0f172a);
}

.skin-img-placeholder.rare      { background: linear-gradient(to bottom, #1e293b, #1e3a8a); }
.skin-img-placeholder.epic      { background: linear-gradient(to bottom, #1e293b, #581c87); }
.skin-img-placeholder.legendary { background: linear-gradient(to bottom, #1e293b, #713f12); }
.skin-img-placeholder.ultimate  { background: linear-gradient(to bottom, #1e293b, #450a0a); }

.skin-info {
  width: 100%;
  text-align: left;
  margin-top: auto;
  z-index: 2;
}

.skin-champion {
  margin: 0;
  font-size: 0.75rem;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.1em;
}

.skin-name {
  margin: 4px 0 0;
  font-size: 1.1rem;
  font-weight: 800;
  color: var(--text-main);
  line-height: 1.2;
}

.duplicate-tag {
  margin: 6px 0 0;
  font-size: 0.7rem;
  color: #94a3b8;
  text-transform: uppercase;
  font-weight: 700;
  letter-spacing: 0.05em;
}

/* Post-reveal */
.pull-actions { margin-top: 4px; }

.primary-btn { width: 180px; padding: 11px; }

/* Odds Card */
.odds-card {
  margin-bottom: 4px;
  background: rgba(15, 23, 42, 0.4);
  border: 1px solid var(--border-subtle);
  border-radius: 999px;
  padding: 4px 18px;
  backdrop-filter: blur(8px);
}

.odds-list-horizontal {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
  flex-wrap: wrap;
}

.odds-item {
  display: flex;
  align-items: center;
  gap: 6px;
}

.odds-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  flex-shrink: 0;
}

.odds-dot.common    { background: #9ca3af; }
.odds-dot.rare      { background: #3b82f6; }
.odds-dot.epic      { background: #a855f7; }
.odds-dot.legendary { background: #eab308; }
.odds-dot.ultimate  { background: #ef4444; }

.odds-label-compact {
  font-size: 0.64rem;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.odds-pct-compact {
  font-size: 0.68rem;
  font-weight: 700;
  color: var(--text-main);
}
</style>
