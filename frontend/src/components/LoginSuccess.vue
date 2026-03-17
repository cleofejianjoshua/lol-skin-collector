<template>
  <div class="login-page">
    <div class="login-card">
      <div class="brand">
        <div class="logo-circle">
          <span class="logo-text">LC</span>
        </div>
        <div class="brand-text">
          <h1>Success</h1>
          <p>You’re signed in</p>
        </div>
      </div>

      <p class="success-text">Login successfully.</p>

      <button class="primary-btn" type="button" @click="goDashboard">
        Go to Dashboard
      </button>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from "vue-router";

const router = useRouter();

const goDashboard = () => {
  router.push({ name: "Dashboard" });
};
</script>

<style scoped>
.success-text {
  margin: 10px 0 14px;
  padding: 10px 12px;
  border-radius: 12px;
  background: rgba(34, 197, 94, 0.12);
  border: 1px solid rgba(34, 197, 94, 0.28);
  color: #bbf7d0;
  font-size: 0.9rem;
  text-align: center;
}
</style>