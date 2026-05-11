<template>
  <div 
    class="skin-slideshow-card rarity-themed" 
    :class="[{ 'is-loading': !currentSkin }, currentSkin?.rarity]"
  >
    <transition name="fade-slide" mode="out-in">
      <div v-if="currentSkin" :key="currentSkin.name" class="slideshow-content">
        <!-- Background Image -->
        <div class="skin-bg">
          <img 
            v-if="currentSkin.image_path" 
            :src="currentSkin.image_path" 
            :alt="currentSkin.name" 
            class="bg-img"
          />
          <div v-else class="bg-placeholder" :class="currentSkin.rarity"></div>
        </div>

        <!-- Overlay Info -->
        <div class="skin-overlay">
          <div class="rarity-tag" :class="currentSkin.rarity">
            {{ currentSkin.rarity }}
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
  currentIndex.value = (currentIndex.value + 1) % props.skins.length;
  currentSkin.value = props.skins[currentIndex.value];
};

watch(() => props.skins, (newSkins) => {
  if (newSkins && newSkins.length > 0 && !currentSkin.value) {
    startSlideshow();
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
  border: 1px solid rgba(255, 255, 255, 0.08);
  overflow: hidden;
  position: relative;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(12px);
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
  filter: brightness(0.7) contrast(1.1);
}

.bg-placeholder {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #1e293b, #0f172a);
}

.bg-placeholder.legendary { background: linear-gradient(135deg, #422006, #0f172a); }
.bg-placeholder.epic      { background: linear-gradient(135deg, #3b0764, #0f172a); }
.bg-placeholder.rare      { background: linear-gradient(135deg, #1e3a8a, #0f172a); }

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

.rarity-tag {
  align-self: flex-start;
  padding: 4px 10px;
  border-radius: 999px;
  font-size: 0.65rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  border: 1px solid rgba(255,255,255,0.2);
  background: rgba(0,0,0,0.4);
}

.rarity-tag.common    { color: #d1d5db; background: rgba(30,30,35,0.85);  border-color: rgba(156,163,175,0.4); }
.rarity-tag.rare      { color: #93c5fd; background: rgba(15,30,60,0.85);  border-color: rgba(59,130,246,0.4); }
.rarity-tag.epic      { color: #d8b4fe; background: rgba(40,10,65,0.85);  border-color: rgba(168,85,247,0.4); }
.rarity-tag.legendary { color: #fde68a; background: rgba(55,35,5,0.9);    border-color: rgba(234,179,8,0.4); }
.rarity-tag.ultimate  { color: #ef4444; background: rgba(60,8,8,0.9);     border-color: rgba(239,68,68,0.5); box-shadow: 0 0 8px rgba(239,68,68,0.3); }

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

/* Transitions */
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: opacity 0.6s ease;
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
