import { reactive } from 'vue'

export class TaskInstance {
  constructor(taskId, estDurationSec, realDurationSec, timestampStarted) {
    this.taskId = taskId;
    this.estDurationSec = estDurationSec;
    this.realDurationSec = realDurationSec;

    this.timestampStarted = timestampStarted;
  };

  getTimeBias() {
    return this.realDurationSec - this.estDurationSec;
  };
};

export class Task {
  constructor(id, title, icon) {
    this.id = id;
    this.title = title;
    this.icon = icon || "📝";
    this.taskInstances = [];

    this.currentRunningInstance = undefined;
  };

  getAvgEstTime() {
    if (this.taskInstances.length === 0) return undefined;
    const totalEst = this.taskInstances.reduce((sum, instance) => sum + instance.estDurationSec, 0);
    return totalEst / this.taskInstances.length;
  };

  getAvgRealTime() {
    if (this.taskInstances.length === 0) return undefined;
    const totalReal = this.taskInstances.reduce((sum, instance) => sum + instance.realDurationSec, 0);
    return totalReal / this.taskInstances.length;
  };

  getAvgTimeBias() {
    if (this.taskInstances.length === 0) return undefined;
    const totalBias = this.taskInstances.reduce((sum, instance) => sum + instance.getTimeBias(), 0);
    return totalBias / this.taskInstances.length;
  };

  getAvgTimeBiasPercentage() {
    const avgEst = this.getAvgEstTime();
    if (avgEst === undefined || avgEst === 0) return undefined;
    const avgBias = this.getAvgTimeBias();
    if (avgBias === undefined) return undefined;
    return (avgBias / avgEst) * 100;
  };

  addTaskInstance(estDurationSec, realDurationSec) {
    const newInstance = new TaskInstance(this.id, estDurationSec, realDurationSec);
    this.taskInstances.push(newInstance);
  };

  startNewInstance(estDurationSec) {
    const newInstance = new TaskInstance(this.id, estDurationSec, 0, Date.now());
    this.currentRunningInstance = newInstance;
  };

  getCurrentRunningInstanceElapsedTime() {
    if (this.currentRunningInstance) {
      const now = Date.now();
      const elapsedSec = Math.floor((now - this.currentRunningInstance.timestampStarted) / 1000);
      return elapsedSec;
    }
    return 0;
  };

  stopCurrentInstance() {
    if (this.currentRunningInstance) {
      const now = Date.now();
      const elapsedSec = Math.floor((now - this.currentRunningInstance.timestampStarted) / 1000);
      this.currentRunningInstance.realDurationSec = elapsedSec;
      this.taskInstances.push(this.currentRunningInstance);
      this.currentRunningInstance = undefined;
    }
  };
};

export const store = reactive({
  tasks: [
    new Task(1, "Sample Task 1", "📚"),
    new Task(2, "Sample Task 2", "🛠️")
  ],
});

export function addTask(title, icon) {
  const id = store.tasks.length + 1;
  const newTask = new Task(id, title, icon);
  store.tasks.push(newTask);
};

export function removeTask(id) {
  store.tasks = store.tasks.filter(task => task.id !== id);
};

export function addTaskInstance(id, estDurationSec, realDurationSec) {
  const task = store.tasks.find(task => task.id === id);
  if (task) task.addTaskInstance(estDurationSec, realDurationSec);
};