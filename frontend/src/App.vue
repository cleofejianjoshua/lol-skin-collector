<script setup>
import { ref, onMounted, computed, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import { fetchUser, logoutUser } from "@/services/api.js";
import ConfirmModal from "@/components/shared/ConfirmModal.vue";
import { useSound } from "@/services/sound.js";

const { pipSound, pullSound, revealSound, clickSound } = useSound();

const username = ref("Guest");
const nickname = ref("");
const route = useRoute();
const router = useRouter();
const loadingUser = ref(true);
const showLogoutModal = ref(false);

const isLoggedIn = computed(() => username.value && username.value !== "Guest");

const loadUser = async () => {
  const data = await fetchUser();
  username.value = data.username || "Guest";
  nickname.value = data.nickname || "";
  loadingUser.value = false;
};

const displayName = computed(() => nickname.value || username.value);

// opens the confirmation modal instead of logging out immediately
const promptLogout = () => {
  showLogoutModal.value = true;
};

// nav sound effect
const navSound = typeof Audio !== 'undefined' ? new Audio('/sounds/sound_click.mp3') : null;
if (navSound) navSound.volume = 0.5;

const handleNavClick = (e) => {
  // only play sound if an anchor tag was clicked
  const link = e.target.closest('a');
  if (link && navSound) {
    navSound.currentTime = 0;
    navSound.play().catch(err => console.log("Audio play failed:", err));
  }
};

const handleNavHover = (e) => {
  const link = e.target.closest('a');
  if (link) pipSound.play();
};

// called when user clicks yes
const confirmLogout = async () => {
  showLogoutModal.value = false;
  try {
    await logoutUser();
  } catch (err) {
    console.error("Logout failed:", err);
  } finally {
    username.value = "Guest";
    router.push({ name: "Login" });
  }
};

// called when user clicks no
const cancelLogout = () => {
  showLogoutModal.value = false;
};

onMounted(loadUser);

// re-check user on every route change
watch(() => route.fullPath, loadUser);
</script>

<template>
  <div class="app-root">

    <!-- navbar -->
    <header v-if="!loadingUser" class="top-bar">
      <span class="brand">LOL Skin Collector</span>

      <!-- logged-in nav -->
      <nav v-if="isLoggedIn" class="nav-links" @click="handleNavClick" @mouseover="handleNavHover">
        <span class="welcome-text">Welcome, {{ displayName }}!</span>  
        <router-link to="/">Home</router-link>
        <router-link to="/collection">Collection</router-link>
        <router-link to="/gacha">Gacha</router-link>
        <router-link to="/gold-forge">Gold</router-link>
        <router-link to="/profile">Profile</router-link>
        <a href="#" @click.prevent="promptLogout">Logout</a>
      </nav>

      <!-- guest nav -->
      <nav v-else class="nav-links" @click="handleNavClick" @mouseover="handleNavHover">
        <router-link to="/login">Log In</router-link>
        <router-link to="/register">Register</router-link>
      </nav>
    </header>

    <!-- page content -->
    <main class="page-content">
      <router-view v-if="!loadingUser" />
    </main>

    <!-- sign out confirmation modal -->
    <ConfirmModal
      :show="showLogoutModal"
      title="Sign out?"
      message="Are you sure you want to sign out of your account?"
      @confirm="confirmLogout"
      @cancel="cancelLogout"
    />

  </div>
</template>
