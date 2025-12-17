<script setup>
import { ref } from "vue";
import { register } from "@/auth";
import { useRouter, RouterLink } from "vue-router";

const username = ref("");
const password = ref("");
const error = ref(null);
const router = useRouter();

const blockInputs = ref(false);

async function submit() {
    if (blockInputs.value) return;

    error.value = null;
    blockInputs.value = true;
    try {
        await register(username.value, password.value);
        router.push("/app/login");
    } catch (err) {
        error.value = err.message;
    } finally {
        blockInputs.value = false;
    }
}
</script>

<template>
    <form @submit.prevent="submit">
        <h1>Register a new account</h1>
        <div class="flex" style="margin: 10px">
            <p class="danger" v-if="error">{{ error }}</p>
            <RouterLink to="/app/login"
                >Already have an account? Log in</RouterLink
            >
        </div>
        <input
            :disabled="blockInputs"
            v-model="username"
            placeholder="Username"
        />
        <input
            :disabled="blockInputs"
            v-model="password"
            type="password"
            placeholder="Password"
        />
        <button class="full-width" :disabled="blockInputs">Login</button>
    </form>
</template>
