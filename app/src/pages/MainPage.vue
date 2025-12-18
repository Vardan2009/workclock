<script setup>
import { onBeforeUnmount, onMounted } from "vue";
import { addTask, loadTasks } from "@/stores/tasks";
import TaskCard from "@/TaskCard.vue";
import { store } from "@/stores/tasks";
import { RouterLink, useRouter } from "vue-router";

import { ref } from "vue";

import TimeDurationModal from "@/TimeDurationModal.vue";

import { getUser, logout } from "@/auth";

const router = useRouter();

let currentUser = await getUser();

const durationModal = ref(null);

const newTaskShortcut = async (e) => {
    console.log(e.ctrlKey, e.shiftKey, e.key);
    if (e.ctrlKey && e.key === "N" && e.shiftKey) {
        e.preventDefault();
        await router.push("/new-task");
    }
};

onMounted(async () => {
    await loadTasks();
    document.addEventListener("keydown", newTaskShortcut);
});

onBeforeUnmount(() => {
    document.removeEventListener("keydown", newTaskShortcut);
});

const logoutBtn = () => {
    logout();
    router.push("/login");
};

import {
    RectangleStackIcon,
    ArrowLeftEndOnRectangleIcon,
} from "@heroicons/vue/16/solid";

const btnAddTask = async () => {
    const taskName = prompt("Enter task name:");
    if (taskName) await addTask(taskName);
};

const onEnter = (el) => {
    const index = el.dataset.index;
    el.style.transitionDelay = `${index * 0.15}s`;
};
</script>

<template>
    <div class="flex" style="gap: 30px; flex-wrap: wrap">
        <h1 class="italic title">Hello, {{ currentUser.username }}!</h1>
        <button @click="logoutBtn">
            <ArrowLeftEndOnRectangleIcon class="inline-icon" />
            Log out
        </button>
    </div>

    <h3><RectangleStackIcon class="inline-icon" /> Your Tasks</h3>

    <RouterLink to="/app/new-task">
        <button class="full-width">
            + Add Task
            <span class="italic translucent">(Ctrl+Shift+N)</span>
        </button>
    </RouterLink>

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
                :duration-modal="durationModal"
            />
        </TransitionGroup>
    </div>

    <TimeDurationModal ref="durationModal" />
</template>
