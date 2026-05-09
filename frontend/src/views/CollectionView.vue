<template>
  <div class="collection-page">

    <!-- Header -->
    <div class="page-header">
      <div class="header-title-row">
        <h1 class="page-title">Collection</h1>
        <span class="header-sep">|</span>
        <span class="page-title shards-label" v-if="!loading">Shards <span class="shard-num">{{ tokenBalance }}</span></span>
      </div>
      <p class="page-subtitle" v-if="!loading">
        {{ collection.length }} skin{{ collection.length !== 1 ? 's' : '' }} owned
      </p>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="feedback-state">
      <div class="spinner"></div>
      <p>Loading collection…</p>
    </div>

    <!-- Empty -->
    <div v-else-if="collection.length === 0" class="feedback-state">
      <p class="empty-msg">Your collection is empty.</p>
    </div>

    <!-- Gallery -->
    <div v-else class="skin-gallery">
      <div
        v-for="entry in collection"
        :key="entry.skin.name"
        class="skin-card"
        :class="entry.skin.rarity"
        @click="openModal(entry)"
        tabindex="0"
        role="button"
        @keydown.enter="openModal(entry)"
      >
        <span v-if="entry.count > 1" class="dupe-badge">×{{ entry.count }}</span>
        <span v-if="getSlotForSkin(entry.skin) !== null" class="slot-pip">
          Slot {{ getSlotForSkin(entry.skin) + 1 }}
        </span>
        <div class="card-art">
          <img v-if="entry.skin.image_path" :src="entry.skin.image_path" :alt="entry.skin.name" class="card-img" />
          <div v-else class="art-bg" :class="entry.skin.rarity"></div>
        </div>
        <div class="card-shimmer"></div>
        <div class="card-info">
          <p class="card-champ">{{ entry.skin.champion }}</p>
          <p class="card-name">{{ entry.skin.name }}</p>
          <span class="rarity-pill" :class="entry.skin.rarity">
            <span v-if="entry.skin.rarity === 'ultimate'" class="ultimate-dot"></span>
            {{ entry.skin.rarity.toUpperCase() }}
          </span>
        </div>
      </div>
    </div>

    <!-- Modal -->
    <Teleport to="body">
      <Transition name="modal-fade">
        <div v-if="selected" class="modal-backdrop" @click.self="closeModal">
          <div class="modal-panel" :class="selected.skin.rarity">
            <button class="modal-close" @click="closeModal">✕</button>

            <div class="modal-art-wrap">
              <img v-if="selected.skin.image_path" :src="selected.skin.image_path" :alt="selected.skin.name" class="modal-img" />
              <div v-else class="modal-art-bg" :class="selected.skin.rarity"></div>
              <span class="modal-rarity-badge" :class="selected.skin.rarity">
                <span v-if="selected.skin.rarity === 'ultimate'" class="ultimate-dot"></span>
                {{ selected.skin.rarity.toUpperCase() }}
              </span>
              <span v-if="selected.count > 1" class="modal-dupe">×{{ selected.count }}</span>
            </div>

            <div class="modal-details">
              <p class="modal-champ">{{ selected.skin.champion }}</p>
              <h2 class="modal-name">{{ selected.skin.name }}</h2>
              <p class="modal-worth">
                Worth <strong>{{ TOKEN_VALUES[selected.skin.rarity] }} Tokens</strong> when disenchanted
              </p>
              <p v-if="getSlotForSkin(selected.skin) !== null" class="modal-slot-info">
                Currently in Slot {{ getSlotForSkin(selected.skin) + 1 }}
              </p>

              <div class="modal-actions">
                <button class="disenchant-btn" @click="disenchant">
                  Disenchant:  +{{ TOKEN_VALUES[selected.skin.rarity] }} Tokens
                </button>

                <div class="display-slot-section">
                  <p class="section-label">Display on Home Page:</p>
                  <div class="slot-grid">
                    <button
                      v-for="i in 4"
                      :key="i"
                      class="slot-btn"
                      :class="{ 'slot-active': getSlotForSkin(selected.skin) === i - 1 }"
                      @click="setDisplaySlot(i - 1)"
                    >
                      Slot {{ i }}
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>

  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { fetchUserCollection } from "@/services/api.js";

const router = useRouter();

const TOKEN_VALUES = { common: 15, rare: 40, epic: 100, legendary: 250, ultimate: 600 };
const SLOTS_KEY    = "lol_display_slots";
const SHARDS_KEY   = "lol_shards";

