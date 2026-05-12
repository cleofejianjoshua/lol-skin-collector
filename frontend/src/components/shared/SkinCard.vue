<template>
  <div
    class="skin-card rarity-themed"
    :class="[rarity, { 'is-empty': isEmpty, 'is-shard': isShard }]"
  >
    <!-- Filled Skin Card -->
    <template v-if="!isEmpty && skin">
      <!-- Background Art -->
      <div class="skin-art">
        <img v-if="skin.image_path" :src="skin.image_path" :alt="skin.name" class="skin-img" />
        <div v-else class="skin-placeholder" :class="rarity"></div>
      </div>

      <!-- Gradient Overlay -->
      <div class="skin-overlay">
        <!-- Top Row: Rarity (left) + Slot# (right) -->
        <div class="top-row">
          <div class="rarity-tag" :class="rarity">
            <span v-if="rarity === 'ultimate'" class="ultimate-dot"></span>
            {{ rarity }}
          </div>
          <div v-if="slotNumber" class="slot-badge">Slot {{ slotNumber }}</div>
          <div v-if="isShard" class="shard-badge">Shard</div>
        </div>

        <!-- Bottom: Skin Info -->
        <div class="skin-text-info">
          <p class="champ-name">{{ skin.champion }}</p>
          <h4 class="skin-name">{{ skin.name }}</h4>
          <slot name="footer"></slot>
        </div>
      </div>
    </template>

    <!-- Empty State -->
    <div v-else class="empty-state">
      <p v-if="slotNumber">Slot {{ slotNumber }}</p>
      <p v-else>Empty</p>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  skin: {
    type: Object,
    default: () => null
  },
  isEmpty: {
    type: Boolean,
    default: false
  },
  slotNumber: {
    type: [Number, String],
    default: null
  },
  isShard: {
    type: Boolean,
    default: false
  }
});

const rarity = computed(() => {
  const r = props.skin?.rarity || 'common';
  return typeof r === 'object' ? r.name : r;
});
</script>

<style scoped>
.skin-card {
  width: 308px;
  height: 560px;
  border-radius: 0;
  background: rgba(15, 23, 42, 0.6);
  border: 2px solid rgba(148, 163, 184, 0.15);
  overflow: hidden;
  position: relative;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(12px);
  transition: box-shadow 0.4s ease, border-color 0.3s ease;
}

/* Hover */
.skin-card:hover {
  border-color: var(--accent);
}

/* Background art */
.skin-art {
  position: absolute;
  inset: 0;
  z-index: 0;
}

.skin-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  filter: brightness(0.8);
  transition: transform 0.5s ease, filter 0.4s ease;
}

.skin-card:hover .skin-img {
  filter: brightness(1);
}

/* Shard State */
.skin-card.is-shard .skin-img {
  filter: grayscale(1) brightness(0.6);
}

.skin-card.is-shard:hover .skin-img {
  filter: grayscale(0.5) brightness(0.8);
}

.shard-badge {
  font-size: 0.62rem;
  font-weight: 800;
  color: #fff;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  background: rgba(148, 163, 184, 0.4);
  padding: 4px 10px;
  border-radius: 999px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(4px);
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
}

.skin-placeholder {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #1e293b, #0f172a);
}

.skin-placeholder.rare      { background: linear-gradient(135deg, #1e3a8a, #0f172a); }
.skin-placeholder.epic      { background: linear-gradient(135deg, #3b0764, #0f172a); }
.skin-placeholder.legendary { background: linear-gradient(135deg, #422006, #0f172a); }
.skin-placeholder.ultimate  { background: linear-gradient(135deg, #450a0a, #0f172a); }

/* Overlay */
.skin-overlay {
  position: absolute;
  inset: 0;
  z-index: 1;
  padding: 20px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  background: linear-gradient(to bottom, rgba(0,0,0,0.3) 0%, transparent 40%, rgba(0,0,0,0.85) 100%);
}

/* Top row: rarity tag left, slot badge right */
.top-row {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.rarity-tag {
  padding: 4px 10px;
  border-radius: 999px;
  font-size: 0.65rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  background: rgba(0,0,0,0.4);
  border: 1px solid rgba(255,255,255,0.2);
  display: flex;
  align-items: center;
  gap: 6px;
  backdrop-filter: blur(4px);
}

.rarity-tag.common    { color: #d1d5db; background: rgba(30,30,35,0.75);    border-color: rgba(156,163,175,0.4); }
.rarity-tag.rare      { color: #93c5fd; background: rgba(15,30,60,0.8);     border-color: rgba(59,130,246,0.4); }
.rarity-tag.epic      { color: #d8b4fe; background: rgba(40,10,65,0.8);     border-color: rgba(168,85,247,0.4); }
.rarity-tag.legendary { color: #fde68a; background: rgba(55,35,5,0.85);     border-color: rgba(234,179,8,0.4); }
.rarity-tag.ultimate  { color: #ef4444; background: rgba(60,8,8,0.85);      border-color: rgba(239,68,68,0.5); box-shadow: 0 0 8px rgba(239,68,68,0.3); }

.ultimate-dot {
  width: 6px;
  height: 6px;
  background: #ef4444;
  border-radius: 50%;
  box-shadow: 0 0 6px #ef4444;
}

.slot-badge {
  font-size: 0.62rem;
  font-weight: 700;
  color: rgba(148,163,184,0.7);
  text-transform: uppercase;
  letter-spacing: 0.1em;
  background: rgba(0,0,0,0.4);
  padding: 4px 10px;
  border-radius: 999px;
  border: 1px solid rgba(255,255,255,0.1);
  backdrop-filter: blur(4px);
}

/* Bottom text info */
.skin-text-info { text-align: left; }

.champ-name {
  margin: 0;
  font-size: 0.7rem;
  color: rgba(255,255,255,0.6);
  text-transform: uppercase;
  letter-spacing: 0.1em;
}

.skin-name {
  margin: 4px 0 0;
  font-size: 1.1rem;
  font-weight: 800;
  color: #fff;
  line-height: 1.2;
}

/* Empty State */
.empty-state {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 16px;
  color: rgba(148, 163, 184, 0.3);
  transition: color 0.3s ease;
}

.empty-state p {
  margin: 0;
  font-size: 0.9rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
</style>
