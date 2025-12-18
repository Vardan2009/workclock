import { ref } from "vue";
import { apiFetch } from "./api";
import { authStore } from "@/stores/auth";

let currentUser = ref(null);

export async function login(username, password) {
    const data = await apiFetch("/login", {
        method: "POST",
        body: JSON.stringify({ username, password }),
    });

    authStore.login(data.access_token, data.expires_in);
}

export async function register(username, password) {
    return apiFetch("/register", {
        method: "POST",
        body: JSON.stringify({ username, password }),
    });
}

export async function logout() {
    await apiFetch("/logout", {
        method: "POST",
    });
    authStore.logout();
    currentUser.value = null;
}

export async function getUser() {
    if (currentUser.value) return currentUser;

    try {
        const data = await apiFetch("/user", {
            method: "GET",
        });
        currentUser.value = data;
    } catch (err) {
        throw new Error("Failed to fetch user data");
    }
    return currentUser;
}
