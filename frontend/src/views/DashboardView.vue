<template>
  <div class="auth-page">
    <div class="cards">
      <BrandHeader
        title="Dashboard"
        subtitle="Your skin collection hub."
      />

      <p class="home-subtitle">
        Welcome to your dashboard. Your collected skins will appear here.
      </p>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from "vue";
import { useRouter } from "vue-router";
import BrandHeader from "@/components/shared/BrandHeader.vue";

const router = useRouter();

onMounted(async () => {
  try {
    const res = await fetch("/api/dashboard", { credentials: "include" });
    if (!res.ok) {
      router.push({ name: "Login" });
    }
  } catch {
    router.push({ name: "Login" });
  }
});
</script>

<style scoped>
.auth-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
}

.home-subtitle {
  margin: 16px 0 0;
  color: var(--text-muted);
  font-size: 0.95rem;
  text-align: center;
}
</style>