const loading      = ref(true);
const collection   = ref([]);
const selected     = ref(null);
const displaySlots = ref([null, null, null, null]);
const tokenBalance = ref(0);

const MOCK_COLLECTION = [
  { skin: { name: "Spirit Blossom Ahri", champion: "Ahri",   rarity: "legendary", image_path: "" }, count: 2 },
  { skin: { name: "Arcane Jinx",         champion: "Jinx",   rarity: "epic",      image_path: "" }, count: 1 },
  { skin: { name: "Pulsefire Ezreal",    champion: "Ezreal", rarity: "epic",      image_path: "" }, count: 3 },
  { skin: { name: "Star Guardian Lux",   champion: "Lux",    rarity: "rare",      image_path: "" }, count: 2 },
  { skin: { name: "Bewitching Jinx",     champion: "Jinx",   rarity: "rare",      image_path: "" }, count: 1 },
  { skin: { name: "Base Ahri",           champion: "Ahri",   rarity: "common",    image_path: "" }, count: 4 },
  { skin: { name: "Base Jinx",           champion: "Jinx",   rarity: "common",    image_path: "" }, count: 1 },
];

function normalizeSkins(data) {
  if (!Array.isArray(data)) {
    console.warn("normalizeSkins: Expected array, got:", data);
    return [];
  }
  const map = new Map();
  for (const skin of data) {
    if (!skin) continue;
    const key = skin.id ?? skin.name;
    if (map.has(key)) {
      map.get(key).count += 1;
    } else {
      map.set(key, { skin, count: skin.count ?? 1 });
    }
  }
  return Array.from(map.values());
}

onMounted(async () => {
  const savedSlots  = localStorage.getItem(SLOTS_KEY);
  const savedShards = localStorage.getItem(SHARDS_KEY);
  if (savedSlots)  displaySlots.value = JSON.parse(savedSlots);
  if (savedShards) tokenBalance.value = parseInt(savedShards, 10);

  // Auth check
  try {
    const userRes = await fetch("/api/user", { credentials: "include" });
    const userData = await userRes.json();
    if (!userRes.ok || !userData.username) {
      router.push({ name: "Login" });
      return;
    }
  } catch (err) {
    console.error("Auth check failed:", err);
    router.push({ name: "Login" });
    return;
  }

  // Always seed with mock cards; merge real backend data on top
  // Create a deep copy of mock to avoid mutating the original reference
  let merged = MOCK_COLLECTION.map(item => ({ 
    skin: { ...item.skin }, 
    count: item.count 
  }));

  try {
    const data = await fetchUserCollection();
    console.log("Fetched collection data:", data);
    
    if (data && data.length > 0) {
      const backendEntries = normalizeSkins(data);
      // Add backend skins that aren't already in mock
      for (const entry of backendEntries) {
        const exists = merged.find(m => m.skin.name === entry.skin.name);
        if (exists) {
          exists.count += entry.count;
        } else {
          merged.push(entry);
        }
      }
    }
  } catch (err) {
    console.error("Failed to fetch user collection from database:", err);
    // Fall back to mock only
  }

  collection.value = merged;
  loading.value = false;
});

function getSlotForSkin(skin) {
  const idx = displaySlots.value.findIndex(s => s && s.name === skin.name);
  return idx >= 0 ? idx : null;
}

function openModal(entry) { selected.value = entry; }
function closeModal()     { selected.value = null; }

function disenchant() {
  if (!selected.value) return;
  const entry  = selected.value;
  tokenBalance.value += TOKEN_VALUES[entry.skin.rarity] ?? 15;
  localStorage.setItem(SHARDS_KEY, tokenBalance.value);

  entry.count -= 1;
  if (entry.count <= 0) {
    collection.value = collection.value.filter(e => e !== entry);
    displaySlots.value = displaySlots.value.map(s => s && s.name === entry.skin.name ? null : s);
    saveSlots();
    closeModal();
  }
}

function setDisplaySlot(idx) {
  if (!selected.value) return;
  const skin  = selected.value.skin;
  const slots = [...displaySlots.value];
  for (let i = 0; i < slots.length; i++) {
    if (slots[i] && slots[i].name === skin.name) slots[i] = null;
  }
  slots[idx] = { ...skin };
  displaySlots.value = slots;
  saveSlots();
}

function saveSlots() {
  localStorage.setItem(SLOTS_KEY, JSON.stringify(displaySlots.value));
}
</script>

