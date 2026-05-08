<!-- Reusable brand logo + title block.
     Props:
       title    (String) — e.g. "LOL Skin Collector"
       subtitle (String) — e.g. "Sign in to manage your collection."
-->
<template>
  <div class="brand">
    <div class="logo-circle">
      <span class="logo-text">LC</span>
    </div>
    <div class="brand-text">
      <h1>{{ title }}</h1>
      <p>{{ subtitle }}</p>
    </div>
  </div>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    default: "LOL Skin Collector",
  },
  subtitle: {
    type: String,
    default: "",
  },
});
</script>
