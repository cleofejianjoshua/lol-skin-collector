<template>
  <div class="login-page">
    <div class="login-card">
      <div class="brand">
        <div class="logo-circle">
          <span class="logo-text">LC</span>
        </div>
        <div class="brand-text">
          <h1>LOL Skin Collector</h1>
          <p>Sign in to manage your collection.</p>
        </div>
      </div>

      <form class="login-form" @submit.prevent="onSubmit">
        <label class="field">
          <span>Email</span>
          <input
            v-model="email"
            type="email"
            placeholder="you@example.com"
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

        <div class="field field-inline">
          <label class="checkbox">
            <input v-model="rememberMe" type="checkbox" />
            <span>Remember me</span>
          </label>
          <button type="button" class="link-button">Forgot password?</button>
        </div>

        <button class="primary-btn" type="submit">
          Log in
        </button>

        <p v-if="error" class="error-text">{{ error }}</p>
      </form>

      <p class="helper-text">
        Don’t have an account?
        <button type="button" class="link-button">Create one</button>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";

const email = ref("");
const password = ref("");
const rememberMe = ref(false);
const error = ref("");

const onSubmit = () => {
  error.value = "";

  // Simple client-side example; hook this into your real API.
  if (!email.value || !password.value) {
    error.value = "Please enter both email and password.";
    return;
  }

  console.log("Login attempt", {
    email: email.value,
    password: password.value,
    rememberMe: rememberMe.value
  });
};
</script>
