import { ref, computed, watch } from 'vue'
import { themes } from '../themes'

const STORAGE_KEY = 'user-local-theme'

const savedTheme = localStorage.getItem(STORAGE_KEY)
const currentThemeId = ref(
  themes.some(t => t.id === savedTheme) ? savedTheme : 'light'
)

const currentTheme = computed(() =>
  themes.find(t => t.id === currentThemeId.value) ?? themes[0]
)

function setTheme(themeOrId) {
  const id = typeof themeOrId === 'string'
    ? themeOrId
    : themeOrId.id

  if (themes.some(t => t.id === id)) {
    currentThemeId.value = id
  }
}

watch(
  currentThemeId,
  (newId, oldId) => {
    if (oldId) document.body.classList.remove(oldId)
    document.body.classList.add(newId)

    localStorage.setItem(STORAGE_KEY, newId)
  },
  { immediate: true }
)

export function useTheme() {
  return {
    themes,
    currentTheme,
    setTheme,
  }
}
