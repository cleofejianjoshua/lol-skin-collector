<template>
  <div class="shards-page">

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
</template>

<script setup>
import { ref, onMounted } from "vue";

const STORAGE_KEY = "lol_shards";
const shards    = ref(0);
const isClicked = ref(false);

onMounted(() => {
  const saved = localStorage.getItem(STORAGE_KEY); // gets shard value from local storage, just a mini database
  if (saved !== null) shards.value = parseInt(saved, 10);
});

const clickShard = () => {
  shards.value++;
  localStorage.setItem(STORAGE_KEY, shards.value);
};
</script>

<style scoped>
.shards-page {
  min-height: 80vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 32px;
  padding: 48px 24px;
  text-align: center;
}

.shards-title {
  margin: 0 0 6px;
  font-size: 2.2rem;
  font-weight: 800;
  background: linear-gradient(135deg, #dbeafe, #818cf8, #a78bfa);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.shards-subtitle {
  margin: 0;
  font-size: 0.9rem;
  color: var(--text-muted);
}

/* Counter */
.shard-counter {
  display: flex;
  align-items: center;
  gap: 10px;
  background: rgba(15, 23, 42, 0.7);
  border: 1px solid rgba(129, 140, 248, 0.25);
  border-radius: 999px;
  padding: 12px 28px;
}

.shard-icon  { font-size: 1.4rem; }

.shard-count {
  font-size: 2rem;
  font-weight: 800;
  color: #a5b4fc;
  min-width: 60px;
  text-align: center;
}

.shard-label {
  font-size: 0.85rem;
  color: var(--text-muted);
  letter-spacing: 0.06em;
}

/* Crystal button */
.crystal-btn {
  position: relative;
  width: 160px;
  height: 160px;
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
  inset: -12px;
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
  width: 130px;
  height: 130px;
  border-radius: 50%;
  background: radial-gradient(circle at 32% 28%, #c4b5fd, #7c3aed 50%, #4c1d95);
  box-shadow: 0 0 40px rgba(139,92,246,0.5), 0 16px 40px rgba(0,0,0,0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: box-shadow 0.15s ease;
}

.crystal-btn:hover .crystal-body {
  box-shadow: 0 0 70px rgba(167,139,250,0.8), 0 16px 40px rgba(0,0,0,0.6);
}

.crystal-btn.clicked .crystal-body {
  box-shadow: 0 0 30px rgba(139,92,246,0.4), 0 8px 20px rgba(0,0,0,0.6);
}

.crystal-emoji {
  font-size: 3.5rem;
  filter: drop-shadow(0 0 12px rgba(167,139,250,0.8));
  pointer-events: none;
}

.click-hint {
  margin: 0;
  font-size: 0.8rem;
  color: rgba(156,163,175,0.5);
  letter-spacing: 0.06em;
}
</style>
