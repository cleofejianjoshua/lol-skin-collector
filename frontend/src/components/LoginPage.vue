<template>
  <div class="login-page">
    <div class="cards">
      <div class="brand">
        <div class="logo-circle">
          <span class="logo-text">LC</span>
        </div>
        <div class="brand-text">
          <h1>LOL Skin Collector</h1>
          <p>Sign in to manage your collection.</p>
        </div>
      </div>

      <form class="login-form" method="POST" 
      @submit.prevent="onSubmit">
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

  try {
    const formData = new FormData();
    formData.append("username", username.value);
    formData.append("password", password.value);

    const res = await fetch("/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        username: username.value,
        password: password.value
      }),
      credentials: "include",
    });

    const data = await res.json();

    if (res.ok) {
      router.push({ name: "LoginSuccess" });
    } else {
      error.value = data.error || "Invalid username or password.";
    }

  } catch (e) {
    error.value = "Login failed.";
  } finally {
    loading.value = false;
  }
};
</script>