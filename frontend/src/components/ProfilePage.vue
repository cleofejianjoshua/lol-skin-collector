<template>
  <div class="profile-page-main">
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

    <div class="skin-card">
      <h2>Favorite Skin</h2>
      <img :src="skinImage" alt="favorite skin image" />
      <p class="skin-name">{{ favoriteSkin }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter, onBeforeRouteUpdate } from "vue-router";

const router = useRouter();

const loading = ref(true);
const errorMsg = ref("");

const username = ref("");
const nickname = ref("");
const email = ref("");
const favoriteSkin = ref("No favorite skin yet");
const skinImage = ref("/default-skin.png");

const loadProfile = async () => {
  loading.value = true;
  errorMsg.value = "";

  try {
    const res = await fetch("/api/user)", {
      method: "GET",
      credentials: "include",
    });

    const data = await res.json();

    if (!res.ok) {
      throw new Error(data.error || "Failed to load profile.");      
    }

    username.value = data.username || "Unknown user";
    nickname.value = data.nickname || data.username || "No nickname set";
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

onMounted(() => {
  loadProfile();
});

onBeforeRouteUpdate(() => {
  loadProfile();
});
</script>

<style scoped>
.profile-page-main {
  display: flex;
  justify-content: flex-start;
  align-items: flex-start;
  gap: 40px;
  padding: 60px 40px;
  min-height: 100vh;
  background: linear-gradient(to bottom, #0f172a 0%, #020617 100%);
}

.profile-card,
.skin-card {
  width: 400px;
  padding: 30px;
  border-radius: 20px;
  background: var(--card-bg);
  box-shadow: var(--shadow-elevated);
  border: 1px solid var(--border-subtle);
}

.profile-card h2,
.skin-card h2 {
  margin: 0 0 8px;
  color: var(--text-main);
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

.primary-btn {
  margin-top: 10px;
  width: 100%;
  padding: 14px;
  border-radius: var(--radius-pill);
  border: none;
  background: radial-gradient(circle at 20% 0, #dbeafe, #60a5fa 40%, #1d4ed8);
  color: #0b1120;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: filter var(--transition-med);
}

.primary-btn:hover {
  filter: brightness(1.05);
}

.error-text {
  margin-top: 12px;
  font-size: 0.85rem;
  color: var(--danger);
}

.skin-card {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.skin-card img {
  width: 100%;
  border-radius: 12px;
  margin-top: 20px;
  object-fit: cover;
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
  }

  .profile-card,
  .skin-card {
    width: 100%;
    max-width: 460px;
  }
}
</style>
