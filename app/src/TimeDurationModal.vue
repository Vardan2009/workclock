<script setup>
import { ref, defineExpose } from "vue";
import { Transition } from "vue";

const visible = ref(false);
const title = ref("Enter duration");
const hours = ref(0);
const minutes = ref(0);
const seconds = ref(0);

let resolvePromise = null;

function show(initialTitle = "Enter duration", defaultValue = "00:00:00") {
    title.value = initialTitle;

    const parts = defaultValue.split(":").map(Number);
    hours.value = parts[0] || 0;
    minutes.value = parts[1] || 0;
    seconds.value = parts[2] || 0;

    visible.value = true;

    return new Promise((resolve) => {
        resolvePromise = resolve;
    });
}

function ok() {
    const h = Number(hours.value);
    const m = Math.min(Math.max(Number(minutes.value), 0), 59);
    const s = Math.min(Math.max(Number(seconds.value), 0), 59);
    const totalSeconds = h * 3600 + m * 60 + s;

    visible.value = false;
    resolvePromise && resolvePromise(totalSeconds);
    resolvePromise = null;
}

function cancel() {
    visible.value = false;
    resolvePromise && resolvePromise(null);
    resolvePromise = null;
}

defineExpose({ show, ok, cancel });
</script>

<template>
    <Transition name="slide">
        <div v-if="visible" class="modal-overlay">
            <div class="modal">
                <h3>{{ title }}</h3>
                <div class="inputs">
                    <input
                        type="number"
                        v-model.number="hours"
                        min="0"
                        placeholder="hh"
                    />
                    :
                    <input
                        type="number"
                        v-model.number="minutes"
                        min="0"
                        max="59"
                        placeholder="mm"
                    />
                    :
                    <input
                        type="number"
                        v-model.number="seconds"
                        min="0"
                        max="59"
                        placeholder="ss"
                    />
                </div>
                <div class="buttons">
                    <button class="full-width" @click="ok">OK</button>
                    <button class="full-width" @click="cancel">Cancel</button>
                </div>
            </div>
        </div>
    </Transition>
</template>

<style scoped>
.modal-overlay {
    position: fixed;
    top: -30px;
    left: -30px;
    width: calc(100% + 30px);
    height: calc(100% + 30px);
    background: rgba(0, 0, 0, 0.5);
    backdrop-filter: blur(3px);
    display: flex;
    justify-content: center;
    align-items: center;
}

.modal {
    background: white;
    padding: 20px;
    border-radius: 6px;
    text-align: center;
}

.inputs input {
    width: 100px;
    text-align: center;
    margin: 0 2px;
}

.buttons {
    margin-top: 30px;
}

.buttons button {
    margin: 5px;
}
</style>
