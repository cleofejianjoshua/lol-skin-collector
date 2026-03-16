<template>
  <div class="home-page">
    <h1>Welcome to LOL Skin Gacha Collector</h1>
    <p class="home-subtitle">
      Track your skins, remember your favorites, and never forget that one legendary you’ve always wanted.
    </p>

    <div class="quote-card" v-for="(quote, i) in quotes" :key="i">
      <p class="quote-text">“{{ quote.text }}”</p>
      <p class="quote-author">— {{ quote.author }}</p>
    </div>
  </div>
</template>

<script setup>
const quotes = [
  {
    text: "The heart is the strongest muscle.",
    author: "Braum",
  },
];
</script>

<style scoped>
.home-page {
  max-width: 640px;
  padding: 32px 24px;
  margin: 0 auto;
  text-align: center;
}

.home-page h1 {
  margin-bottom: 8px;
  font-size: 2rem;
}

.home-subtitle {
  margin: 0 0 24px;
  color: var(--text-muted);
  font-size: 0.95rem;
}

.quote-card {
  margin: 12px 0;
  padding: 14px 16px;
  border-radius: 12px;
  background: rgba(15, 23, 42, 0.8);
  border: 1px solid var(--border-subtle);
}

.quote-text {
  margin: 0 0 6px;
  font-size: 0.95rem;
}

.quote-author {
  margin: 0;
  font-size: 0.8rem;
  color: var(--text-muted);
}
</style>