<style scoped>
.collection-page {
  width: 100%;
  min-height: 100vh;
  padding: 40px 48px;
  margin: 0 auto;
}

/* ── Header ── */
.page-header {
  margin-bottom: 28px;
}

.header-title-row {
  display: flex;
  align-items: baseline;
  gap: 16px;
  margin-bottom: 4px;
}

.page-title {
  margin: 0;
  font-size: 2rem;
  font-weight: 800;
  background: linear-gradient(135deg, #f9fafb, #93c5fd);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.header-sep {
  font-size: 2rem;
  font-weight: 300;
  color: rgba(148, 163, 184, 0.3);
  line-height: 1;
}

.shards-label {
  color: var(--text-muted);
  background: none;
  -webkit-text-fill-color: var(--text-muted);
}

.shards-label .shard-num {
  -webkit-text-fill-color: #fde68a;
  color: #fde68a;
}

.page-subtitle {
  margin: 0;
  font-size: 0.88rem;
  color: var(--text-muted);
}

/* ── Feedback states ── */
.feedback-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  padding: 80px 0;
  color: var(--text-muted);
}

.spinner {
  width: 36px; height: 36px;
  border: 3px solid rgba(148,163,184,0.2);
  border-top-color: #60a5fa;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin { to { transform: rotate(360deg); } }

.empty-icon { font-size: 2.5rem; }
.empty-msg  { margin: 0; font-size: 1rem; }

/* ── Gallery Grid ── */
.skin-gallery {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(308px, 1fr));
  gap: 32px;
}

/* ── Skin Card ── */
.skin-card {
  position: relative;
  width: 308px;
  height: 560px;
  border-radius: 18px;
  overflow: hidden;
  cursor: pointer;
  border: 1px solid rgba(148,163,184,0.15);
  background: rgba(15, 23, 42, 0.6);
  transition: transform 0.25s ease, box-shadow 0.25s ease;
  outline: none;
}

.skin-card:hover,
.skin-card:focus {
  transform: translateY(-6px) scale(1.02);
}

.skin-card.common    { border-color: rgba(156,163,175,0.3); }
.skin-card.common:hover  { box-shadow: 0 12px 32px rgba(0,0,0,0.4); }
.skin-card.rare      { border-color: rgba(59,130,246,0.4); }
.skin-card.rare:hover    { box-shadow: 0 12px 40px rgba(59,130,246,0.25); }
.skin-card.epic      { border-color: rgba(168,85,247,0.45); }
.skin-card.epic:hover    { box-shadow: 0 12px 40px rgba(168,85,247,0.3); }
.skin-card.legendary { border-color: rgba(234,179,8,0.5); }
.skin-card.legendary:hover { box-shadow: 0 12px 50px rgba(234,179,8,0.35); }
.skin-card.ultimate  { border-color: rgba(239, 68, 68, 0.7); }
.skin-card.ultimate:hover  { box-shadow: 0 12px 60px rgba(239, 68, 68, 0.45); }

/* Dupe badge */
.dupe-badge {
  position: absolute;
  top: 10px; right: 10px;
  z-index: 10;
  background: rgba(0,0,0,0.75);
  backdrop-filter: blur(6px);
  color: #f9fafb;
  font-size: 0.72rem;
  font-weight: 700;
  padding: 3px 8px;
  border-radius: 999px;
  border: 1px solid rgba(255,255,255,0.15);
}

/* Slot pip */
.slot-pip {
  position: absolute;
  top: 10px; left: 10px;
  z-index: 10;
  background: rgba(59,130,246,0.85);
  color: #dbeafe;
  font-size: 0.65rem;
  font-weight: 700;
  padding: 3px 8px;
  border-radius: 999px;
  letter-spacing: 0.04em;
}

/* Art */
.card-art {
  position: absolute;
  inset: 0;
}

.card-img {
  width: 100%; height: 100%;
  object-fit: cover;
  transition: transform 0.4s ease;
}

.skin-card:hover .card-img { transform: scale(1.06); }

