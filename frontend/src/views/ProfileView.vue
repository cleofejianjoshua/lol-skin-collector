<template>
  <div class="profile-page-main">

    <!-- Profile Info Card -->
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

        <div class="info-field">
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

    <!-- Favorite Skin Card -->
    <div class="skin-card">
      <h2>Favorite Skin</h2>
      <img
        v-if="skinImage"
        :src="skinImage"
        :alt="favoriteSkin"
        class="skin-image"
      />
      <div v-else class="skin-placeholder">
        <span>No skin selected yet</span>
      </div>
      <p class="skin-name">{{ favoriteSkin }}</p>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter, onBeforeRouteUpdate } from "vue-router";
import { fetchUser } from "@/services/api.js";

const router = useRouter();

const loading = ref(true);
const errorMsg = ref("");

const username = ref("");
const nickname = ref("");
const email = ref("");
const favoriteSkin = ref("No favorite skin yet");
const skinImage = ref("");

const loadProfile = async () => {
  loading.value = true;
  errorMsg.value = "";

  try {
    const data = await fetchUser();

    if (!data.username) {
      throw new Error(data.error || "Failed to load profile.");
    }

    username.value = data.username || "Unknown user";
    nickname.value = data.nickname || data.username || "No nickname set";
    email.value = data.email || "No email set";

    // Skin image from backend — path like /images/skins/champions/ahri/default.jpg
    skinImage.value = data.favorite_skin_image || "";
    favoriteSkin.value = data.favorite_skin || "No favorite skin yet";
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
.profile-page-main {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  flex-wrap: wrap;
  gap: 40px;
  padding: 60px 40px;
  min-height: 80vh;
}

.subtitle {
  font-size: 0.9rem;
  color: var(--text-muted);
  margin-bottom: 18px;
}

.info-field {
  margin-bottom: 18px;
}

.info-field span {
  font-size: 0.9rem;
  color: var(--text-muted);
  display: block;
}

.info-field p {
  font-size: 1rem;
  color: var(--text-main);
  margin: 4px 0 0;
}

.skin-card {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.skin-image {
  width: 100%;
  border-radius: 12px;
  margin-top: 20px;
  object-fit: cover;
}

.skin-placeholder {
  width: 100%;
  height: 200px;
  margin-top: 20px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px dashed var(--border-subtle);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-muted);
  font-size: 0.9rem;
}

.skin-name {
  margin-top: 12px;
  font-size: 0.9rem;
  color: var(--text-muted);
}

@media (max-width: 768px) {
  .profile-page-main {
    flex-direction: column;
    align-items: center;
    padding: 32px 20px;
  }
}
</style>
