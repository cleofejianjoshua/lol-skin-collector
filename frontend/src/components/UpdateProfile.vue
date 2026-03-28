<template>
  <div class="login-page">
    <div class="login-card profile-card-large">
      
      <!-- HEADER (NO LOGO) -->
      <div class="brand">
        <div class="brand-text">
          <h1>Update Profile</h1>
          <p>Change your information</p>
        </div>
      </div>

      <!-- FORM -->
      <form class="profile-form" @submit.prevent="onSubmit">
        
        <label class="field">
          <span>Nickname</span>
          <input
            v-model="nickname"
            type="text"
            placeholder="Enter your nickname"
            required
          />
        </label>

        <label class="field">
          <span>Email</span>
          <input
            v-model="email"
            type="email"
            placeholder="Enter your email"
            required
          />
        </label>

        <p v-if="success" class="success-text">
          Profile updated successfully!
        </p>

        <button class="primary-btn" type="submit">
          Save Changes
        </button>
      </form>

    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";

const nickname = ref("");
const email = ref("");
const success = ref(false);

const onSubmit = () => {
  console.log("Saved:", nickname.value, email.value);

  success.value = true;

  setTimeout(() => {
    success.value = false;
  }, 2000);
};
</script>

<style scoped>
/* PAGE LAYOUT */
.profile-page {
  display: flex;
  justify-content: flex-start; 
  align-items: flex-start;
  min-height: 100vh;
  padding-top: 60px;
  padding-left: 80px;

  /* responsive center on small screens */
}
@media (max-width: 768px) {
  .profile-page {
    justify-content: center;
    padding-left: 24px;
    padding-right: 24px;
    padding-top: 40px;
  }
}

/* CARD */
.profile-card.profile-card-large {
  width: 100%;
  max-width: 600px; /* bigger than before */
  padding: 40px 36px; /* more spacious */
  border-radius: 24px;
  background: #1e1e2f;
  box-shadow: 0 16px 40px rgba(0, 0, 0, 0.35);
}

/* HEADER */
.brand {
  margin-bottom: 28px;
}

.brand-text h1 {
  margin: 0;
  font-size: 2rem;
}

.brand-text p {
  margin: 0;
  font-size: 1rem;
  color: #aaa;
}

/* FORM */
.profile-form {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

/* FIELD */
.field {
  width: 100%;
  margin-bottom: 22px;
}

.field span {
  display: block;
  margin-bottom: 8px;
  font-size: 1rem;
}

/* BIG INPUTS */
.field input {
  width: 100%;
  padding: 16px 18px;
  font-size: 1.1rem;
  border-radius: 12px;
  border: none;
  outline: none;
  background: #2a2a40;
  color: white;
}

/* BUTTON */
.primary-btn {
  margin-top: 14px;
  width: 100%;
  padding: 16px;
  border-radius: 16px;
  border: none;
  background: #6366f1;
  color: white;
  font-size: 1.05rem;
  cursor: pointer;
  transition: background 0.2s;
}

.primary-btn:hover {
  background: #4f46e5;
}

/* SUCCESS MESSAGE */
.success-text {
  margin-bottom: 12px;
  padding: 12px;
  border-radius: 12px;
  background: rgba(34, 197, 94, 0.15);
  color: #bbf7d0;
  width: 100%;
  font-size: 1rem;
}
</style>