.art-bg {
  width: 100%; height: 100%;
}
.art-bg.common    { background: linear-gradient(160deg, #1e293b 0%, #0f172a 100%); }
.art-bg.rare      { background: linear-gradient(160deg, #1e3a8a 0%, #0f172a 100%); }
.art-bg.epic      { background: linear-gradient(160deg, #581c87 0%, #1e293b 100%); }
.art-bg.legendary { background: linear-gradient(160deg, #713f12 0%, #1e293b 100%); }

/* Shimmer on hover */
.card-shimmer {
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, transparent 40%, rgba(255,255,255,0.07) 50%, transparent 60%);
  background-size: 200% 200%;
  opacity: 0;
  transition: opacity 0.3s ease;
  pointer-events: none;
}
.skin-card:hover .card-shimmer { opacity: 1; }

/* Info overlay */
.card-info {
  position: absolute;
  bottom: 0; left: 0; right: 0;
  background: linear-gradient(to top, rgba(5,10,25,0.95) 0%, transparent 100%);
  padding: 32px 14px 14px;
  text-align: center;
}

.card-champ {
  margin: 0 0 2px;
  font-size: 0.65rem;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.card-name {
  margin: 0 0 8px;
  font-size: 0.85rem;
  font-weight: 700;
  color: var(--text-main);
  line-height: 1.2;
}

.rarity-pill {
  font-size: 0.6rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  padding: 3px 9px;
  border-radius: 999px;
}
.rarity-pill.common    { background: rgba(156,163,175,0.15); color: #d1d5db; border: 1px solid rgba(156,163,175,0.3); }
.rarity-pill.rare      { background: rgba(59,130,246,0.15);  color: #93c5fd; border: 1px solid rgba(59,130,246,0.4); }
.rarity-pill.epic      { background: rgba(168,85,247,0.15);  color: #d8b4fe; border: 1px solid rgba(168,85,247,0.4); }
.rarity-pill.legendary { background: rgba(234,179,8,0.15);   color: #fde68a; border: 1px solid rgba(234,179,8,0.5); }
.rarity-pill.ultimate  { background: rgba(239, 68, 68, 0.15); color: #ef4444; border: 1px solid rgba(239, 68, 68, 0.5); box-shadow: 0 0 10px rgba(239, 68, 68, 0.3); display: flex; align-items: center; gap: 6px; }

.ultimate-dot {
  width: 5px;
  height: 5px;
  background: #ef4444;
  border-radius: 50%;
  box-shadow: 0 0 6px #ef4444;
}

/* ── Modal ── */
.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.75);
  backdrop-filter: blur(8px);
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
}

.modal-panel {
  position: relative;
  display: flex;
  gap: 0;
  width: 100%;
  max-width: 720px;
  background: rgba(10, 16, 30, 0.96);
  border-radius: 24px;
  overflow: hidden;
  border: 1px solid rgba(148,163,184,0.15);
  box-shadow: 0 40px 80px rgba(0,0,0,0.6);
}

.modal-panel.rare      { border-color: rgba(59,130,246,0.4);  box-shadow: 0 0 60px rgba(59,130,246,0.15), 0 40px 80px rgba(0,0,0,0.6); }
.modal-panel.epic      { border-color: rgba(168,85,247,0.45); box-shadow: 0 0 60px rgba(168,85,247,0.2),  0 40px 80px rgba(0,0,0,0.6); }
.modal-panel.legendary { border-color: rgba(234,179,8,0.5);   box-shadow: 0 0 80px rgba(234,179,8,0.25),  0 40px 80px rgba(0,0,0,0.6); }
.modal-panel.ultimate  { border-color: rgba(239, 68, 68, 0.8); box-shadow: 0 0 100px rgba(239, 68, 68, 0.4), 0 40px 80px rgba(0,0,0,0.6); }

.modal-close {
  position: absolute;
  top: 14px; right: 14px;
  z-index: 10;
  background: rgba(0,0,0,0.5);
  border: 1px solid rgba(255,255,255,0.1);
  color: var(--text-muted);
  width: 32px; height: 32px;
  border-radius: 50%;
  cursor: pointer;
  font-size: 0.85rem;
  transition: background 0.2s, color 0.2s;
  display: flex; align-items: center; justify-content: center;
}
.modal-close:hover { background: rgba(255,255,255,0.1); color: #f9fafb; }

.modal-art-wrap {
  position: relative;
  width: 308px;
  flex-shrink: 0;
  min-height: 560px;
}

.modal-img {
  width: 100%; height: 100%;
  object-fit: cover;
}

.modal-art-bg {
  width: 100%; height: 100%;
}
.modal-art-bg.common    { background: linear-gradient(160deg, #1e293b 0%, #0f172a 100%); }
.modal-art-bg.rare      { background: linear-gradient(160deg, #1e3a8a 0%, #0f172a 100%); }
.modal-art-bg.epic      { background: linear-gradient(160deg, #581c87 0%, #1e293b 100%); }
.modal-art-bg.legendary { background: linear-gradient(160deg, #92400e 0%, #1e293b 100%); }
.modal-art-bg.ultimate  { background: linear-gradient(160deg, #450a0a 0%, #1e293b 100%); }

.modal-rarity-badge {
  position: absolute;
  top: 14px; left: 14px;
  font-size: 0.62rem; font-weight: 700;
  letter-spacing: 0.1em;
  padding: 4px 10px;
  border-radius: 999px;
}
.modal-rarity-badge.common    { background: rgba(156,163,175,0.2); color: #d1d5db; border: 1px solid rgba(156,163,175,0.4); }
.modal-rarity-badge.rare      { background: rgba(59,130,246,0.2);  color: #93c5fd; border: 1px solid rgba(59,130,246,0.5); }
.modal-rarity-badge.epic      { background: rgba(168,85,247,0.2);  color: #d8b4fe; border: 1px solid rgba(168,85,247,0.5); }
.modal-rarity-badge.legendary { background: rgba(234,179,8,0.2);   color: #fde68a; border: 1px solid rgba(234,179,8,0.6); }
.modal-rarity-badge.ultimate  { background: rgba(239, 68, 68, 0.2); color: #ef4444; border: 1px solid rgba(239, 68, 68, 0.7); display: flex; align-items: center; gap: 6px; }

.modal-dupe {
  position: absolute;
  bottom: 14px; right: 14px;
  background: rgba(0,0,0,0.7);
  color: #f9fafb;
  font-size: 0.8rem; font-weight: 700;
  padding: 4px 10px;
  border-radius: 999px;
  border: 1px solid rgba(255,255,255,0.15);
}

.modal-details {
  flex: 1;
  padding: 32px 28px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 8px;
}

.modal-champ {
  margin: 0;
  font-size: 0.78rem;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.modal-name {
  margin: 0;
  font-size: 1.6rem;
  font-weight: 800;
  color: var(--text-main);
  line-height: 1.15;
}

.modal-worth {
  margin: 0;
  font-size: 0.85rem;
  color: var(--text-muted);
}
.modal-worth strong { color: #fde68a; }

.modal-slot-info {
  margin: 0;
  font-size: 0.8rem;
  color: #93c5fd;
}

.modal-actions {
  display: flex;
  flex-direction: column;
  gap: 14px;
  margin-top: 12px;
}

.disenchant-btn {
  padding: 12px 20px;
  border-radius: 10px;
  background: rgba(234,179,8,0.1);
  border: 1px solid rgba(234,179,8,0.4);
  color: #fde68a;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s, border-color 0.2s, transform 0.15s;
  text-align: left;
}
.disenchant-btn:hover {
  background: rgba(234,179,8,0.2);
  border-color: rgba(234,179,8,0.7);
  transform: translateY(-1px);
}

.display-slot-section { display: flex; flex-direction: column; gap: 10px; }

.section-label {
  margin: 0;
  font-size: 0.75rem;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.slot-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 8px;
}

.slot-btn {
  padding: 9px 4px;
  border-radius: 8px;
  background: rgba(15,23,42,0.8);
  border: 1px solid rgba(148,163,184,0.2);
  color: var(--text-muted);
  font-size: 0.8rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}
.slot-btn:hover {
  background: rgba(59,130,246,0.15);
  border-color: rgba(59,130,246,0.5);
  color: #93c5fd;
}
.slot-btn.slot-active {
  background: rgba(59,130,246,0.25);
  border-color: rgba(59,130,246,0.7);
  color: #dbeafe;
}

/* ── Modal transition ── */
.modal-fade-enter-active,
.modal-fade-leave-active { transition: opacity 0.2s ease, transform 0.2s ease; }
.modal-fade-enter-from,
.modal-fade-leave-to { opacity: 0; }
.modal-fade-enter-from .modal-panel,
.modal-fade-leave-to .modal-panel { transform: scale(0.95); }

/* ── Responsive ── */
@media (max-width: 600px) {
  .collection-page { padding: 24px 16px; }
  .modal-panel { flex-direction: column; }
  .modal-art-wrap { width: 100%; min-height: 220px; }
  .slot-grid { grid-template-columns: repeat(2, 1fr); }
}
</style>
