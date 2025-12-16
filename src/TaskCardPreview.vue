<script setup>
import { defineProps } from "vue";

const props = defineProps(["taskTitle", "taskIcon"]);
</script>

<template>
    <div class="card">
        <h2 class="flex">
            <template v-if="taskTitle != ''">
                {{ taskIcon ? taskIcon : "📝" }} {{ taskTitle }}
            </template>
            <template v-else>
                <span class="italic" style="opacity: 0.5"
                    >{{ taskIcon ? taskIcon : "📝" }} New Task</span
                >
            </template>
            <button class="inline danger">X</button>
        </h2>
        Avg. estimate: N/A<br />
        Avg. actual: N/A<br />
        Avg. bias: N/A<br />
        <button>Start Tracking</button>
    </div>
</template>

<style scoped>
div.card {
    background-color: var(--bg-alt);
    border-radius: 8px;
    padding: 15px;
    margin: 15px 0px;
}
</style>
