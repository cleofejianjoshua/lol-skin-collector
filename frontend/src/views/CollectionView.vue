<template>
  <div class="collection-page">

    <!-- Header -->
    <div class="page-header" v-if="!loading">
      <div class="header-title-row">
        <h1 class="page-title">Collection</h1>
        <span class="header-sep">|</span>
        <span class="page-title essence-label">Essence: <span class="essence-num">{{ tokenBalance }}</span></span>
      </div>
      <p class="page-subtitle">
        {{ ownedCount }} permanent - {{ shardCount }} shard{{ shardCount !== 1 ? 's' : '' }}
      </p>

      <!-- Filter -->
      <div class="filter-row-container" v-if="!loading && collection.length > 0">
        <div class="filter-row">
          <button class="filter-btn" :class="{ active: activeFilter === 'all' }" @click="activeFilter = 'all'">
            All Rarity <span class="filter-count">{{ getFilterCount('all') }}</span>
          </button>
          <button class="filter-btn" :class="{ active: activeFilter === 'ultimate' }" @click="activeFilter = 'ultimate'">
            Ultimate <span class="filter-count">{{ getFilterCount('ultimate') }}</span>
          </button>
          <button class="filter-btn" :class="{ active: activeFilter === 'legendary' }" @click="activeFilter = 'legendary'">
            Legendary <span class="filter-count">{{ getFilterCount('legendary') }}</span>
          </button>
          <button class="filter-btn" :class="{ active: activeFilter === 'epic' }" @click="activeFilter = 'epic'">
            Epic <span class="filter-count">{{ getFilterCount('epic') }}</span>
          </button>
          <button class="filter-btn" :class="{ active: activeFilter === 'rare' }" @click="activeFilter = 'rare'">
            Rare <span class="filter-count">{{ getFilterCount('rare') }}</span>
          </button>
          <button class="filter-btn" :class="{ active: activeFilter === 'common' }" @click="activeFilter = 'common'">
            Common <span class="filter-count">{{ getFilterCount('common') }}</span>
          </button>
        </div>
        <div class="filter-row secondary">
          <button class="filter-btn" :class="{ active: statusFilter === 'all' }" @click="statusFilter = 'all'">
            All Status <span class="filter-count">{{ getFilterCount(undefined, 'all') }}</span>
          </button>
          <button class="filter-btn" :class="{ active: statusFilter === 'permanent' }" @click="statusFilter = 'permanent'">
            Permanent <span class="filter-count">{{ getFilterCount(undefined, 'permanent') }}</span>
          </button>
          <button class="filter-btn" :class="{ active: statusFilter === 'shards' }" @click="statusFilter = 'shards'">
            Shards <span class="filter-count">{{ getFilterCount(undefined, 'shards') }}</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Skeleton Grid -->
    <div v-if="loading" class="skin-gallery">
      <div v-for="i in 10" :key="i" class="card-wrapper skeleton-card">
        <div class="skeleton-img"></div>
        <div class="skeleton-line short"></div>
        <div class="skeleton-line"></div>
      </div>
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

    <!-- Empty Filter Result -->
    <div v-else-if="filteredCollection.length === 0" class="feedback-state">
      <p class="empty-msg">No skins match the selected filter.</p>
    </div>

    <!-- Gallery -->
    <div v-else class="skin-gallery">
      <div
        v-for="entry in filteredCollection"
        :key="entry.skin.name"
        class="card-wrapper"
        @click="openModal(entry)"
        tabindex="0"
        role="button"
        @keydown.enter="openModal(entry)"
      >
        <SkinCard :skin="entry.skin" :isShard="!entry.is_owned" />
        <span v-if="entry.count > 1" class="dupe-badge">×{{ entry.count }}</span>
        <span v-if="entry.is_owned && getSlotForSkin(entry.skin) !== null" class="slot-pip">
          Slot {{ getSlotForSkin(entry.skin) + 1 }}
        </span>
      </div>
    </div>

    <!-- Modal -->
    <Teleport to="body">
      <Transition name="modal-fade">
        <div v-if="selected" class="modal-backdrop" @click.self="closeModal">
          <div class="modal-container">
            
            <!-- Left: Card Art (Using universal SkinCard) -->
            <div class="modal-card-side" :class="{ 'is-shard-preview': !selected.is_owned }">
              <SkinCard :skin="selected.skin" :isShard="!selected.is_owned" />
              <!-- Optional: Add dupe count if needed, or keep it clean -->
              <span v-if="selected.count > 1" class="modal-dupe-badge">×{{ selected.count }}</span>
            </div>

            <!-- Right: Details/Actions Card -->
            <div class="modal-actions-card rarity-themed" :class="selected.skin.rarity.name">
              
              <div class="modal-details-content">
                
                <div class="modal-info-block">
                  <p v-if="getSlotForSkin(selected.skin) !== null" class="modal-slot-info">
                    Assigned to <strong>Slot {{ getSlotForSkin(selected.skin) + 1 }}</strong>
                  </p>
                </div>

                <div class="modal-actions">
                  <!-- Enchant Button -->
                  <div v-if="!selected.is_owned" class="enchant-section">
                    <p class="cost-text blue">ENCHANTMENT COST = {{ (typeof selected.skin.rarity === 'object' ? selected.skin.rarity.unlock_cost : null) ?? 0 }}</p>
                    <button class="enchant-btn" @click="enchant">
                      Enchant
                    </button>
                  </div>

                  <!-- Disenchant Button -->
                  <div v-if="!selected.is_owned || selected.count > 1" class="disenchant-section">
                    <p class="cost-text amber">DISENCHANT REWARD = {{ (typeof selected.skin.rarity === 'object' ? selected.skin.rarity.disenchant_value : null) ?? 0 }}</p>
                    <button class="disenchant-btn" @click="disenchant">
                      Disenchant
                    </button>
                  </div>

                  <div v-if="selected.is_owned" class="display-slot-section">
                    <p class="section-label">Home Page Display</p>
                    <div class="slot-grid">
                      <button
                        v-for="i in 4"
                        :key="i"
                        class="slot-btn"
                        :class="{ 'slot-active': getSlotForSkin(selected.skin) === i - 1 }"
                        @click="setDisplaySlot(i-1)"
                      >
                        Slot {{ i }}
                      </button>
                    </div>
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
import { ref, onMounted, computed } from "vue";
import { useRouter } from "vue-router";
import { fetchUserCollection, fetchDisplaySlots, updateDisplaySlot, clearDisplaySlot, unlockSkin, fetchSkins } from "@/services/api.js";
import SkinCard from "@/components/shared/SkinCard.vue";

