<template>
  <div class="auth-page">
    <div class="cards">
      <BrandHeader
        title="LOL Skin Collector"
        subtitle="Create your account."
      />

      <form class="login-form" @submit.prevent="onSubmit">
        <label class="field">
          <span>Username</span>
          <input
            v-model="username"
            type="text"
            placeholder="Your username"
            required
          />
        </label>

        <label class="field">
          <span>Password</span>
          <input
            v-model="password"
            type="password"
            placeholder="Password"
            minlength="6"
            required
          />
        </label>

        <label class="field">
          <span>Repeat Password</span>
          <input
            v-model="password2"
            type="password"
            placeholder="Repeat password"
            minlength="6"
            required
          />
        </label>

        <p v-if="passwordError" class="error-text">{{ passwordError }}</p>
        <p v-if="error" class="error-text">{{ error }}</p>

        <button class="primary-btn" type="submit" :disabled="loading">
          {{ loading ? "Creating account..." : "Sign up" }}
        </button>
      </form>

      <p class="helper-text">
        Already have an account?
        <router-link to="/login" class="link-button">Sign in</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import BrandHeader from "@/components/shared/BrandHeader.vue";

const router = useRouter();
const username = ref("");
const password = ref("");
const password2 = ref("");
const passwordError = ref("");
const error = ref("");
const loading = ref(false);

const onSubmit = async () => {
  passwordError.value = "";
  error.value = "";
  loading.value = true;

  if (password.value !== password2.value) {
    passwordError.value = "Passwords must match.";
    loading.value = false;
    return;
  }

  try {
    const res = await fetch("/auth/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        username: username.value,
        password: password.value,
        password2: password2.value,
      }),
      credentials: "include",
    });

    const data = await res.json();

    if (!res.ok) {
      error.value = data.error || "Registration failed.";
    } else {
      router.push({ name: "Login" });
    }
  } catch (e) {
    error.value = "Registration failed. Please try again.";
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
