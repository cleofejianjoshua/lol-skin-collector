<template>
  <div class="login-page">
    <div class="login-card login-success-card">
      <div class="brand">
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

<!-->
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
<!-->

<style scoped>
/* Bigger login-success card */
.login-success-card {
  width: 500px !important;          /* wider than default */
  max-width: none !important;       /* override global max-width */
  padding: 40px 36px !important;    /* more padding */
  border-radius: 24px !important;   /* bigger rounding */
}

/* Make the success text a bit bigger */
.success-text {
  margin: 16px 0 20px;
  padding: 14px 16px;
  border-radius: 14px;
  background: rgba(34, 197, 94, 0.12);
  border: 1px solid rgba(34, 197, 94, 0.28);
  color: #bbf7d0;
  font-size: 1rem;
  text-align: center;
}

/* Optional: bigger button */
.primary-btn {
  padding: 16px 20px;
  font-size: 1rem;
  border-radius: 16px;
}
</style>