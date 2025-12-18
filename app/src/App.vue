<script setup>
import { useRoute } from "vue-router";
import { Suspense } from "vue";

const route = useRoute();
</script>

<template>
    <Suspense>
        <div class="content-width">
            <div class="floating-corner">
                <span class="italic">
                    <span style="font-weight: 1000">Work</span>Clock
                </span>
                |
                <a
                    href="https://github.com/Vardan2009/time-manager-app"
                    target="_blank"
                    >GitHub</a
                >
            </div>

            <Transition name="slide" mode="out-in">
                <div :key="route.path">
                    <div>
                        <router-view></router-view>
                    </div>
                </div>
            </Transition>
        </div>

        <template #fallback> <h1>Loading...</h1></template>
    </Suspense>
</template>

<style>
@import url("https://fonts.googleapis.com/css2?family=Funnel+Display:wght@300..800&display=swap");

:root {
    --bg: #e8e8e8;
    --bg-alt: #ffffff;

    --fg: #333;

    --accent1: #4e598c;
    --accent1-hover: #3b4470;

    --accent2: #ff8c42;
    --accent2-hover: #e67624;

    --danger: #ff4c4c;
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
    font: inherit;
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

button[disabled] {
    opacity: 0.5;
    cursor: not-allowed;
    background-color: var(--accent1-hover);
}

button[disabled].danger {
    background-color: var(--danger-hover);
}

p.danger {
    color: var(--danger);
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

.slide-enter-active,
.slide-leave-active {
    transition: all 0.3s ease;
}

.slide-enter-from {
    opacity: 0;
    transform: translateY(10px) scale(1.01);
    filter: blur(3px);
}

.slide-leave-to {
    opacity: 0;
    transform: translateY(-10px) scale(0.99);
    filter: blur(3px);
}

.slide-enter-to,
.slide-leave-from {
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

input {
    padding: 10px;
    font-size: 16px;
    border: 2px solid var(--accent1);
    border-radius: 5px;
    width: 100%;
    box-sizing: border-box;
    margin-bottom: 20px;
}

button.full-width {
    width: 100%;
    font-size: 18px;
}

div.floating-corner {
    font-size: 14pt;
    font-style: italic;
    z-index: -10;
}

.translucent {
    opacity: 0.6;
}

* {
    -ms-overflow-style: none;
    scrollbar-width: none;
}

::-webkit-scrollbar {
    display: none;
}
</style>
