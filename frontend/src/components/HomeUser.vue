<template>
    <div class="home-page">
        <h1>Welcome Back, {{ username }}!</h1>
        <p class="home-subtitle">
          Good to see you again, ready to collect some skins?
        </p>

        <div class="quote-card">
        <p class="quote-text">“{{ randomQuote.text }}”</p>
        <p class="quote-author">— {{ randomQuote.author }}</p>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from "vue";

const username = ref("");

onMounted(async () => {
  try {
    const res = await fetch("http://127.0.0.1:5000/api/user", {
      credentials: "include",
    });
    const data = await res.json();
    username.value = data.username || "Summoner";
  } catch (err) {
    username.value = "Summoner";
  }
});

const quotes = [
  {
    text: "The heart is the strongest muscle.",
    author: "Braum",
  },
  {
    text: "Never underestimate the power of the Scout's code.",
    author: "Teemo",
  },
  {
    text: "Precision is the difference between a butcher and a surgeon.",
    author: "Camille",
  },
  {
    text: "I am the weapon.",
    author: "Jax",
  },
  {
    text: "The unseen blade is the deadliest.",
    author: "Zed",
  },
];

// Pick random quote
const randomQuote = ref(
  quotes[Math.floor(Math.random() * quotes.length)]
);
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


