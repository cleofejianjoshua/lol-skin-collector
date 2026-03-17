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
          <router-link to="/register" class="link-button">
            Sign up
          </router-link>
        </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";


const username = ref("");
const password = ref("");
const rememberMe = ref(false);
const error = ref("");
const loading = ref(false);
const router = useRouter();

const onSubmit = async () => {
  error.value = "";
  loading.value = true;

  if (!username.value || !password.value) {
    error.value = "Please enter both username and password.";
    loading.value = false;
    return;
  }

  try {
    const res = await fetch("http://127.0.0.1:5000/api/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        username: username.value,
        password: password.value,
        rememberMe: rememberMe.value,
      }),
    });

    if (!res.ok) {
      const msg = await res.text();
      throw new Error(msg || "Login failed.");
    }

    const data = await res.json();
    console.log("Login success", data);
    await router.push({ name: "LoginSuccess" });
    // TODO: save token / mark user as logged in / navigate
  } catch (e) {
    error.value = e.message || "Unable to login. Please try again.";
  } finally {
    loading.value = false;
  }
};
</script>