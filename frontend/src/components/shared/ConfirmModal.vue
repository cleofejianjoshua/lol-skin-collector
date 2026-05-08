<!-- Reusable confirmation modal.
     Props:
       show    (Boolean) — controls visibility
       title   (String)  — modal heading
       message (String)  — body text
     Emits:
       confirm — user clicked Yes
       cancel  — user clicked No / backdrop
-->
<template>
  <Teleport to="body">
    <Transition name="modal-fade">
      <div v-if="show" class="modal-backdrop" @click.self="$emit('cancel')">
        <div class="modal-card">
          <!-- Icon -->
          <div class="modal-icon">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"
              stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="10"/>
              <line x1="12" y1="8" x2="12" y2="12"/>
              <line x1="12" y1="16" x2="12.01" y2="16"/>
            </svg>
          </div>

          <h2 class="modal-title">{{ title }}</h2>
          <p class="modal-message">{{ message }}</p>

          <div class="modal-actions">
            <button class="modal-btn modal-btn--cancel" @click="$emit('cancel')">
              No, stay
            </button>
            <button class="modal-btn modal-btn--confirm" @click="$emit('confirm')">
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
/* Backdrop */
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

/* Card */
.modal-card {
  position: relative;
  width: 100%;
  max-width: 380px;
  padding: 36px 32px 28px;
  border-radius: 22px;
  background: linear-gradient(145deg, rgba(255,255,255,0.04), rgba(6,9,20,0.96));
  border: 1px solid rgba(255,255,255,0.08);
  box-shadow: 0 32px 80px rgba(0,0,0,0.85);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  text-align: center;
}

/* Glowing top border */
.modal-card::before {
  content: "";
  position: absolute;
  inset: -1px;
  border-radius: inherit;
  border: 1px solid transparent;
  background: linear-gradient(135deg, rgba(249,115,115,0.7), transparent 55%) border-box;
  mask: linear-gradient(#000 0 0) padding-box, linear-gradient(#000 0 0);
  mask-composite: exclude;
  pointer-events: none;
}

/* Icon */
.modal-icon {
  width: 52px;
  height: 52px;
  border-radius: 50%;
  background: rgba(249, 115, 115, 0.12);
  border: 1px solid rgba(249, 115, 115, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--danger);
  margin-bottom: 4px;
}

.modal-icon svg {
  width: 24px;
  height: 24px;
}

.modal-title {
  margin: 0;
  font-size: 1.2rem;
  font-weight: 700;
  color: var(--text-main);
}

.modal-message {
  margin: 0;
  font-size: 0.88rem;
  color: var(--text-muted);
  line-height: 1.5;
}

/* Buttons */
.modal-actions {
  display: flex;
  gap: 12px;
  width: 100%;
  margin-top: 8px;
}

.modal-btn {
  flex: 1;
  padding: 11px 16px;
  border-radius: var(--radius-pill);
  border: none;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.15s ease, filter 0.15s ease;
}

.modal-btn:hover {
  transform: translateY(-2px);
  filter: brightness(1.1);
}

.modal-btn:active {
  transform: translateY(0);
}

.modal-btn--cancel {
  background: rgba(255, 255, 255, 0.07);
  color: var(--text-main);
  border: 1px solid var(--border-subtle);
}

.modal-btn--confirm {
  background: linear-gradient(135deg, #f97373, #dc2626);
  color: #fff;
  box-shadow: 0 8px 24px rgba(220, 38, 38, 0.4);
}

/* Transition */
.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.2s ease;
}

.modal-fade-enter-active .modal-card,
.modal-fade-leave-active .modal-card {
  transition: transform 0.2s ease, opacity 0.2s ease;
}

.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}

.modal-fade-enter-from .modal-card,
.modal-fade-leave-to .modal-card {
  transform: scale(0.92) translateY(12px);
  opacity: 0;
}
</style>
