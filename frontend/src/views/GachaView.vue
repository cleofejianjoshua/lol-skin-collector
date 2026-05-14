<template>
  <div class="gacha-page">
    <div class="gacha-layout-wrapper">
      <!-- left slideshow -->
      <aside class="gacha-side-panel left">
        <SkinSlideshow :skins="skins" :interval="5000" />
      </aside>

      <!-- center Content -->
      <div class="gacha-main-container">
        <!-- page glow overlay -->
        <div
          class="page-glow"
          :class="{
            'pulsing': isPulling,
            ['reveal-' + (result?.skin?.rarity?.name || result?.skin?.rarity)]: revealed
          }"
        ></div>

        <!-- header -->
        <div class="gacha-header">
          <h1 class="gacha-title">Skin Gacha</h1>
          <button class="history-btn" @click="openHistory" @mouseenter="pipSound.play()">
            History
          </button>
        </div>

        <!-- gold balance & cost -->
        <div class="gold-info">
          <div class="gold-balance">
            <span>{{ gold }} Gold</span>
          </div>
          <span class="gold-divider">·</span>
          <span class="gold-cost">Cost: <strong>{{ PULL_COST }} Gold</strong> per pull</span>
        </div>


        <!-- pull area -->
        <div class="pull-area">
          <!-- card -->
          <div 
            class="card-container" 
            :class="{ flipped: revealed, popped : popped }"
            @click="revealed && resetPull()"  
            :style="{ cursor: revealed ? 'pointer' : 'default' }"
          >
            <!-- back pull button -->
            <div class="card-face card-back">
              <!-- roulette display while pulling -->
              <div v-if="isPulling" class="roulette-display" :class="rouletteRarity">
                <div class="roulette-shimmer"></div>
                <div class="roulette-rarity-tag" :class="rouletteRarity">
                  <span v-if="rouletteRarity === 'ultimate'" class="ultimate-dot"></span>
                  {{ rouletteRarity.toUpperCase() }}
                </div>
                <div class="roulette-art">
                  <div class="roulette-placeholder" :class="rouletteRarity"></div>
                </div>
                <div v-if="showSkinName" class="roulette-skin-name">
                  {{ rouletteDisplaySkin?.name ?? '???' }}
                </div>
                <p class="card-hint">Summoning...</p>
              </div>

              <!-- normal pull button -->
              <template v-else>
                <button
                  class="pull-btn"
                  :class="{ pulling: isPulling, disabled: notEnoughGold, 'pity-pull': isPity }"
                  :disabled="isPulling || notEnoughGold"
                  @click="triggerPull"
                  @mouseenter="pipSound.play()"
                >
                  <div class="pull-orb">
                    <span class="pull-label">{{ isPity ? 'LUCKY PULL' : 'PULL' }}</span>
                  </div>
                </button>
                <p class="card-hint">Click to summon</p>
              </template>
            </div>

            <!-- front: result -->
            <div class="card-face card-front rarity-themed" :class="[result?.skin?.rarity.name, { 'is-gold-pull': !result?.is_duplicate }]" @mouseenter="pipSound.play()">
              <div v-if="result" class="result-inner">
                <div class="rarity-shimmer"></div>
                <span class="rarity-badge" :class="result.skin.rarity.name">
                  <span v-if="result.skin.rarity.name === 'ultimate'" class="ultimate-dot"></span>
                  {{ result.skin.rarity.name.toUpperCase() }}
                </span>

                <!-- gold badge top right -->
                <div class="gold-badge">GOLD</div>


                <!-- skin art -->
                <div class="skin-art-container">
                  <img
                    v-if="result.skin.image_path"
                    :src="result.skin.image_path"
                    :alt="result.skin.name"
                    class="skin-img"
                  />
                  <div v-else class="skin-img-placeholder" :class="result.skin.rarity.name"></div>
                </div>

                <div class="skin-info">
                  <p class="skin-champion">{{ result.skin.champion }}</p>
                  <h2 class="skin-name">{{ result.skin.name }}</h2>
                  <p v-if="result.is_duplicate" class="duplicate-tag">✦ Duplicate</p>
                </div>
              </div>
            </div>
          </div>
          
          <div class="gold-info" :class="{ pity: isPity }">
            <span class="gold-cost">
              <template v-if="isPity">
                <strong>Boosted rates active ↑↑</strong>
              </template>
              <template v-else>
                <strong>Boosted rates</strong> in <strong>{{ pulls_until_pity }}</strong> pull{{ pulls_until_pity !== 1 ? 's' : '' }}
              </template>
            </span>
          </div>

          <!-- rarity odds -->
          <div class="odds-card " :class="{ pity: isPity }">
            <div class="odds-list-horizontal">
              <div class="odds-item" v-for="r in displayedRarities" :key="r.name">
                <span class="odds-dot" :class="r.name"></span>
                <span class="odds-label-compact">{{ r.label }}:</span>
                <span class="odds-pct-compact">{{ r.pct }}</span>
              </div>
            </div>
          </div>

          <!-- not enough gold warning -->
          <p v-if="notEnoughGold && !revealed" class="error-text">
            Not enough gold. Go earn more!
          </p>

          <!-- post actions -->
          <div v-if="revealed" class="pull-actions">
            <button class="primary-btn" @click="resetPull" @mouseenter="pipSound.play()">Pull Again</button>
          </div>
        </div>
      </div>

      <!-- right slideshow -->
      <aside class="gacha-side-panel right">
        <SkinSlideshow :skins="skins" :interval="5000" />
      </aside>
    </div>
  </div>

  <!-- pull history modal -->
  <Teleport to="body">
    <Transition name="modal-fade">
      <div v-if="historyOpen" class="history-overlay" @click.self="closeHistory">
        <div class="history-modal">

          <!-- modal header -->
          <div class="history-modal-header">
            <div class="history-modal-title-group">
              <h2 class="history-modal-title">Pull History</h2>
            </div>
            <button class="history-close-btn" @click="closeHistory" aria-label="Close">✕</button>
          </div>
          <div class="history-divider"></div>

          <!-- loading state -->
          <div v-if="historyLoading" class="history-loading">
            <div class="history-spinner"></div>
            <span>Loading history…</span>
          </div>

          <!-- empty state -->
          <div v-else-if="historyData.total === 0" class="history-empty">
            <p>No pulls yet.<br/>Summon your first skin!</p>
          </div>

          <!-- table -->
          <template v-else>
            <table class="history-table">
              <thead>
                <tr>
                  <th>#</th>
                  <th>Skin</th>
                  <th>Rarity</th>
                  <th>Champion</th>
                  <th>Date</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="pull in historyData.pulls"
                  :key="pull.pull_number"
                  class="history-row"
                  :class="pull.rarity"
                >
                  <td class="col-num">{{ pull.pull_number }}</td>
                  <td class="col-skin">
                    <div class="skin-thumb-wrap">
                      <img
                        v-if="pull.image_path"
                        :src="pull.image_path"
                        :alt="pull.skin_name"
                        class="skin-thumb"
                      />
                      <div v-else class="skin-thumb-placeholder" :class="pull.rarity"></div>
                    </div>
                    <span class="skin-name-cell">{{ pull.skin_name }}</span>
                  </td>
                  <td class="col-rarity">
                    <span class="rarity-pill" :class="pull.rarity">
                      <span v-if="pull.rarity === 'ultimate'" class="ultimate-dot"></span>
                      {{ pull.rarity.charAt(0).toUpperCase() + pull.rarity.slice(1) }}
                    </span>
                  </td>
                  <td class="col-champion">{{ pull.champion }}</td>
                  <td class="col-date">{{ pull.obtained_at }}</td>
                </tr>
              </tbody>
            </table>

            <!-- pagination -->
            <div class="history-pagination">
              <button
                class="page-arrow"
                :disabled="historyPage <= 1"
                @click="changePage(historyPage - 1)"
                aria-label="Previous page"
              >◀</button>

              <span class="page-indicator">
                {{ historyPage }} <span class="page-sep">/</span> {{ historyData.total_pages }}
              </span>

              <button
                class="page-arrow"
                :disabled="historyPage >= historyData.total_pages"
                @click="changePage(historyPage + 1)"
                aria-label="Next page"
              >▶</button>
            </div>
          </template>

        </div>
      </div>
    </Transition>
  </Teleport>

