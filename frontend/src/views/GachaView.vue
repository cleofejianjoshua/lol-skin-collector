<template>
  <div class="gacha-page">

    <!-- Header -->
    <div class="gacha-header">
      <h1 class="gacha-title">Skin Gacha</h1>
      <p class="gacha-subtitle">Summon your destiny.</p>
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

    <!-- Pull area -->
    <div class="pull-area">

      <!-- Not enough shards warning -->
      <p v-if="notEnoughShards && !revealed" class="error-text">
        Not enough shards. Go earn more!
      </p>

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

      <!-- Post-reveal actions -->
      <div v-if="revealed" class="pull-actions">
        <button class="primary-btn" @click="resetPull">Pull Again</button>
      </div>

    </div>

    <!-- Rarity odds -->
    <div class="odds-card">
      <h3 class="odds-title">Drop Rates</h3>
      <div class="odds-list">
        <div class="odds-row" v-for="r in rarities" :key="r.name">
          <span class="odds-dot" :class="r.name"></span>
          <span class="odds-label">{{ r.label }}</span>
          <span class="odds-pct">{{ r.pct }}</span>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { gachaPull } from "@/services/api.js";

const PULL_COST   = 10;
const STORAGE_KEY = "lol_shards";

const shards    = ref(0);
const isPulling = ref(false);
const revealed  = ref(false);
const result    = ref(null);
const demoMode  = ref(false);

const notEnoughShards = computed(() => shards.value < PULL_COST);

const rarities = [
  { name: "legendary", label: "Legendary", pct: "5%"  },
  { name: "epic",      label: "Epic",      pct: "10%" },
  { name: "rare",      label: "Rare",      pct: "25%" },
  { name: "common",    label: "Common",    pct: "60%" },
];

onMounted(() => {
  const saved = localStorage.getItem(STORAGE_KEY);
  if (saved !== null) shards.value = parseInt(saved, 10);
});

// Mock pool for demo (no backend skins yet)
const MOCK_POOL = [
  { name: "Spirit Blossom Ahri",  champion: "Ahri",   rarity: "legendary", image_path: "" },
  { name: "Arcane Jinx",          champion: "Jinx",   rarity: "epic",      image_path: "" },
  { name: "Pulsefire Ezreal",     champion: "Ezreal", rarity: "epic",      image_path: "" },
  { name: "Star Guardian Lux",    champion: "Lux",    rarity: "rare",      image_path: "" },
  { name: "Bewitching Jinx",      champion: "Jinx",   rarity: "rare",      image_path: "" },
  { name: "Base Ahri",            champion: "Ahri",   rarity: "common",    image_path: "" },
  { name: "Base Jinx",            champion: "Jinx",   rarity: "common",    image_path: "" },
  { name: "Base Lux",             champion: "Lux",    rarity: "common",    image_path: "" },
];

const WEIGHTS = { common: 60, rare: 25, epic: 10, legendary: 5 };

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

  const delay = new Promise(res => setTimeout(res, 900));

  try {
    const [data] = await Promise.all([gachaPull(), delay]);
    result.value  = data;
    demoMode.value = false;
  } catch {
    await delay;
    result.value   = mockPull();
    demoMode.value = true;
  }

  // Deduct shards (UI only for now)
  shards.value -= PULL_COST;
  localStorage.setItem(STORAGE_KEY, shards.value);

  isPulling.value = false;
  revealed.value  = true;
};

const resetPull = () => {
  revealed.value  = false;
  result.value    = null;
  isPulling.value = false;
};
</script>

<style scoped>
/* Page */
.gacha-page {
  min-height: 80vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 28px;
  padding: 48px 24px;
}

.gacha-header { text-align: center; }

