<script setup>
import { ref, defineExpose, useTemplateRef } from "vue";
import { Transition } from "vue";

const visible = ref(false);
const title = ref("Enter duration");
const hours = ref(0);
const minutes = ref(0);
const seconds = ref(0);

import { nextTick, onMounted, onBeforeUnmount } from "vue";

let resolvePromise = null;

const hourInput = useTemplateRef("hourInput");

async function show(initialTitle = "Enter duration") {
    title.value = initialTitle;

    hours.value = "";
    minutes.value = "";
    seconds.value = "";

    visible.value = true;
    await nextTick();
    hourInput.value.focus();

    return new Promise((resolve) => {
        resolvePromise = resolve;
    });
}

onMounted(() => {
    document.addEventListener("keydown", onEsc);
});

onBeforeUnmount(() => {
    document.removeEventListener("keydown", onEsc);
});

const onEsc = (e) => {
    if (e.key === "Escape") {
        cancel();
    }
};

function ok() {
    const h = Number(hours.value) || 0;
    const m = Math.min(Math.max(Number(minutes.value) || 0, 0), 59);
    const s = Math.min(Math.max(Number(seconds.value) || 0, 0), 59);
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
    <Transition name="fade">
        <div v-if="visible" class="modal-overlay" @click="cancel">
            <div class="modal" @click.stop>
                <h2>{{ title }}</h2>
                <div class="time-input-group">
                    <div class="input-unit">
                        <input
                            ref="hourInput"
                            type="number"
                            v-model.number="hours"
                            min="0"
                            placeholder="0"
                            inputmode="numeric"
                            class="time-input"
                        />
                    </div>
                    <span class="separator">:</span>
                    <div class="input-unit">
                        <input
                            type="number"
                            v-model.number="minutes"
                            min="0"
                            max="59"
                            placeholder="0"
                            inputmode="numeric"
                            class="time-input"
                        />
                    </div>
                    <span class="separator">:</span>
                    <div class="input-unit">
                        <input
                            type="number"
                            v-model.number="seconds"
                            min="0"
                            max="59"
                            placeholder="0"
                            inputmode="numeric"
                            class="time-input"
                        />
                    </div>
                </div>
                <div class="buttons">
                    <button class="btn btn-primary" @click="ok">Confirm</button>
                    <button class="btn btn-secondary" @click="cancel">Cancel</button>
                </div>
            </div>
        </div>
    </Transition>
</template>

<style scoped>
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
    padding: 20px;
}

.modal {
    background: var(--bg-alt);
    padding: 24px;
    border-radius: 5px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    width: 100%;
    max-width: 340px;
}

h2 {
    margin: 0 0 24px;
    font-size: 20px;
    color: var(--text-primary);
}

.time-input-group {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 8px;
    margin-bottom: 28px;
}

.input-unit {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
}

.time-input {
    width: 70px;
    padding: 12px 8px;
    font-size: 28px;
    font-weight: 600;
    text-align: center;
    border: 2px solid var(--border-color);
    border-radius: 8px;
    background: var(--bg-primary);
    color: var(--text-primary);
    transition: border-color 0.2s;
    margin: 0;
}

.time-input::placeholder {
    color: var(--text-secondary);
    opacity: 0.1;
}

.input-unit label {
    font-size: 12px;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 0.5px;
    font-weight: 500;
}

.separator {
    font-size: 28px;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 6px;
}

.buttons {
    display: flex;
    gap: 12px;
    flex-direction: column;
}

.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
    opacity: 0;
}

@media (max-width: 480px) {
    .modal {
        padding: 20px;
    }

    .time-input {
        width: 60px;
        padding: 10px 6px;
        font-size: 24px;
    }

    .separator {
        font-size: 24px;
    }

    .btn {
        padding: 14px 12px;
        font-size: 16px;
    }
}
</style>