</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { gachaPull, fetchSkins, fetchGold, spendGold, fetchGachaStatus, fetchPullHistory } from "@/services/api.js";
import SkinSlideshow from "@/components/shared/SkinSlideshow.vue";
import { useSound } from "@/services/sound.js";

const { pipSound, pullSound, revealSound, clickSound } = useSound();

const PULL_COST   = 25;

const gold      = ref(null);
const skins     = ref([]);
const isPulling = ref(false);
const revealed  = ref(false);
const result    = ref(null);
const demoMode  = ref(false);
const pulls_until_pity = ref(10);
const isPity = computed(() => pulls_until_pity.value === 1);
const showSkinName     = ref(true);
const rouletteRarity   = ref("common");
const rouletteSkins    = ref([]);
const popped = ref(false);
let rouletteInterval   = null;

// history modal state
const historyOpen    = ref(false);
const historyLoading = ref(false);
const historyPage    = ref(1);
const HISTORY_PAGE_SIZE = 5;
const historyData    = ref({ pulls: [], total: 0, page: 1, page_size: 5, total_pages: 1 });

async function loadHistory(page = 1) {
  historyLoading.value = true;
  try {
    historyData.value = await fetchPullHistory(page, HISTORY_PAGE_SIZE);
    historyPage.value = page;
  } catch (err) {
    console.error("Failed to load pull history:", err);
  } finally {
    historyLoading.value = false;
  }
}

