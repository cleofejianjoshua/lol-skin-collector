<template>
  <div class="login-page">
    <div class="cards profile-card-large">
      <div class="brand">
        <div class="brand-text">
          <h1>Update Profile</h1>
          <p>Change your information</p>
        </div>
      </div>

      <form class="profile-form" @submit.prevent="onSubmit">
        <label class="field">
          <span>Nickname</span>
          <input
            v-model="nickname"
            name="nickname"
            type="text"
            placeholder="Enter your nickname"
            required
          />
        </label>

        <label class="field">
          <span>Email</span>
          <input
            v-model="email"
            name="email"
            type="email"
            placeholder="Enter your email"
            required
          />
        </label>

        <p v-if="successMsg" class="success-text">{{ successMsg }}</p>
        <p v-if="errorMsg" class="error-text">{{ errorMsg }}</p>

        <button class="primary-btn" type="submit" :disabled="loading">
          {{ loading ? "Saving..." : "Save Changes" }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();
const nickname = ref("");
const email = ref("");
const loading = ref(false);
const successMsg = ref("");
const errorMsg = ref("");

// Load existing data first
onMounted(async () => {
  try {
    const res = await fetch("(api/user", {
      credentials: "include",
    });

    const data = await res.json();
    nickname.value = data.nickname || data.username;
    email.value = data.email || "";
  } catch (err) {
    console.error(err);
  }
});

//  Send update request
const onSubmit = async () => {
  loading.value = true;
  successMsg.value = "";
  errorMsg.value = "";

  try {
    const formData = new FormData();
    formData.append("nickname", nickname.value);
    formData.append("email", email.value);

    const res = await fetch("/api/update-profile", {
      method: "POST",
      body: formData,
      credentials: "include", // send cookies
    });

    const data = await res.json();
    if (!res.ok) {
      throw new Error(data.error || "Failed to update profile");
    }

    successMsg.value = "Profile updated successfully!";
    setTimeout(() => router.push({ name: "Profile" }), 1500);
  } catch (err) {
    errorMsg.value = err.message;
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
  background: linear-gradient(to bottom, rgba(15, 23, 42, 0.9), rgba(15, 23, 42, 0.96)),
    url("/lolwallpaper.png") center top / cover no-repeat fixed;
}

.cards.profile-card-large {
  width: 100%;
  max-width: 600px;
  padding: 40px 36px;
  border-radius: 24px;
  background: var(--card-bg);
  box-shadow: var(--shadow-elevated);
  backdrop-filter: blur(18px);
  border: 1px solid var(--border-subtle);
}

.brand-text h1 {
  margin: 0;
  font-size: 1.8rem;
  color: var(--text-main);
}
.brand-text p {
  margin: 0;
  color: var(--text-muted);
  font-size: 0.9rem;
}

.profile-form {
  display: flex;
  flex-direction: column;
  margin-top: 20px;
}

.field {
  margin-bottom: 18px;
}

.field span {
  display: block;
  margin-bottom: 6px;
  color: var(--text-muted);
}

.field input {
  width: 100%;
  padding: 14px 16px;
  font-size: 1rem;
  border-radius: 12px;
  border: 1px solid var(--border-subtle);
  background: rgba(6, 9, 20, 0.85);
  color: var(--text-main);
}

.field input:focus {
  border-color: var(--accent);
}

.primary-btn {
  margin-top: 10px;
  width: 100%;
  padding: 14px;
  border-radius: var(--radius-pill);
  border: none;
  font-weight: 600;
  background: radial-gradient(circle at 20% 0, #dbeafe, #60a5fa 40%, #1d4ed8);
  color: #0b1120;
  cursor: pointer;
  transition: filter var(--transition-med);
}

.primary-btn:hover {
  filter: brightness(1.05);
}

.success-text {
  background: rgba(34, 197, 94, 0.15);
  color: #bbf7d0;
  padding: 10px;
  border-radius: 12px;
  font-size: 0.9rem;
}
.error-text {
  background: rgba(239, 68, 68, 0.15);
  color: var(--danger);
  padding: 10px;
  border-radius: 12px;
  font-size: 0.9rem;
}
</style>
