import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      "path": "/",
      "name": "main",
      "component": () => import("../pages/MainPage.vue")
    },
    {
      "path": "/task/:id",
      "name": "taskDetail",
      "component": () => import("../pages/TaskDetailPage.vue")
    },
    {
      "path": "/new-task",
      "name": "newTask",
      "component": () => import("../pages/NewTask.vue")
    }
  ],
});

export default router;