function openHistory() {
  historyOpen.value = true;
  loadHistory(1);
  clickSound.play();
}

function closeHistory() {
  historyOpen.value = false;
  clickSound.play();
}

function changePage(page) {
  if (page < 1 || page > historyData.value.total_pages) return;
  loadHistory(page);
  pipSound.play();
}

const RARITY_ORDER = ["common", "rare", "epic", "legendary", "ultimate"];

const rouletteDisplaySkin = computed(() => {
  const pool = skins.value.filter(s => {
    const r = typeof s.rarity === 'object' ? s.rarity.name : s.rarity;
    return r === rouletteRarity.value;
  });
  if (!pool.length) return null;
  return pool[Math.floor(Math.random() * pool.length)];
});

function startRoulette() {
  // filter skins per rarity for name display
  rouletteSkins.value = skins.value;

  let speed = 60;
  let ticks  = 0;
  const totalTicks = 120;

  rouletteInterval = setInterval(() => {
    ticks++;
    pipSound.play();
    // pick weighted random rarity for visual effect
    const pool = isPity.value
      ? ["common","common","rare","rare","epic","epic","epic","legendary","ultimate"]
      : ["common","common","common","rare","rare","epic","legendary"];
    rouletteRarity.value = pool[Math.floor(Math.random() * pool.length)];

    // slow down toward the end
    if (ticks > totalTicks * 0.6) speed = 120;
    if (ticks > totalTicks * 0.85) speed = 220;

    if (ticks >= totalTicks) {
      clearInterval(rouletteInterval);
      rouletteInterval = null;
    }
  }, speed);
}

function stopRoulette() {
  if (rouletteInterval) {
    clearInterval(rouletteInterval);
    rouletteInterval = null;
  }
}

const notEnoughGold = computed(() => gold.value !== null && gold.value < PULL_COST);

const rarities = [
  { name: "common",    label: "Common",    pct: "40%" },
  { name: "rare",      label: "Rare",      pct: "32%" },
  { name: "epic",      label: "Epic",      pct: "18%" },
  { name: "legendary", label: "Legendary", pct: "9%"  },
  { name: "ultimate",  label: "Ultimate",  pct: "1%"  }
];

const displayedRarities = computed(() => {
  if (isPity.value) {
    return [
      { name: "common",    label: "Common",    pct: "0% ↓"  },
      { name: "rare",      label: "Rare",      pct: "15% ↓" },
      { name: "epic",      label: "Epic",      pct: "45% ↑" },
      { name: "legendary", label: "Legendary", pct: "36% ↑" },
      { name: "ultimate",  label: "Ultimate",  pct: "4% ↑"  },
    ];
  }
  return rarities;
});

