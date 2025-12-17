<script setup>
import { ref } from "vue";
import { RouterLink } from "vue-router";

import TaskCardPreview from "@/TaskCardPreview.vue";

import { addTask } from "@/stores/tasks";

import { useRouter } from "vue-router";

import { onMounted, useTemplateRef, onBeforeUnmount } from "vue";

const router = useRouter();

const taskTitle = ref("");
const taskIcon = ref("");

const allTaskIcons = [
    "📝",
    "📚",
    "🛠️",
    "💼",
    "🎨",
    "🎵",
    "🏃‍♂️",
    "🍳",
    "🧹",
    "🚀",
];

const input = useTemplateRef("task-title-input");

onMounted(() => {
    input.value.focus();
    document.addEventListener("keydown", onEsc);
});

onBeforeUnmount(() => {
    document.removeEventListener("keydown", onEsc);
});

const onEsc = (e) => {
    if (e.key === "Escape") {
        router.push("/app");
    }
};

const createTask = () => {
    if (taskTitle.value.trim() === "") {
        alert("Task title cannot be empty.");
        return;
    }
    addTask(taskTitle.value.trim(), taskIcon.value || "📝");
    router.push("/app");
};
</script>

<template>
    <p><RouterLink to="/app">Tasks</RouterLink> / Create new task</p>

    <h1>Create new task</h1>

    <h3>Task Title</h3>
    <input
        ref="task-title-input"
        type="text"
        v-model="taskTitle"
        placeholder="Task Title"
    />

    <h3>Task Icon</h3>

    <div class="icon-grid">
        <button
            v-for="icon in allTaskIcons"
            :key="icon"
            @click="taskIcon = icon"
            :class="{ 'selected-icon': taskIcon === icon }"
            class="icon-button"
        >
            {{ icon }}
        </button>
    </div>

    <hr />

    <TaskCardPreview :taskTitle="taskTitle" :task-icon="taskIcon" />

    <hr />

    <button class="full-width" @click="createTask">Create Task</button>
</template>

<style>
.icon-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(50px, 1fr));
    gap: 10px;
    margin-bottom: 20px;
}

.icon-button {
    font-size: 24px;
    padding: 10px;
    border: 2px solid transparent;
    background-color: var(--bg-alt);
    border-radius: 8px;
    cursor: pointer;
    transition: border-color 0.3s;
}
</style>
