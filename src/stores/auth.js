import { reactive, computed } from "vue";

const state = reactive({
    accessToken: localStorage.getItem("access_token"),
    expiresAt: localStorage.getItem("expires_at"),
    user: null,
});

export const authStore = {
    state,

    isAuthenticated: computed(() => {
        return !!state.accessToken && !isTokenExpired();
    }),

    login(token, expiresIn) {
        const expiresAt = Date.now() + expiresIn * 1000;

        state.accessToken = token;
        state.expiresAt = expiresAt;

        localStorage.setItem("access_token", token);
        localStorage.setItem("expires_at", expiresAt);
    },

    logout() {
        state.accessToken = null;
        state.expiresAt = null;
        state.user = null;

        localStorage.removeItem("access_token");
        localStorage.removeItem("expires_at");
    },
};

function isTokenExpired() {
    if (!state.expiresAt) return true;
    return Date.now() > Number(state.expiresAt);
}
