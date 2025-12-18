<script setup>
import { useRoute, RouterLink } from "vue-router";
import { store } from "@/stores/tasks";
import { formatSecondsToHMS } from "@/util";
import { onMounted, onBeforeUnmount } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();

const route = useRoute();
const taskId = parseInt(route.params.id);

const task = store.tasks.find((t) => t.id === taskId);

onMounted(() => {
    document.addEventListener("keydown", onEsc);
});

onBeforeUnmount(() => {
    document.removeEventListener("keydown", onEsc);
});

const onEsc = (e) => {
    if (e.key === "Escape") {
        router.push("/");
    }
};
</script>

<template>
    <div v-if="task">
        <p><RouterLink to="/">Tasks</RouterLink> / {{ task.title }}</p>
        <h1 class="italic title">{{ task.icon }} {{ task.title }}</h1>

        <div class="stats">
            <p>
                Avg. Estimated Time:
                {{ formatSecondsToHMS(task.getAvgEstTime()) }}
            </p>
            <p>
                Avg. Actual Time:
                {{ formatSecondsToHMS(task.getAvgRealTime()) }}
            </p>
            <p>
                Avg. Bias: {{ formatSecondsToHMS(task.getAvgTimeBias()) }} ({{
                    task.getAvgTimeBiasPercentage()?.toFixed(1)
                }}%)
            </p>
            <p>Total Instances: {{ task.taskInstances.length }}</p>
        </div>

        <hr />

        <h3>Task Instances</h3>
        <div v-if="task.taskInstances.length === 0" class="empty">
            <p>No instances yet. Start tracking!</p>
        </div>
        <ul v-else>
            <li
                v-for="(instance, index) in task.taskInstances"
                :key="index"
                class="instance"
            >
                <strong>Instance {{ index + 1 }}</strong>
                <p>
                    Started:
                    {{ new Date(instance.timestampStarted).toLocaleString() }}
                </p>
                <p>
                    Estimated: {{ formatSecondsToHMS(instance.estDurationSec) }}
                </p>
                <p>
                    Actual: {{ formatSecondsToHMS(instance.realDurationSec) }}
                </p>
                <p>
                    Bias: {{ formatSecondsToHMS(instance.getTimeBias()) }} ({{
                        (
                            (instance.getTimeBias() / instance.estDurationSec) *
                            100
                        ).toFixed(1)
                    }}%)
                </p>
            </li>
        </ul>
    </div>
    <div v-else>
        <p>Task not found</p>
    </div>
</template>

<style scoped></style>
