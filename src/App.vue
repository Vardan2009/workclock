<script setup>
import { useRoute } from 'vue-router';

const route = useRoute();
</script>

<template>
  <div class="content-width">
    <Transition  name="slide" mode="out-in">
      <div :key="route.path">
     <router-view></router-view>
      </div>
    </Transition>
  </div>
</template>

<style>
@import url('https://fonts.googleapis.com/css2?family=Funnel+Display:wght@300..800&display=swap');

:root {
  --bg: #e8e8e8;
  --bg-alt: #ffffff;

  --fg: #333;
  
  --accent1: #4E598C;
  --accent1-hover: #3b4470;

  --accent2: #FF8C42;
  --accent2-hover: #e67624;

  --danger: #FF4C4C;
  --danger-hover: #e63b3b;
}

body {
  background-color: var(--bg);
  color: var(--fg);
  font-family: Arial, sans-serif;
  margin: 0;
  padding: 20px;

  font-family: "Funnel Display", sans-serif;
  font-optical-sizing: auto;
  font-style: normal;

  user-select: none;
}

button {
  background-color: var(--accent1);
  border: none;
  border-radius: 5px;
  color: white;
  cursor: pointer;
  padding: 10px 15px;
  margin-top: 10px;
}

button:hover {
  background-color: var(--accent1-hover);
}

button.inline {
  display: inline-block;
  width: 25px;
  height: 25px;
  padding: 0;
  margin: 0;
}

button.primary {
  background-color: var(--accent2);
}

button.primary:hover {
  background-color: var(--accent2-hover);
}

button.danger {
  background-color: var(--danger);
}

button.danger:hover {
  background-color: var(--danger-hover);
}

.flex {
  align-items: center;
  display: flex;
  gap: 10px;
}

a {
  color: var(--accent1);
  text-decoration: none;
}

a:hover {
  color: var(--accent1-hover);
}

.content-width {
  max-width: 800px;
  margin: auto;
}

.slide-enter-active, .slide-leave-active {
  transition: all 0.3s ease;
}

.slide-enter-from {
  opacity: 0;
  transform: translateY(10px);
}

.slide-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

.slide-enter-to, .slide-leave-from {
  opacity: 1;
  transform: translateY(0);
}

.italic {
  font-style: italic;
}

.title {
  font-weight: 800;
  font-size: 48px;
}

.inline-icon {
  display: inline-block;
  width: 1em;
  height: 1em;
  vertical-align: -0.15em;
}

</style>