const router = useRouter();

const loading      = ref(true);
const collection   = ref([]);
const selected     = ref(null);
const displaySlots = ref([null, null, null, null]); // [skin | null, ...]
const tokenBalance = ref(0);
const activeFilter = ref("all");
const statusFilter = ref("all"); // all, permanent, shards
const allSkins     = ref([]);

const rarityTotals = computed(() => {
  const totals = {
    all: allSkins.value.length,
    ultimate: 0,
    legendary: 0,
    epic: 0,
    rare: 0,
    common: 0
  };
  allSkins.value.forEach(s => {
    const rName = typeof s.rarity === 'object' ? s.rarity.name : s.rarity;
    if (totals[rName] !== undefined) totals[rName]++;
  });
  return totals;
});

function getFilterCount(rarity, status) {
  // Use current selection if the other part is omitted
  const r = rarity ?? activeFilter.value;
  const s = status ?? statusFilter.value;

  const userCount = collection.value.filter(e => {
    let rMatch = true;
    if (r !== 'all') {
      const rName = typeof e.skin.rarity === 'object' ? e.skin.rarity.name : e.skin.rarity;
      rMatch = (rName === r);
    }
    
    let sMatch = true;
    if (s === 'permanent') {
      sMatch = e.is_owned;
    } else if (s === 'shards') {
      sMatch = !e.is_owned;
    }
    
    return rMatch && sMatch;
  }).length;

  const total = rarityTotals.value[r] || 0;
  return `${userCount}/${total}`;
}

const ownedCount = computed(() => collection.value.filter(e => e.is_owned).length);
const shardCount = computed(() => collection.value.filter(e => !e.is_owned).length);

const filteredCollection = computed(() => {
  return collection.value.filter(e => {
    // Rarity Filter
    let rarityMatch = true;
    if (activeFilter.value !== "all") {
      const rarityName = typeof e.skin.rarity === 'object' ? e.skin.rarity.name : e.skin.rarity;
      rarityMatch = (rarityName === activeFilter.value);
    }

    // Status Filter
    let statusMatch = true;
    if (statusFilter.value === "permanent") {
      statusMatch = e.is_owned;
    } else if (statusFilter.value === "shards") {
      statusMatch = !e.is_owned;
    }

    return rarityMatch && statusMatch;
  });
});

