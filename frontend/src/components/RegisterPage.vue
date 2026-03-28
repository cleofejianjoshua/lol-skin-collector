<template>
  <div class="login-page">
    <div class="cards">
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
    const formData = new FormData();
    formData.append("username", username.value);
    formData.append("password", password.value);
    formData.append("password2", password2.value);

    const res = await fetch("http://127.0.0.1:5000/api/register", {
      method: "POST",
      body: formData,
      credentials: "include" // Include cookies for session management
    });

const data = await res.json();

if (!res.ok) {
  error.value = data.error || "Registration failed.";
} else {
  alert("Account created!");
  window.location.href = "/login"; // Vue route
}

  } catch (e) {
    error.value = "Registration failed.";
  } finally {
    loading.value = false;
  }
};
</script>