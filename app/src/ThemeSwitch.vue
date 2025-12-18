<script setup>
import { useTheme } from '@/stores/theme'

const { themes, currentTheme, setTheme } = useTheme()
</script>

<template>
  <div class="theme-switcher">
    <button
      v-for="theme in themes"
      :key="theme.id"
      class="inline"
      style=""
      :class="{ active: currentTheme.id === theme.id }"
      @click="setTheme(theme)"
      :title="theme.description"
    >
      {{ theme.icon }}
    </button>
  </div>
</template>

<style scoped>

.theme-switcher button {
    display: inline-block;
    font-style: normal;
    background-color: transparent;
    opacity: 0.5; 
    margin: 5px;
}

.theme-switcher button:hover {
    opacity: 1;
}

</style>