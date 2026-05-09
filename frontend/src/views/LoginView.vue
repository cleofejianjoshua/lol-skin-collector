<template>
  <div class="auth-page">
    <div class="cards">
      <BrandHeader
        title="LOL Skin Collector"
        subtitle="Sign in to manage your collection."
      />

      <form class="login-form" @submit.prevent="onSubmit">
        <label class="field">
          <span>Username</span>
          <input
            v-model="username"
            type="text"
            placeholder="your_username"
            required
          />
        </label>

        <label class="field">
          <span>Password</span>
          <input
            v-model="password"
            type="password"
            placeholder="••••••••"
            minlength="6"
            required
          />
        </label>

        <button class="primary-btn" type="submit" :disabled="loading">
          {{ loading ? "Signing in..." : "Log in" }}
        </button>

        <p v-if="error" class="error-text">{{ error }}</p>
      </form>

      <p class="helper-text">
        Don't have an account?
        <router-link to="/register" class="link-button">Sign up</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import BrandHeader from "@/components/shared/BrandHeader.vue";

const username = ref("");
const password = ref("");

const error = ref("");
const loading = ref(false);
const router = useRouter();

const onSubmit = async () => {
  error.value = "";
  loading.value = true;

  try {
    const res = await fetch("/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        username: username.value,
        password: password.value,
      }),
      credentials: "include",
    });

    const data = await res.json();

    if (res.ok) {
      router.push({ path: "/" });
    } else {
      error.value = data.error || "Invalid username or password.";
    }
  } catch (e) {
    error.value = "Login failed. Please try again.";
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
</style>
