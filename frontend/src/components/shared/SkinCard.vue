<template>
  <div
    class="skin-card rarity-themed"
    :class="[rarity, { 'is-empty': isEmpty, 'is-shard': isShard, 'read-only': readOnly }]"
    @mouseenter="!isEmpty && pipSound.play()"
  >
    <!-- filled skin Card -->
    <template v-if="!isEmpty && skin">
      <!-- background Art -->
      <div class="skin-art">
        <img v-if="skin.image_path" :src="skin.image_path" :alt="skin.name" class="skin-img" />
        <div v-else class="skin-placeholder" :class="rarity"></div>
      </div>

      <!-- gradient overlay -->
      <div class="skin-overlay">
        <!-- top row rarity (left) + Slot (right) -->
        <div class="top-row">
          <div class="rarity-tag" :class="rarity">
            <span v-if="rarity === 'ultimate'" class="ultimate-dot"></span>
            {{ rarity }}
          </div>
          <div v-if="slotNumber" class="slot-badge">Slot {{ slotNumber }}</div>
          <div v-if="isShard" class="shard-badge">Shard</div>
        </div>

        <!-- bottom skin info -->
        <div class="skin-text-info">
          <p class="champ-name">{{ skin.champion }}</p>
          <h4 class="skin-name">{{ skin.name }}</h4>
          <slot name="footer"></slot>
        </div>
      </div>
    </template>

    <!-- empty state -->
    <div v-else class="empty-state">
      <p v-if="slotNumber">Slot {{ slotNumber }}</p>
      <p v-else>Empty</p>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useSound } from "@/services/sound.js";

const { pipSound, pullSound, revealSound, clickSound } = useSound();

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
  },
  readOnly: {
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

/* hover */
.skin-card:hover {
  border-color: var(--accent);
}

/* background art */
.skin-art {
  position: absolute;
  inset: 0;
  z-index: 0;
}

.skin-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: filter 0.4s ease;
  filter: brightness(1);
}

/* shard state */
.skin-card.is-shard .skin-img {
  filter: grayscale(1) brightness(0.6);
}

.skin-card.is-shard:hover .skin-img {
  filter: grayscale(0.5) brightness(0.8);
}



/* overlay */
.skin-overlay {
  position: absolute;
  inset: 0;
  z-index: 1;
  padding: 16px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  background: linear-gradient(to bottom, rgba(0,0,0,0.3) 0%, transparent 40%, rgba(0,0,0,0.85) 100%);
}

/* top row: rarity tag left, slot badge right */
.top-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
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

/* bottom text info */
.skin-text-info { text-align: left; }

.champ-name {
  margin: 0;
  font-size: 0.72rem;
  color: rgba(255,255,255,0.6);
  text-transform: uppercase;
  letter-spacing: 0.12em;
}

.skin-name {
  margin: 4px 0 0;
  font-size: 1.1rem;
  font-weight: 800;
  color: #fff;
  line-height: 1.2;
}

/* empty state */
.empty-state {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(15, 23, 42, 0.3);
  color: rgba(148, 163, 184, 0.4);
  font-size: 0.85rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;
}

.skin-card.read-only {
  cursor: default;
}
</style>
