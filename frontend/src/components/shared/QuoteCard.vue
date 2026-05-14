<!-- random quote card -->
<template>
  <div class="quote-card">
    <p class="quote-text">"{{ randomQuote.text }}"</p>
    <p class="quote-author">— {{ randomQuote.author }}</p>
  </div>
</template>

<script setup>
import { ref } from "vue";

const quotes = [
  { text: "The heart is the strongest muscle.", author: "Braum" },
  { text: "Never underestimate the power of the Scout's code.", author: "Teemo" },
  { text: "Precision is the difference between a butcher and a surgeon.", author: "Camille" },
  { text: "I am the weapon.", author: "Jax" },
  { text: "The unseen blade is the deadliest.", author: "Zed" },
  { text: "You can't stop the moon from rising.", author: "Diana" },
  { text: "In my dreams, I hold the world entire.", author: "Senna" },
  { text: "Patience is your greatest weapon.", author: "Caitlyn" },
];

const randomQuote = ref(quotes[Math.floor(Math.random() * quotes.length)]);
</script>

<style scoped>
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
