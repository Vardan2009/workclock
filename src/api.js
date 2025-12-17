import { authStore } from "@/stores/auth";

const API_BASE = "http://127.0.0.1:5000";

export async function apiFetch(endpoint, options = {}) {
    const headers = {
        "Content-Type": "application/json",
        ...(options.headers || {}),
    };

    if (authStore.state.accessToken) {
        headers.Authorization = `Bearer ${authStore.state.accessToken}`;
    }

    const response = await fetch(`${API_BASE}${endpoint}`, {
        ...options,
        headers,
    });

    const data = await response.json();

    if (data.error) throw new Error(data.error);

    if (response.status === 401) {
        authStore.logout();
        throw new Error("Unauthorized");
    }

    return data;
}
