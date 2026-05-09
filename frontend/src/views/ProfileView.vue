<template>
  <div class="profile-page">
    <div class="profile-layout-wrapper">
      <!-- Left Slideshow -->
      <aside class="profile-side-panel left">
        <SkinSlideshow :skins="MOCK_POOL" :interval="4500" />
      </aside>

      <!-- Center Content -->
      <div class="profile-main-container">
        <div class="profile-card">
          <h2>Profile</h2>
          <p class="subtitle">Your account information</p>

          <div v-if="loading" class="info-field">
            <p>Loading profile...</p>
          </div>

          <template v-else>
            <div class="info-field">
              <span>Username</span>
              <p>{{ username }}</p>
            </div>

            <div v-if="nickname" class="info-field">
              <span>Nickname</span>
              <p>{{ nickname }}</p>
            </div>

            <div class="info-field">
              <span>Email</span>
              <p>{{ email }}</p>
            </div>

            <button class="primary-btn" @click="goUpdateProfile">
              Update Profile
            </button>

            <p v-if="errorMsg" class="error-text">{{ errorMsg }}</p>
          </template>
        </div>
      </div>

      <!-- Right Slideshow -->
      <aside class="profile-side-panel right">
        <SkinSlideshow :skins="MOCK_POOL" :interval="6500" />
      </aside>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter, onBeforeRouteUpdate } from "vue-router";
import { fetchUser } from "@/services/api.js";
import SkinSlideshow from "@/components/shared/SkinSlideshow.vue";

const router = useRouter();

const loading = ref(true);
const errorMsg = ref("");

const username = ref("");
const nickname = ref("");
const email = ref("");

const MOCK_POOL = [
  { name: "Spirit Blossom Ahri",  champion: "Ahri",   rarity: "legendary", image_path: "" },
  { name: "Arcane Jinx",          champion: "Jinx",   rarity: "epic",      image_path: "" },
  { name: "Pulsefire Ezreal",     champion: "Ezreal", rarity: "epic",      image_path: "" },
  { name: "Star Guardian Lux",    champion: "Lux",    rarity: "rare",      image_path: "" },
  { name: "Bewitching Jinx",      champion: "Jinx",   rarity: "rare",      image_path: "" },
];

const loadProfile = async () => {
  loading.value = true;
  errorMsg.value = "";

  try {
    const data = await fetchUser();

    if (!data.username) {
      throw new Error(data.error || "Failed to load profile.");
    }

    username.value = data.username || "Unknown user";
    nickname.value = data.nickname || "";
    email.value = data.email || "No email set";
  } catch (err) {
    errorMsg.value = err.message;
  } finally {
    loading.value = false;
  }
};

const goUpdateProfile = () => {
  router.push({ name: "UpdateProfile" });
};

onMounted(loadProfile);
onBeforeRouteUpdate(loadProfile);
</script>

<style scoped>
.profile-page {
  min-height: 80vh;
  position: relative;
  overflow-x: hidden;
  padding: 60px 0;
}

.profile-layout-wrapper {
  display: flex;
  align-items: flex-start;
  justify-content: center;
  width: 100%;
  max-width: 100vw;
  margin: 0;
  padding: 0;
}

.profile-side-panel {
  position: fixed;
  top: 50%;
  transform: translateY(-50%);
  z-index: 5;
  display: block;
  width: 320px;
}

.profile-side-panel.left {
  left: 180px;
}

.profile-side-panel.right {
  right: 180px;
}

.profile-main-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 40px;
}

.subtitle {
  font-size: 0.9rem;
  color: var(--text-muted);
  margin-bottom: 24px;
}

.profile-card {
  text-align: left;
}

.info-field {
  margin-bottom: 22px;
}

.info-field span {
  font-size: 0.85rem;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  display: block;
}

.info-field p {
  font-size: 1.1rem;
  color: var(--text-main);
  margin: 6px 0 0;
  font-weight: 500;
}

.primary-btn {
  margin-top: 10px;
  min-width: 200px;
}

@media (max-width: 1280px) {
  .profile-side-panel { display: none; }
}
</style>
