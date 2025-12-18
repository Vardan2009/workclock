import { createRouter, createWebHashHistory } from "vue-router";

import { authStore } from "@/stores/auth";

const router = createRouter({
    history: createWebHashHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: "/",
            name: "main",
            component: () => import("../pages/MainPage.vue"),
            meta: {
                requiresAuth: true,
            },
        },
        {
            path: "/login",
            name: "login",
            component: () => import("../pages/LoginPage.vue"),
        },
        {
            path: "/register",
            name: "register",
            component: () => import("../pages/RegisterPage.vue"),
        },
        {
            path: "/task/:id",
            name: "taskDetail",
            component: () => import("../pages/TaskDetailPage.vue"),
            meta: {
                requiresAuth: true,
            },
        },
        {
            path: "/new-task",
            name: "newTask",
            component: () => import("../pages/NewTask.vue"),
            meta: {
                requiresAuth: true,
            },
        },
    ],
});

router.beforeEach((to) => {
    if (to.meta.requiresAuth && !authStore.isAuthenticated.value)
        return { name: "login" };
});

export default router;
