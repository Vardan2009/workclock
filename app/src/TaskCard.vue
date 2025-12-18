<script setup>
import { defineProps } from "vue";

import { removeTask } from "./stores/tasks";
import { formatSecondsToHMS } from "./util";

const props = defineProps(["task", "duration-modal"]);

import { ref } from "vue";

import { ClockIcon, TrashIcon } from "@heroicons/vue/16/solid";

const runningTaskId = ref(null);
const elapsedTime = ref(0);
let interval = null;

const gettingDeleted = ref(false);

const startNewInstance = async (task) => {
    const estTime = await props.durationModal.show(
        "Enter duration",
        "01:30:00",
    );
    if (!isNaN(estTime) && estTime > 0) {
        task.startNewInstance(estTime);
        runningTaskId.value = task.id;
        elapsedTime.value = 0;
        startTimer();
    }
};

const stopInstance = (task) => {
    task.stopCurrentInstance();
    clearInterval(interval);
    runningTaskId.value = null;
    elapsedTime.value = 0;
};

const startTimer = () => {
    if (interval) clearInterval(interval);
    interval = setInterval(() => {
        elapsedTime.value++;
    }, 1000);
};
</script>

<template>
    <div :class="{ card: true, disabled: gettingDeleted }">
        <h2 class="flex">
            <RouterLink :to="`/app/task/${task.id}`"
                >{{ task.icon }} {{ task.title }}</RouterLink
            >
            <button
                class="inline danger"
                style="font-size: 14px"
                :disabled="gettingDeleted"
                @click="
                    () => {
                        removeTask(task.id);
                        gettingDeleted = true;
                    }
                "
            >
                <TrashIcon class="inline-icon" />
            </button>
        </h2>

        <template
            v-if="runningTaskId === task.id && task.currentRunningInstance"
        >
            <ClockIcon class="inline-icon" /> Running... Estimated:
            {{ formatSecondsToHMS(task.currentRunningInstance.estDurationSec) }}
            Elapsed: {{ formatSecondsToHMS(elapsedTime) }}<br />
            <button class="danger" @click="stopInstance(task)">
                Complete Task
            </button>
        </template>
        <template v-else>
            Avg. estimate: {{ formatSecondsToHMS(task.getAvgEstTime()) }}<br />
            Avg. actual: {{ formatSecondsToHMS(task.getAvgRealTime()) }}<br />
            Avg. bias: {{ formatSecondsToHMS(task.getAvgTimeBias()) }} ({{
                task.getAvgTimeBiasPercentage()?.toFixed(1)
            }}%)<br />
            <button
                :disabled="gettingDeleted"
                class="full-width"
                @click="startNewInstance(task)"
            >
                Start Tracking
            </button>
        </template>
    </div>
</template>

<style scoped>
div.card {
    background-color: var(--bg-alt);
    border-radius: 8px;
    padding: 15px;
    margin: 15px 0px;
    transition: opacity 0.3s ease-in-out;
}

div.card * {
    transition: opacity 0.3s ease-in-out;
}

div.card.disabled {
    opacity: 0.5;
}
</style>
