<template>
  <div class="auth-page">
    <div class="cards cards--wide">
      <div class="brand-text">
        <h1>Update Profile</h1>
        <p>Change your account information</p>
      </div>

      <form class="profile-form" @submit.prevent="onSubmit">
        <label class="field">
          <span>Nickname</span>
          <input
            v-model="nickname"
            name="nickname"
            type="text"
            placeholder="Enter your nickname"
          />
        </label>

        <label class="field">
          <span>Email</span>
          <input
            v-model="email"
            name="email"
            type="email"
            placeholder="Enter your email"
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
import { fetchUser } from "@/services/api.js";

const router = useRouter();
const nickname = ref("");
const email = ref("");
const loading = ref(false);
const successMsg = ref("");
const errorMsg = ref("");

// Pre-fill with existing data
onMounted(async () => {
  try {
    const data = await fetchUser();
    nickname.value = data.nickname || data.username || "";
    email.value = data.email || "";
  } catch (err) {
    console.error("Failed to load user data:", err);
  }
});

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
      credentials: "include",
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
.auth-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
}

.cards--wide {
  text-align: left;
}

.brand-text {
  margin-bottom: 32px;
}

.brand-text h1 {
  margin: 0 0 6px;
  font-size: 2rem;
  font-weight: 800;
  color: var(--text-main);
}

.brand-text p {
  margin: 0;
  color: var(--text-muted);
  font-size: 0.95rem;
}

.profile-form {
  gap: 24px;
}
</style>