function normalizeSkins(data) {
  if (!Array.isArray(data)) return [];
  const map = new Map();
  for (const entry of data) {
    if (!entry) continue;
    const skin = entry.skin ?? entry;
    const key  = skin.id ?? skin.name;
    
    if (map.has(key)) {
      const existing = map.get(key);
      existing.count += 1;
      if (entry.is_owned) existing.is_owned = true;
    } else {
      map.set(key, { 
        id: entry.id, 
        skin, 
        count: 1, 
        is_owned: !!entry.is_owned 
      });
    }
  }
  return Array.from(map.values());
}

onMounted(async () => {
  try {
    const [userRes, collectionData, slots, allSkinsData] = await Promise.all([
      fetch("/api/user", { credentials: "include" }).then(r => r.json()),
      fetchUserCollection().catch(() => []),
      fetchDisplaySlots().catch(() => []),
      fetchSkins().catch(() => []),
    ]);

    if (!userRes.username) { router.push({ name: "Login" }); return; }

    tokenBalance.value = userRes.essence ?? 0;
    collection.value   = normalizeSkins(collectionData ?? []);
    allSkins.value     = allSkinsData ?? [];

    const slotArray = [null, null, null, null];
    for (const s of slots) {
      slotArray[s.slot_index] = s.skin ?? null;
    }
    displaySlots.value = slotArray;
  } catch {
    router.push({ name: "Login" });
  } finally {
    loading.value = false;
  }
});

function getSlotForSkin(skin) {
  const idx = displaySlots.value.findIndex(s => s && s.id === skin.id);
  return idx >= 0 ? idx : null;
}

function openModal(entry) { selected.value = entry; }
function closeModal()     { selected.value = null;  }

async function disenchant() {
  if (!selected.value) return;
  const entry = selected.value;
  
  if (entry.is_owned && entry.count <= 1) {
    alert("Cannot disenchant a permanent skin unless you have a duplicate.");
    return;
  }

  try {
    const res = await fetch(`/api/collection/disenchant/${entry.id}`, {
      method: "DELETE",
      credentials: "include",
    });
    if (!res.ok) { 
      const errorData = await res.json();
      alert(errorData.error || "Disenchant failed");
      return; 
    }
    const data = await res.json();
    tokenBalance.value = data.essence;
    entry.count -= 1;
    if (entry.count <= 0) {
      // Clear slot if this skin was displayed
      const slotIdx = getSlotForSkin(entry.skin);
      if (slotIdx !== null) {
        await clearDisplaySlot(slotIdx);
        displaySlots.value[slotIdx] = null;
      }
      collection.value = collection.value.filter(e => e !== entry);
      closeModal();
    }
  } catch (err) {
    console.error("Network error during disenchant:", err);
  }
}

async function enchant() {
  if (!selected.value) return;
  const entry = selected.value;
  
  try {
    const data = await unlockSkin(entry.id);
    tokenBalance.value = data.essence;
    entry.is_owned = true;
  } catch (err) {
    alert(err.message || "Failed to unlock skin");
    console.error("Enchant error:", err);
  }
}

async function setDisplaySlot(idx) {
  if (!selected.value) return;
  const skin = selected.value.skin;

  // Clear this skin from any existing slot first
  const currentSlot = getSlotForSkin(skin);
  if (currentSlot !== null && currentSlot !== idx) {
    await clearDisplaySlot(currentSlot);
    displaySlots.value[currentSlot] = null;
  }

  // If already in this slot, clear it (toggle off)
  if (currentSlot === idx) {
    await clearDisplaySlot(idx);
    displaySlots.value[idx] = null;
    return;
  }

  await updateDisplaySlot(idx, skin.id);
  displaySlots.value[idx] = { ...skin };
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
  margin-bottom: 32px;
}

.header-title-row {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 4px;
}

.page-title {
  margin: 0;
  font-size: 2.2rem;
  font-weight: 800;
  color: #fff;
  letter-spacing: -0.02em;
}

.header-sep {
  color: rgba(255,255,255,0.15);
  font-size: 1.5rem;
  font-weight: 300;
}

