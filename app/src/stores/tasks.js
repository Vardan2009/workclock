import { reactive } from "vue";
import { apiFetch } from "@/api";

export class TaskInstance {
    constructor(taskId, estDurationSec, realDurationSec, timestampStarted) {
        this.taskId = taskId;
        this.estDurationSec = estDurationSec;
        this.realDurationSec = realDurationSec;
        this.timestampStarted = timestampStarted;
    }

    getTimeBias() {
        return this.realDurationSec - this.estDurationSec;
    }
}

export class Task {
    constructor(id, title, icon) {
        this.id = id;
        this.title = title;
        this.icon = icon || "📝";
        this.taskInstances = [];
        this.currentRunningInstance = undefined;
    }

    getAvgEstTime() {
        if (this.taskInstances.length === 0) return undefined;
        const totalEst = this.taskInstances.reduce(
            (sum, instance) => sum + instance.estDurationSec,
            0,
        );
        return totalEst / this.taskInstances.length;
    }

    getAvgRealTime() {
        if (this.taskInstances.length === 0) return undefined;
        const totalReal = this.taskInstances.reduce(
            (sum, instance) => sum + instance.realDurationSec,
            0,
        );
        return totalReal / this.taskInstances.length;
    }

    getAvgTimeBias() {
        if (this.taskInstances.length === 0) return undefined;
        const totalBias = this.taskInstances.reduce(
            (sum, instance) => sum + instance.getTimeBias(),
            0,
        );
        return totalBias / this.taskInstances.length;
    }

    getAvgTimeBiasPercentage() {
        const avgEst = this.getAvgEstTime();
        if (avgEst === undefined || avgEst === 0) return undefined;
        const avgBias = this.getAvgTimeBias();
        if (avgBias === undefined) return undefined;
        return (avgBias / avgEst) * 100;
    }

    startNewInstance(estDurationSec) {
        const newInstance = new TaskInstance(
            this.id,
            estDurationSec,
            0,
            Date.now(),
        );
        this.currentRunningInstance = newInstance;
    }

    getCurrentRunningInstanceElapsedTime() {
        if (this.currentRunningInstance) {
            const now = Date.now();
            const elapsedSec = Math.floor(
                (now - this.currentRunningInstance.timestampStarted) / 1000,
            );
            return elapsedSec;
        }
        return 0;
    }

    async stopCurrentInstance() {
        if (this.currentRunningInstance) {
            const now = Date.now();
            const elapsedSec = Math.floor(
                (now - this.currentRunningInstance.timestampStarted) / 1000,
            );
            this.currentRunningInstance.realDurationSec = elapsedSec;

            // Send to server
            await apiFetch(`/tasks/${this.id}/instances`, {
                method: "POST",
                body: JSON.stringify({
                    est_duration_sec:
                        this.currentRunningInstance.estDurationSec,
                    real_duration_sec: elapsedSec,
                    timestamp_started:
                        this.currentRunningInstance.timestampStarted,
                }),
            });

            this.taskInstances.push(this.currentRunningInstance);
            this.currentRunningInstance = undefined;
        }
    }
}

export const store = reactive({
    tasks: [],
});

export async function loadTasks() {
    try {
        const data = await apiFetch("/tasks");
        store.tasks = data.tasks.map((t) => new Task(t.id, t.title, t.icon));
        // Load instances
        store.tasks.forEach((task) => {
            const serverTask = data.tasks.find((st) => st.id === task.id);
            if (serverTask) {
                task.taskInstances = serverTask.task_instances.map(
                    (inst) =>
                        new TaskInstance(
                            inst.taskId,
                            inst.est_duration_sec,
                            inst.real_duration_sec,
                            inst.timestamp_started,
                        ),
                );
            }
        });
    } catch (err) {
        console.error("Failed to load tasks:", err);
    }
}

export async function addTask(title, icon) {
    try {
        const newTask = await apiFetch("/tasks", {
            method: "POST",
            body: JSON.stringify({ title, icon: icon || "📝" }),
        });
        store.tasks.push(new Task(newTask.id, newTask.title, newTask.icon));
    } catch (err) {
        console.error("Failed to add task:", err);
    }
}

export async function removeTask(id) {
    try {
        await apiFetch(`/tasks/${id}`, { method: "DELETE" });
        store.tasks = store.tasks.filter((task) => task.id !== id);
    } catch (err) {
        console.error("Failed to remove task:", err);
    }
}
