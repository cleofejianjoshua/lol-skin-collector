<template>
  <div 
    class="skin-slideshow-card rarity-themed" 
    :class="[{ 'is-loading': !currentSkin }, getRarityName(currentSkin)]"
  >
    <transition name="fade-slide" mode="out-in">
      <div v-if="currentSkin" :key="currentSkin.name" class="slideshow-content">
        <!-- background Image -->
        <div class="skin-bg">
          <img 
            v-if="currentSkin.image_path" 
            :src="currentSkin.image_path" 
            :alt="currentSkin.name" 
            class="bg-img"
          />
          <div v-else class="skin-placeholder" :class="currentSkin.rarity"></div>
        </div>

        <!-- overlay Info -->
        <div class="skin-overlay">
          <div class="rarity-tag" :class="getRarityName(currentSkin)">
            {{ getRarityName(currentSkin) }}
          </div>
          <div class="text-info">
            <p class="champ-name">{{ currentSkin.champion }}</p>
            <h4 class="skin-name">{{ currentSkin.name }}</h4>
          </div>
        </div>
      </div>
      <div v-else class="loading-state">
        <div class="spinner"></div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue';

const props = defineProps({
  skins: {
    type: Array,
    default: () => []
  },
  interval: {
    type: Number,
    default: 5000
  }
});

const currentIndex = ref(0);
const currentSkin = ref(null);
const timer = ref(null);

const getRarityName = (skin) => {
  if (!skin || !skin.rarity) return 'common';
  return typeof skin.rarity === 'object' ? skin.rarity.name : skin.rarity;
};

const startSlideshow = () => {
  if (timer.value) clearInterval(timer.value);
  if (props.skins.length > 0) {
    currentIndex.value = Math.floor(Math.random() * props.skins.length);
    currentSkin.value = props.skins[currentIndex.value];
    timer.value = setInterval(nextSkin, props.interval);
  }
};

const nextSkin = () => {
  if (props.skins.length === 0) return;
  
  // transition to the next skin
  currentIndex.value = (currentIndex.value + 1) % props.skins.length;
  currentSkin.value = props.skins[currentIndex.value];

  // preload the one AFTER the next one
  const nextIdx = (currentIndex.value + 1) % props.skins.length;
  const nextToPreload = props.skins[nextIdx];
  if (nextToPreload && nextToPreload.image_path) {
    const img = new Image();
    img.src = nextToPreload.image_path;
  }
};

watch(() => props.skins, (newSkins) => {
  if (newSkins && newSkins.length > 0 && !currentSkin.value) {
    startSlideshow();
    // preload the first few
    newSkins.slice(0, 3).forEach(s => {
      if (s.image_path) {
        const img = new Image();
        img.src = s.image_path;
      }
    });
  }
}, { deep: true });

onMounted(startSlideshow);
onUnmounted(() => {
  if (timer.value) clearInterval(timer.value);
});
</script>

<style scoped>
.skin-slideshow-card {
  width: 308px;
  height: 560px;
  border-radius: 0;
  background: rgba(15, 23, 42, 0.6);
  border: 2px solid rgba(255, 255, 255, 0.08);
  overflow: hidden;
  position: relative;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(12px);
  transition: border-color 2s ease;
}

.slideshow-content {
  width: 100%;
  height: 100%;
  position: relative;
}

.skin-bg {
  position: absolute;
  inset: 0;
  z-index: 0;
}

.bg-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  filter: brightness(1.1) contrast(1.05);
  transition: opacity 0.5s ease;
}

.bg-placeholder {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #1e293b, #0f172a);
}

/* overlay */
.skin-overlay {
  position: absolute;
  inset: 0;
  padding: 20px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  z-index: 1;
  background: linear-gradient(to bottom, rgba(0,0,0,0.3) 0%, transparent 40%, rgba(0,0,0,0.8) 100%);
}

.text-info {
  text-align: left;
}

.champ-name {
  margin: 0;
  font-size: 0.75rem;
  color: rgba(255,255,255,0.6);
  text-transform: uppercase;
  letter-spacing: 0.1em;
}

.skin-name {
  margin: 4px 0 0;
  font-size: 1.1rem;
  font-weight: 800;
  color: white;
  line-height: 1.2;
}

/* transitions */
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: opacity 2s ease, transform 2s ease;
}

.fade-slide-enter-from {
  opacity: 0;
}

.fade-slide-leave-to {
  opacity: 0;
}

.loading-state {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
}

.spinner {
  width: 30px;
  height: 30px;
  border: 2px solid rgba(255,255,255,0.1);
  border-top-color: #3b82f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