.essence-label {
  font-size: 2.2rem;
  font-weight: 800;
  display: flex;
  align-items: center;
  gap: 8px;
  background: linear-gradient(135deg, #a855f7, #6366f1, #3b82f6);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: -0.02em;
}

.essence-num {
  font-weight: 900;
}

.page-subtitle {
  margin: 0 0 24px;
  font-size: 1rem;
  color: var(--text-muted);
}

/* ── Filters ── */
.filter-row-container {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.filter-row {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.filter-row.secondary {
  opacity: 0.9;
}

.filter-btn {
  background: rgba(15, 23, 42, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.1);
  padding: 8px 18px;
  border-radius: 999px;
  color: var(--text-muted);
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.filter-btn:hover {
  color: #93c5fd;
}

.filter-btn.active {
  background: rgba(59,130,246,0.25);
  border-color: rgba(59,130,246,0.7);
  color: #dbeafe;
}

.filter-count {
  margin-left: 6px;
  opacity: 0.5;
  font-size: 0.7rem;
  font-weight: 500;
  font-family: var(--font-mono, monospace);
}

.filter-btn.active .filter-count {
  opacity: 0.9;
  color: #fff;
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

/* ── Card Wrapper (overlays for collection-specific badges) ── */
.card-wrapper {
  position: relative;
  width: 308px;
  height: 560px;
  cursor: pointer;
  border-radius: 0;
  transition: transform 0.25s ease, border-color 0.25s ease;
  outline: none;
}

.card-wrapper:hover,
.card-wrapper:focus {
  transform: translateY(-10px);
  z-index: 5;
}

/* Dupe badge */
.dupe-badge {
  position: absolute;
  top: 12px; right: 12px;
  z-index: 2;
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
  top: 12px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 2;
  background: rgba(59,130,246,0.85);
  color: #dbeafe;
  font-size: 0.65rem;
  font-weight: 700;
  padding: 4px 12px;
  border-radius: 999px;
  letter-spacing: 0.06em;
  backdrop-filter: blur(4px);
  border: 1px solid rgba(96,165,250,0.5);
  box-shadow: 0 0 12px rgba(59,130,246,0.35);
  white-space: nowrap;
}

/* ── Modal ── */
.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.85);
  backdrop-filter: blur(12px);
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px;
}

.modal-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  width: 100%;
  max-width: 308px;
  transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.modal-card-side {
  width: 308px;
  height: 560px;
  flex-shrink: 0;
  box-shadow: 0 30px 60px rgba(0,0,0,0.8);
  position: relative;
}

.modal-dupe-badge {
  position: absolute;
  top: 14px; right: 14px;
  z-index: 10;
  background: rgba(0,0,0,0.8);
  color: #fff;
  padding: 4px 10px;
  font-size: 0.8rem;
  font-weight: 700;
  border: 1px solid rgba(255,255,255,0.2);
}

.modal-actions-card {
  width: 100%;
  background: linear-gradient(165deg, rgba(15, 23, 42, 0.95) 0%, rgba(2, 6, 23, 0.98) 100%);
  border: 1px solid rgba(148, 163, 184, 0.12);
  border-radius: 0;
  padding: 20px 24px;
  position: relative;
  display: flex;
  flex-direction: column;
  box-shadow: 0 40px 100px rgba(0,0,0,0.7);
  backdrop-filter: blur(20px);
}

/* Rarity-themed borders for actions card - slightly more pronounced */
.modal-actions-card.rare      { border-bottom: 3px solid rgba(59, 130, 246, 0.6); }
.modal-actions-card.epic      { border-bottom: 3px solid rgba(168, 85, 247, 0.6); }
.modal-actions-card.legendary { border-bottom: 3px solid rgba(234, 179, 8, 0.7); }
.modal-actions-card.ultimate  { border-bottom: 3px solid rgba(239, 68, 68, 0.9); }


.modal-info-block {
  margin-bottom: 16px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.modal-worth {
  margin: 0;
  font-size: 0.88rem;
  color: #94a3b8;
  letter-spacing: 0.01em;
}
.modal-worth strong { 
  color: #fbbf24;
  font-weight: 700;
  text-shadow: 0 0 10px rgba(251, 191, 36, 0.3);
}

.modal-slot-info {
  margin: 0;
  font-size: 0.82rem;
  color: #60a5fa;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 6px;
}
.modal-slot-info::before {
  content: "•";
  font-size: 1.2rem;
}

/* Enchantment Section */
.enchant-section {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 8px;
}

.enchant-btn {
  width: 100%;
  padding: 14px;
  background: rgba(59, 130, 246, 0.08);
  border: 1px solid rgba(59, 130, 246, 0.3);
  border-radius: 0;
  color: #60a5fa;
  font-weight: 800;
  font-size: 0.95rem;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  text-align: center;
}

.enchant-btn:hover {
  background: rgba(59, 130, 246, 0.15);
  border-color: rgba(59, 130, 246, 0.6);
  color: #fff;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.enchant-btn:active {
  transform: translateY(1px);
}


.enchant-hint {
  font-size: 0.75rem;
  color: rgba(148, 163, 184, 0.6);
  text-align: center;
  margin: 0;
  font-style: italic;
}

.modal-actions {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.disenchant-btn {
  width: 100%;
  padding: 14px;
  background: rgba(245, 158, 11, 0.08);
  border: 1px solid rgba(245, 158, 11, 0.25);
  border-radius: 0;
  color: #fbbf24;
  font-size: 0.9rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  text-align: center;
  position: relative;
  overflow: hidden;
}
.disenchant-btn:hover {
  background: rgba(245, 158, 11, 0.15);
  border-color: rgba(245, 158, 11, 0.6);
  color: #fff;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

/* Enchantment & Disenchantment Sections */
.enchant-section, .disenchant-section {
  display: flex;
  flex-direction: column;
  gap: 4px;
  margin-bottom: 12px;
}

.cost-text {
  margin: 0 0 4px;
  font-size: 0.8rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}
.cost-text.blue { color: #60a5fa; }
.cost-text.amber { color: #fbbf24; }

.value-row {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 4px;
}

.essence-icon {
  font-size: 1.2rem;
  filter: drop-shadow(0 0 5px rgba(168, 85, 247, 0.4));
}

.value-num {
  font-size: 1.6rem;
  font-weight: 900;
  color: #fff;
  letter-spacing: 0.02em;
}

.enchant-section .value-num { color: #60a5fa; }
.disenchant-section .value-num { color: #fbbf24; }

.display-slot-section {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.section-label {
  margin: 0;
  font-size: 0.72rem;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.15em;
  font-weight: 800;
  opacity: 0.8;
}

.slot-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 8px;
}

.slot-btn {
  padding: 12px 4px;
  background: rgba(15, 23, 42, 0.5);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 0;
  color: #64748b;
  font-size: 0.78rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.25s ease;
  position: relative;
}
.slot-btn:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.15);
  color: #cbd5e1;
  transform: translateY(-2px);
}
.slot-btn.slot-active {
  background: rgba(59, 130, 246, 0.1);
  border-color: rgba(59, 130, 246, 0.5);
  color: #fff;
  box-shadow: inset 0 0 15px rgba(59, 130, 246, 0.15);
}
.slot-btn.slot-active::after {
  content: "";
  position: absolute;
  bottom: 0; left: 0; right: 0;
  height: 2px;
  background: #3b82f6;
}

/* ── Modal transition ── */
.modal-fade-enter-active,
.modal-fade-leave-active { transition: opacity 0.4s ease; }
.modal-fade-enter-from,
.modal-fade-leave-to { opacity: 0; }

.modal-fade-enter-from .modal-container,
.modal-fade-leave-to .modal-container { 
  transform: scale(0.8) translateY(30px);
  opacity: 0;
}

/* ── Responsive ── */
@media (max-width: 768px) {
  .collection-page { padding: 24px 16px; }
  .modal-container { 
    flex-direction: column; 
    align-items: center;
    gap: 20px;
    padding-bottom: 40px;
  }
  .modal-actions-card { width: 100%; padding: 30px 20px; }
  .slot-grid { grid-template-columns: repeat(2, 1fr); }
}

/* ── Skeleton ── */
.skeleton-card {
  cursor: default;
  pointer-events: none;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.skeleton-img {
  width: 308px;
  height: 480px;
  background: linear-gradient(90deg,
    rgba(255,255,255,0.04) 25%,
    rgba(255,255,255,0.08) 50%,
    rgba(255,255,255,0.04) 75%
  );
  background-size: 200% 100%;
  animation: shimmer 1.4s infinite;
}

.skeleton-line {
  height: 14px;
  border-radius: 4px;
  background: linear-gradient(90deg,
    rgba(255,255,255,0.04) 25%,
    rgba(255,255,255,0.08) 50%,
    rgba(255,255,255,0.04) 75%
  );
  background-size: 200% 100%;
  animation: shimmer 1.4s infinite;
  width: 100%;
}

.skeleton-line.short { width: 60%; }

@keyframes shimmer {
  0%   { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
</style>
