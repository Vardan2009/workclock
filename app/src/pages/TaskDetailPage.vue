<script setup>
import { useRoute, RouterLink } from "vue-router";
import { store, updateTaskNote } from "@/stores/tasks";
import { formatSecondsToHMS } from "@/util";
import { onMounted, onBeforeUnmount } from "vue";
import { useRouter } from "vue-router";

import { ref } from "vue";

const router = useRouter();

const route = useRoute();
const taskId = parseInt(route.params.id);

const task = store.tasks.find((t) => t.id === taskId);

let debounceTimeout = null;

onMounted(() => {
    if(!task) 
        router.push("/");
    
    document.addEventListener("keydown", onEsc);
});

onBeforeUnmount(() => {
    document.removeEventListener("keydown", onEsc);
    if (debounceTimeout) clearTimeout(debounceTimeout);
});

const onEsc = (e) => {
    if (e.key === "Escape") {
        router.push("/");
    }
};

const unsavedChanges = ref(false)
const savingChanges = ref(false)
const taskNotesInput = ref(task.task_note)

const updateNote = () => {
    unsavedChanges.value = true;
    savingChanges.value = false;
    
    if (debounceTimeout) clearTimeout(debounceTimeout);
    
    debounceTimeout = setTimeout(async () => {
        savingChanges.value = true;
        await updateTaskNote(task.id, taskNotesInput.value);
        unsavedChanges.value = false;
        savingChanges.value = false;
    }, 300);
}

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
        <h3>
            Task notes
            <span v-if="unsavedChanges" class="danger">*</span>
            <span v-if="savingChanges" class="italic">Saving changes...</span>
        </h3>
        <textarea @input="updateNote" v-model="taskNotesInput" name="task-notes"></textarea>

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
                    {{ new Date(instance.timestamp_started).toLocaleString() }}
                </p>
                <p>
                    Estimated: {{ formatSecondsToHMS(instance.est_duration_sec) }}
                </p>
                <p>
                    Actual: {{ formatSecondsToHMS(instance.real_duration_sec) }}
                </p>
                <p>
                    Bias: {{ formatSecondsToHMS(instance.getTimeBias()) }} ({{
                        (
                            (instance.getTimeBias() / instance.est_duration_sec) *
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

<style scoped>
</style>