onMounted(async () => {
  try {
    const [goldData, statusData] = await Promise.all([
      fetchGold(),
      fetchGachaStatus().catch(() => ({ pulls_until_pity: 10 })),
    ]);
    gold.value           = goldData.gold ?? 0;
    pulls_until_pity.value = statusData.pulls_until_pity;
  } catch (err) {
    console.error("Failed to load gacha data:", err);
  }

  // load skins for side panels
  try {
    const data = await fetchSkins();
    // map backend keys (skin_name -> name)
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

// mock pool for demo (no backend skins yet)
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
  if (isPulling.value || revealed.value || notEnoughGold.value) return;
  isPulling.value = true;
  startRoulette();
  pullSound.play();

  const delay = new Promise(res => setTimeout(res, 2000));

  try {
    const [data] = await Promise.all([gachaPull(), delay]);
    stopRoulette();
    rouletteRarity.value = data.skin.rarity;

    // preload image before flipping the card
    if (data.skin.image_path) {
      await new Promise(resolve => {
        const img = new Image();
        img.onload = resolve;
        img.onerror = resolve; // resolve anyway on error
        img.src = data.skin.image_path;
      });
    }

    result.value = {
      skin: { ...data.skin, name: data.skin.name || data.skin.skin_name, rarity: data.skin.rarity || data.skin.rarity_name },
      is_duplicate: data.is_duplicate,
    };
    gold.value             = data.gold;
    pulls_until_pity.value = data.pulls_until_pity;
    demoMode.value         = false;
  } catch {
    await delay;
    stopRoulette();
    result.value   = mockPull();
    demoMode.value = true;
  }

  isPulling.value = false;
  revealed.value  = true;
  revealSound.play();

  popped.value = true;
  setTimeout(() => { popped.value = false; }, 1000);
};

const resetPull = () => {
  revealed.value  = false;
  isPulling.value = false;
  // clear result after flip-back animation
  setTimeout(() => {
    if (!revealed.value) result.value = null;
  }, 1200);
  clickSound.play();
};
</script>

<style scoped>
/* page layout */
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

/* rarity reveal flashes */
.page-glow.reveal-common    { animation: flashCommon 2s ease-out forwards; opacity: 1; }
.page-glow.reveal-rare      { animation: flashRare 2s ease-out forwards; opacity: 1; }
.page-glow.reveal-epic      { animation: flashEpic 2s ease-out forwards; opacity: 1; }
.page-glow.reveal-legendary { animation: flashLegendary 2s ease-out forwards; opacity: 1; }
.page-glow.reveal-ultimate  { animation: flashUltimate 2s ease-out forwards; opacity: 1; }

@keyframes flashCommon {
  0% { background: rgba(255, 255, 255, 0.8); }
  5% { background: rgba(156, 163, 175, 0.4); }
  100% { background: transparent; }
}
@keyframes flashRare {
  0% { background: rgba(255, 255, 255, 0.9); }
  8% { background: rgba(59, 130, 246, 0.5); }
  100% { background: transparent; }
}
@keyframes flashEpic {
  0% { background: rgba(255, 255, 255, 1); }
  10% { background: rgba(168, 85, 247, 0.6); }
  100% { background: transparent; }
}
@keyframes flashLegendary {
  0% { background: rgba(255, 255, 255, 1); }
  12% { background: rgba(234, 179, 8, 0.7); }
  100% { background: transparent; }
}
@keyframes flashUltimate {
  0% { background: rgba(255, 255, 255, 1); box-shadow: inset 0 0 100px rgba(255,255,255,1); }
  15% { background: rgba(239, 68, 68, 0.8); }
  100% { background: transparent; }
}

.gacha-header { text-align: center; }

.gacha-title {
  margin: 0 0 4px;
  font-size: 3.5rem;
  font-weight: 800;
  background: linear-gradient(135deg, #dbeafe, #60a5fa, #a78bfa);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* gold info bar */
.gold-info {
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

.gold-info.pity {
  background: rgba(88, 28, 135, 0.25);
  border-color: rgba(168, 85, 247, 0.3);
}

.gold-balance {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #fbbf24;
  font-weight: 700;
  text-shadow: 0 0 10px rgba(251, 191, 36, 0.3);
}

.gold-icon { font-size: 0.85rem; }
.gold-divider { color: var(--border-subtle); }
.gold-cost strong { color: #fbbf24; }

/* pull area */
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
  border-radius: 0;
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

/* rarity border on front */
.card-front.common    { border-color: rgba(156,163,175,0.3); }
.card-front.rare      { border-color: rgba(59,130,246,0.5);  box-shadow: 0 0 30px rgba(59,130,246,0.2); }
.card-front.epic      { border-color: rgba(168,85,247,0.5);  box-shadow: 0 0 40px rgba(168,85,247,0.25); }
.card-front.legendary { border-color: rgba(234,179,8,0.6);   box-shadow: 0 0 60px rgba(234,179,8,0.35); }
.card-front.ultimate  { border-color: rgba(239,68,68,0.8);  box-shadow: 0 0 80px rgba(239,68,68,0.5); }

/* pull button */
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
  transition: transform 0.15s ease, box-shadow 0.5s ease, background 0.5s ease;
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

.pull-btn.pity-pull .pull-orb {
  background: radial-gradient(circle at 32% 28%, #c084fc, #a855f7 50%, #7e22ce);
  box-shadow: 0 0 36px rgba(168, 85, 247, 0.5);
}

.pull-btn.pity-pull .pull-label {
  color: #f3e8ff;
}

.pull-btn.pity-pull:not(.disabled):hover .pull-orb {
  transform: scale(1.08);
  box-shadow: 0 0 60px rgba(168, 85, 247, 0.75);
}

@keyframes orbPulsePity {
  0%, 100% { box-shadow: 0 0 36px rgba(168, 85, 247, 0.5); }
  50%       { box-shadow: 0 0 70px rgba(192, 132, 252, 0.85); }
}

.pull-btn.pity-pull.pulling .pull-orb {
  animation: orbPulsePity 0.8s ease-in-out infinite;
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

/* result card front */
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

.gold-badge {
  position: absolute;
  top: 16px; right: 16px;
  background: rgba(15, 23, 42, 0.7);
  backdrop-filter: blur(8px);
  color: #94a3b8;
  font-size: 0.65rem;
  font-weight: 800;
  padding: 3px 10px;
  border-radius: 999px;
  border: 1px solid rgba(255, 255, 255, 0.08);
  letter-spacing: 0.1em;
  text-transform: uppercase;
  z-index: 10;
}

.ultimate-dot {
  width: 6px;
  height: 6px;
  background: #ef4444;
  border-radius: 50%;
  box-shadow: 0 0 8px #ef4444;
}

/* skin art */
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

/* gold pull styling */
.is-gold-pull .skin-img {
  filter: brightness(.8);
  transition: filter 1s ease;
}

.gold-stamp-container {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%) scale(4);
  opacity: 0;
  z-index: 10;
  pointer-events: none;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.gold-stamp-container.stamp-active {
  transform: translate(-50%, -50%) scale(1) rotate(-15deg);
  opacity: 1;
}

.gold-stamp {
  font-size: 3.5rem;
  font-weight: 900;
  color: rgba(255, 255, 255, 0.15);
  border: 6px solid rgba(255, 255, 255, 0.15);
  padding: 8px 24px;
  text-transform: uppercase;
  letter-spacing: 0.15em;
  background: rgba(0, 0, 0, 0.2);
  backdrop-filter: blur(2px);
  box-shadow: 0 0 30px rgba(0, 0, 0, 0.4);
  text-shadow: 0 0 15px rgba(255, 255, 255, 0.1);
}

/* post-reveal */
.pull-actions { 
  animation: fadeIn 0.5s ease forwards;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.primary-btn { width: 180px; padding: 11px; }

/* odds card */
.odds-card {
  margin-bottom: 4px;
  background: rgba(15, 23, 42, 0.4);
  border: 1px solid var(--border-subtle);
  border-radius: 999px;
  padding: 8px 24px;
  backdrop-filter: blur(8px);
  transition: background 0.5s ease, border-color 0.5s ease;
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
  font-size: 0.8rem;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.odds-pct-compact {
  font-size: 0.95rem;
  font-weight: 800;
  color: var(--text-main);
  font-family: var(--font-mono, monospace);
}

.pull-btn.pity-pull ~ .odds-card,
.odds-card.pity {
  background: rgba(88, 28, 135, 0.25);
  border-color: rgba(168, 85, 247, 0.3);
}

/* roulette */
.roulette-display {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 16px;
  position: relative;
  overflow: hidden;
  transition: background 0.1s ease;
}

.roulette-display.common    { background: linear-gradient(135deg, rgba(30,30,35,0.9), #0f172a); }
.roulette-display.rare      { background: linear-gradient(135deg, rgba(15,30,60,0.9), #0f172a); }
.roulette-display.epic      { background: linear-gradient(135deg, rgba(40,10,65,0.9), #0f172a); }
.roulette-display.legendary { background: linear-gradient(135deg, rgba(55,35,5,0.9),  #0f172a); }
.roulette-display.ultimate  { background: linear-gradient(135deg, rgba(60,8,8,0.9),   #0f172a); }

.roulette-shimmer {
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, transparent 40%, rgba(255,255,255,0.04) 50%, transparent 60%);
  animation: shimmerSlide 0.4s linear infinite;
  pointer-events: none;
}

@keyframes shimmerSlide {
  0%   { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}

.card-container.popped {
  animation: cardPop 1s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
}

@keyframes cardPop {
  0%   { transform: scale(1)    translateY(0);    }
  40%  { transform: scale(1.08) translateY(-12px); }
  100% { transform: scale(1)    translateY(0);    }
}

.roulette-rarity-tag {
  padding: 6px 16px;
  border-radius: 999px;
  font-size: 0.75rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  border: 1px solid rgba(255,255,255,0.2);
  backdrop-filter: blur(4px);
  transition: all 0.1s ease;
}

.roulette-rarity-tag.common    { color: #d1d5db; background: rgba(30,30,35,0.75);  border-color: rgba(156,163,175,0.4); }
.roulette-rarity-tag.rare      { color: #93c5fd; background: rgba(15,30,60,0.8);   border-color: rgba(59,130,246,0.4); }
.roulette-rarity-tag.epic      { color: #d8b4fe; background: rgba(40,10,65,0.8);   border-color: rgba(168,85,247,0.4); }
.roulette-rarity-tag.legendary { color: #fde68a; background: rgba(55,35,5,0.85);   border-color: rgba(234,179,8,0.4); }
.roulette-rarity-tag.ultimate  { color: #ef4444; background: rgba(60,8,8,0.85);    border-color: rgba(239,68,68,0.5); box-shadow: 0 0 8px rgba(239,68,68,0.3); }

.roulette-art {
  width: 180px;
  height: 280px;
  overflow: hidden;
}

.roulette-placeholder {
  width: 100%;
  height: 100%;
  transition: background 0.1s ease;
}

.roulette-placeholder.common    { background: linear-gradient(135deg, #1e293b, #0f172a); }
.roulette-placeholder.rare      { background: linear-gradient(135deg, #1e3a8a, #0f172a); }
.roulette-placeholder.epic      { background: linear-gradient(135deg, #3b0764, #0f172a); }
.roulette-placeholder.legendary { background: linear-gradient(135deg, #422006, #0f172a); }
.roulette-placeholder.ultimate  { background: linear-gradient(135deg, #450a0a, #0f172a); }

.roulette-skin-name {
  font-size: 0.85rem;
  font-weight: 700;
  color: rgba(255,255,255,0.7);
  text-align: center;
  padding: 0 16px;
  transition: opacity 0.1s ease;
}

.toggle-name-btn {
  background: rgba(15, 23, 42, 0.4);
  border: 1px solid var(--border-subtle);
  border-radius: 999px;
  padding: 4px 14px;
  font-size: 0.7rem;
  font-weight: 600;
  color: var(--text-muted);
  cursor: pointer;
  transition: all 0.2s ease;
}

.toggle-name-btn:hover {
  color: #93c5fd;
  border-color: rgba(59,130,246,0.4);
}

/* history button */
.history-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: rgba(15, 23, 42, 0.55);
  border: 1px solid rgba(99, 155, 255, 0.25);
  border-radius: 999px;
  padding: 6px 16px;
  font-size: 0.78rem;
  font-weight: 700;
  color: #93c5fd;
  letter-spacing: 0.05em;
  cursor: pointer;
  transition: all 0.2s ease;
  backdrop-filter: blur(8px);
  margin-top: 6px;
}

.history-btn:hover {
  background: rgba(59, 130, 246, 0.18);
  border-color: rgba(99, 155, 255, 0.5);
  color: #bfdbfe;
  box-shadow: 0 0 14px rgba(59,130,246,0.2);
}

.history-btn-icon { font-size: 0.9rem; }

/* history modal overlay */
.history-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.72);
  backdrop-filter: blur(6px);
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.25s ease;
}
.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}
.modal-fade-enter-active .history-modal,
.modal-fade-leave-active .history-modal {
  transition: transform 0.25s cubic-bezier(0.34, 1.4, 0.64, 1);
}
.modal-fade-enter-from .history-modal {
  transform: scale(0.92) translateY(20px);
}
.modal-fade-leave-to .history-modal {
  transform: scale(0.95) translateY(10px);
}

/* history modal panel */
.history-modal {
  width: min(780px, 94vw);
  background: linear-gradient(145deg, rgba(10, 15, 30, 0.97), rgba(15, 22, 45, 0.97));
  border: 1px solid rgba(99, 155, 255, 0.2);
  border-radius: 16px;
  box-shadow: 0 30px 80px rgba(0,0,0,0.7), 0 0 40px rgba(59,130,246,0.08);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  max-height: 90vh;
}

.history-modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px 16px;
}

.history-modal-title-group {
  display: flex;
  align-items: center;
  gap: 10px;
}

.history-modal-icon { font-size: 1.2rem; }

.history-modal-title {
  margin: 0;
  font-size: 1.3rem;
  font-weight: 800;
  background: linear-gradient(135deg, #dbeafe, #93c5fd, #a78bfa);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: 0.04em;
}

.history-close-btn {
  background: none;
  border: none;
  color: #64748b;
  font-size: 1rem;
  cursor: pointer;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}
.history-close-btn:hover {
  background: rgba(239,68,68,0.15);
  color: #f87171;
}

.history-divider {
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(99,155,255,0.3) 40%, rgba(167,139,250,0.3) 60%, transparent);
  margin: 0 24px;
}

/* loading/empty */
.history-loading,
.history-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 14px;
  padding: 48px 24px;
  color: #64748b;
  font-size: 0.9rem;
  text-align: center;
  line-height: 1.6;
}

.history-empty-icon { font-size: 2.5rem; }

.history-spinner {
  width: 32px;
  height: 32px;
  border: 3px solid rgba(99,155,255,0.2);
  border-top-color: #60a5fa;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}
@keyframes spin {
  to { transform: rotate(360deg); }
}

/* history table */
.history-table {
  width: 100%;
  border-collapse: collapse;
  margin: 16px 0 0;
  padding: 0 24px;
  font-size: 0.82rem;
  display: table;
}

.history-table thead tr {
  background: rgba(255,255,255,0.03);
}

.history-table th {
  padding: 10px 16px;
  text-align: left;
  font-size: 0.7rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #475569;
  border-bottom: 1px solid rgba(255,255,255,0.06);
}

.history-table th:first-child { padding-left: 24px; }
.history-table th:last-child  { padding-right: 24px; }

.history-row {
  transition: background 0.15s ease;
  border-bottom: 1px solid rgba(255,255,255,0.04);
  animation: rowSlideIn 0.3s ease forwards;
  opacity: 0;
}

@keyframes rowSlideIn {
  from { opacity: 0; transform: translateX(-8px); }
  to   { opacity: 1; transform: translateX(0); }
}

.history-row:nth-child(1) { animation-delay: 0.04s; }
.history-row:nth-child(2) { animation-delay: 0.08s; }
.history-row:nth-child(3) { animation-delay: 0.12s; }
.history-row:nth-child(4) { animation-delay: 0.16s; }
.history-row:nth-child(5) { animation-delay: 0.20s; }

/* left rarity accent bar */
.history-row.common    { box-shadow: inset 3px 0 0 rgba(156,163,175,0.45); }
.history-row.rare      { box-shadow: inset 3px 0 0 rgba(59,130,246,0.6);  background: rgba(59,130,246,0.04); }
.history-row.epic      { box-shadow: inset 3px 0 0 rgba(168,85,247,0.6);  background: rgba(168,85,247,0.05); }
.history-row.legendary { box-shadow: inset 3px 0 0 rgba(234,179,8,0.7);   background: rgba(234,179,8,0.05); }
.history-row.ultimate  { box-shadow: inset 3px 0 0 rgba(239,68,68,0.8);   background: rgba(239,68,68,0.06); }

.history-row td {
  padding: 11px 16px;
  vertical-align: middle;
  color: #cbd5e1;
}

.history-table td:first-child { padding-left: 24px; }
.history-table td:last-child  { padding-right: 24px; }

.col-num {
  color: #475569;
  font-size: 0.7rem;
  font-weight: 700;
  font-family: monospace;
  width: 36px;
}

.col-skin {
  display: flex;
  align-items: center;
  gap: 10px;
  min-width: 0;
}

.skin-thumb-wrap {
  flex-shrink: 0;
  width: 36px;
  height: 36px;
  border-radius: 6px;
  overflow: hidden;
  border: 1px solid rgba(255,255,255,0.08);
}

.skin-thumb {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.skin-thumb-placeholder {
  width: 100%;
  height: 100%;
}
.skin-thumb-placeholder.common    { background: linear-gradient(135deg, #1e293b, #334155); }
.skin-thumb-placeholder.rare      { background: linear-gradient(135deg, #1e3a8a, #1e293b); }
.skin-thumb-placeholder.epic      { background: linear-gradient(135deg, #3b0764, #1e293b); }
.skin-thumb-placeholder.legendary { background: linear-gradient(135deg, #422006, #1e293b); }
.skin-thumb-placeholder.ultimate  { background: linear-gradient(135deg, #450a0a, #1e293b); }

.skin-name-cell {
  font-weight: 600;
  color: #e2e8f0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 160px;
}

.col-rarity { width: 100px; }

.rarity-pill {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 3px 10px;
  border-radius: 999px;
  font-size: 0.65rem;
  font-weight: 800;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.rarity-pill.common    { background: rgba(30,30,35,0.8);  color: #d1d5db; border: 1px solid rgba(156,163,175,0.3); }
.rarity-pill.rare      { background: rgba(15,30,60,0.8);  color: #93c5fd; border: 1px solid rgba(59,130,246,0.4); }
.rarity-pill.epic      { background: rgba(40,10,65,0.8);  color: #d8b4fe; border: 1px solid rgba(168,85,247,0.4); }
.rarity-pill.legendary { background: rgba(55,35,5,0.85); color: #fde68a; border: 1px solid rgba(234,179,8,0.5); }
.rarity-pill.ultimate  { background: rgba(60,8,8,0.85);  color: #ef4444; border: 1px solid rgba(239,68,68,0.6); box-shadow: 0 0 8px rgba(239,68,68,0.3); }

.col-champion {
  color: #94a3b8;
  font-size: 0.78rem;
}

.col-date {
  color: #475569;
  font-size: 0.72rem;
  font-family: monospace;
  white-space: nowrap;
}

/* pagination */
.history-pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px;
  padding: 18px 24px;
  border-top: 1px solid rgba(255,255,255,0.05);
  margin-top: 4px;
}

.page-arrow {
  width: 34px;
  height: 34px;
  border-radius: 50%;
  background: rgba(255,255,255,0.05);
  border: 1px solid rgba(99,155,255,0.2);
  color: #93c5fd;
  font-size: 0.75rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.page-arrow:not(:disabled):hover {
  background: rgba(59,130,246,0.2);
  border-color: rgba(99,155,255,0.5);
  box-shadow: 0 0 12px rgba(59,130,246,0.25);
}

.page-arrow:disabled {
  opacity: 0.25;
  cursor: not-allowed;
}

.page-indicator {
  font-size: 0.82rem;
  font-weight: 700;
  color: #cbd5e1;
  min-width: 60px;
  text-align: center;
  font-family: monospace;
  letter-spacing: 0.05em;
}

.page-sep {
  color: #475569;
  margin: 0 4px;
}
</style>
