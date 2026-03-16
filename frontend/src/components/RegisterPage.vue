<template>
  <div class="login-page">
    <div class="login-card">
      <div class="brand">
        <div class="logo-circle">
          <span class="logo-text">LC</span>
        </div>
        <div class="brand-text">
          <h1>LOL Skin Collector</h1>
          <p>Sign up</p>
        </div>
      </div>

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

        <p v-if="passwordError" class="error-text">
          {{ passwordError }}
        </p>

        <button class="primary-btn" type="submit">
          Sign up
        </button>
      </form>

      <p class="helper-text">
        Already have an account?
        <router-link to="/login" class="link-button">
          Sign in
        </router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";

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
    const res = await fetch("http://127.0.0.1:5000/api/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        username: username.value,
        password: password.value,
      }),
    });

    if (!res.ok) {
      const msg = await res.text();
      throw new Error(msg || "Register failed.");
    }

    const data = await res.json();
    console.log("Register success", data);
    // TODO: navigate to /login or auto‑login, clear form, etc.
  } catch (e) {
    error.value = e.message || "Unable to register. Please try again.";
  } finally {
    loading.value = false;
  }
};
</script>