.gacha-title {
  margin: 0 0 6px;
  font-size: 2.2rem;
  font-weight: 800;
  background: linear-gradient(135deg, #dbeafe, #60a5fa, #a78bfa);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.gacha-subtitle {
  margin: 0;
  color: var(--text-muted);
  font-size: 0.9rem;
}

/* Shard info bar */
.shard-info {
  display: flex;
  align-items: center;
  gap: 12px;
  background: rgba(15, 23, 42, 0.6);
  border: 1px solid var(--border-subtle);
  border-radius: 999px;
  padding: 10px 22px;
  font-size: 0.88rem;
  color: var(--text-muted);
}

.shard-balance {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #a5b4fc;
  font-weight: 600;
}

.shard-icon { font-size: 1rem; }
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
  width: 280px;
  height: 380px;
  perspective: 1000px;
}

.card-face {
  position: absolute;
  inset: 0;
  border-radius: 20px;
  backface-visibility: hidden;
  -webkit-backface-visibility: hidden;
  transition: transform 0.75s cubic-bezier(0.4, 0, 0.2, 1);
  overflow: hidden;
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
  transform: rotateY(180deg);
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
  align-items: center;
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
  animation: shimmerSweep 1.5s cubic-bezier(0.4, 0, 0.2, 1) 0.4s forwards;
}

@keyframes shimmerSweep {
  0%   { transform: translateX(-150%) rotate(25deg) scale(2); }
  100% { transform: translateX(150%)  rotate(25deg) scale(2); }
}

.rarity-badge {
  position: absolute;
  top: 14px; right: 14px;
  font-size: 0.62rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  padding: 4px 10px;
  border-radius: 999px;
}

.rarity-badge.common    { background: rgba(156,163,175,0.15); color: #d1d5db; border: 1px solid rgba(156,163,175,0.3); }
.rarity-badge.rare      { background: rgba(59,130,246,0.15);  color: #93c5fd; border: 1px solid rgba(59,130,246,0.4); }
.rarity-badge.epic      { background: rgba(168,85,247,0.15);  color: #d8b4fe; border: 1px solid rgba(168,85,247,0.4); }
.rarity-badge.legendary { background: rgba(234,179,8,0.15);   color: #fde68a; border: 1px solid rgba(234,179,8,0.5); }

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

.card-container.flipped:hover .skin-img {
  transform: scale(1.05);
}

.skin-img-placeholder {
  width: 100%;
  height: 100%;
  background: linear-gradient(to bottom, #1e293b, #0f172a);
}

.skin-img-placeholder.rare      { background: linear-gradient(to bottom, #1e293b, #1e3a8a); }
.skin-img-placeholder.epic      { background: linear-gradient(to bottom, #1e293b, #581c87); }
.skin-img-placeholder.legendary { background: linear-gradient(to bottom, #1e293b, #713f12); }

.skin-info {
  width: 100%;
  text-align: center;
  background: linear-gradient(to top, rgba(5,10,25,0.95) 0%, transparent 100%);
  padding: 28px 16px 12px;
}

.skin-champion {
  margin: 0 0 2px;
  font-size: 0.72rem;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.skin-name {
  margin: 0;
  font-size: 1.05rem;
  font-weight: 700;
  color: var(--text-main);
}

.duplicate-tag {
  margin: 4px 0 0;
  font-size: 0.72rem;
  color: var(--text-muted);
}

/* Post-reveal */
.pull-actions { margin-top: 4px; }

.primary-btn { width: 180px; padding: 11px; }

/* Odds card */
.odds-card {
  background: rgba(15, 23, 42, 0.6);
  border: 1px solid var(--border-subtle);
  border-radius: 14px;
  padding: 18px 24px;
  min-width: 200px;
  backdrop-filter: blur(8px);
}

.odds-title {
  margin: 0 0 12px;
  font-size: 0.72rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--text-muted);
}

.odds-list { display: flex; flex-direction: column; gap: 8px; }

.odds-row {
  display: flex;
  align-items: center;
  gap: 10px;
}

.odds-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
}

.odds-dot.common    { background: #9ca3af; }
.odds-dot.rare      { background: #3b82f6; }
.odds-dot.epic      { background: #a855f7; }
.odds-dot.legendary { background: #eab308; box-shadow: 0 0 6px rgba(234,179,8,0.6); }

.odds-label { flex: 1; font-size: 0.83rem; color: var(--text-main); }
.odds-pct   { font-size: 0.83rem; font-weight: 600; color: var(--text-muted); }
</style>
