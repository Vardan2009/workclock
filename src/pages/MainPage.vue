<script setup>
import { addTask } from "@/stores/tasks";
import TaskCard from "@/TaskCard.vue";
import { store } from "@/stores/tasks";
import { RouterLink, useRouter } from "vue-router";

import { getUser, logout } from "@/auth";

const router = useRouter();

let currentUser = await getUser();

const logoutBtn = () => {
    logout();
    router.push("/app/login");
};

import {
    RectangleStackIcon,
    ArrowLeftEndOnRectangleIcon,
} from "@heroicons/vue/16/solid";

const btnAddTask = () => {
    const taskName = prompt("Enter task name:");
    if (taskName) addTask(taskName);
};

const onEnter = (el) => {
    const index = el.dataset.index;
    el.style.transitionDelay = `${index * 0.15}s`;
};
</script>

<template>
    <div class="flex">
        <h1>Hello, {{ currentUser.username }}!</h1>
        <button class="inline" @click="logoutBtn">
            <ArrowLeftEndOnRectangleIcon class="inline-icon" />
        </button>
    </div>

    <div class="flex">
        <h3><RectangleStackIcon class="inline-icon" /> Your Tasks</h3>
        <RouterLink to="/app/new-task">
            <button class="inline">+</button>
        </RouterLink>
    </div>

    <div v-if="store.tasks.length === 0" class="empty">
        <p class="italic">No tasks yet. Add one to get started!</p>
    </div>
    <div v-else>
        <TransitionGroup name="slide" tag="div" appear @enter="onEnter">
            <TaskCard
                v-for="(task, index) in store.tasks"
                :key="task.id"
                :task="task"
                :data-index="index"
            />
        </TransitionGroup>
    </div>
</template>
