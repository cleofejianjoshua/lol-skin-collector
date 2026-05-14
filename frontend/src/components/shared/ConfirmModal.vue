<template>
  <Teleport to="body">
    <Transition name="modal-fade">
      <div v-if="show" class="modal-backdrop" @click.self="$emit('cancel')">
        <div class="cards">
          <h2 class="modal-title">{{ title }}</h2>
          <p class="modal-message">{{ message }}</p>

          <div class="modal-actions">
            <button class="secondary-btn" @click="$emit('cancel')">
              No, stay
            </button>
            <button class="danger-btn" @click="$emit('confirm')">
              Yes, sign out
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
defineProps({
  show:    { type: Boolean, default: false },
  title:   { type: String,  default: "Are you sure?" },
  message: { type: String,  default: "" },
});

defineEmits(["confirm", "cancel"]);
</script>

<style scoped>
/* backdrop */
.modal-backdrop {
  position: fixed;
  inset: 0;
  z-index: 100;
  background: rgba(2, 6, 23, 0.75);
  backdrop-filter: blur(6px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
}

.modal-title {
  margin: 0 0 4px;
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--text-main);
  text-align: center;
}

.modal-message {
  margin: 0 0 16px;
  font-size: 0.92rem;
  color: var(--text-muted);
  line-height: 1.5;
  text-align: center;
}

/* buttons */
.modal-actions {
  display: flex;
  gap: 12px;
  width: 100%;
}

/* transition */
.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.2s ease;
}

.modal-fade-enter-active .cards,
.modal-fade-leave-active .cards {
  transition: transform 0.2s ease, opacity 0.2s ease;
}

.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}

.modal-fade-enter-from .cards,
.modal-fade-leave-to .cards {
  transform: scale(0.92) translateY(12px);
  opacity: 0;
}
</style>
