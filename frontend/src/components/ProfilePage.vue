<template>
  <div class="profile-page-main">
    
    <!-- LEFT: Profile Card -->
    <div class="profile-card">
      <h2>Profile</h2>
      <p>View your information</p>

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
    </div>

    <!-- RIGHT: Skin Card -->
    <div class="skin-card">
      <h2>Favorite Skin</h2>
      <img :src="skinImage" alt="favorite_skin_image" />
    </div>

  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();

// Sample data
const nickname = ref("ranpchu");
const email = ref("araymo@example.com");
const skinImage = ref("/default-skin.png"); // your skin image path

const goUpdateProfile = () => {
  router.push({ name: "UpdateProfile" });
};
</script>

<style scoped>
.profile-page-main {
  display: flex;
  justify-content: flex-start; /* align left */
  align-items: flex-start;     /* align top */
  gap: 40px;                   /* space between cards */
  padding: 60px 40px;
  min-height: 100vh;
  background: linear-gradient(to bottom, #0f172a 0%, #020617 100%);
}

/* Profile card */
.profile-card {
  width: 400px;
  padding: 30px;
  border-radius: 20px;
  background: #1e1e2f;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
}

.profile-card h2 {
  margin-bottom: 10px;
}

.info-field {
  margin-bottom: 18px;
}

.info-field span {
  font-size: 0.9rem;
  color: #aaa;
  display: block;
}

.info-field p {
  font-size: 1rem;
  color: white;
  margin: 4px 0 0;
}

.primary-btn {
  margin-top: 10px;
  width: 100%;
  padding: 14px;
  border-radius: 12px;
  border: none;
  background: #6366f1;
  color: white;
  font-size: 1rem;
  cursor: pointer;
}

.primary-btn:hover {
  background: #4f46e5;
}

/* Skin card */
.skin-card {
  width: 400px;
  padding: 30px;
  border-radius: 20px;
  background: #1e1e2f;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
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
</style>