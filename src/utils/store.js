import { createStore } from 'vuex';
import VuexPersistence from 'vuex-persist';
import Swal from 'sweetalert2';

const vuexLocal = new VuexPersistence({
    storage: window.localStorage
});

export default createStore({
    state: {
        token: null,
        csrfToken: null,
        userId:null
    },
    mutations: {
        setToken(state, token) {
            state.token = token;
        },
        removeToken(state) {
            state.token = null;
        },
        setUserId(state, userId) {
            state.userId = userId;
        },
        removeUserId(state) {
            state.userId = null;
        },
        setCsrfToken(state, csrfToken) {  // Mutation to set CSRF token
            state.csrfToken = csrfToken;
        },
        removeCsrfToken(state) {  // Clear CSRF token
            state.csrfToken = null;
        }
    },
    actions: {
        async fetchCsrfToken({ commit }) {
            try {
                const response = await fetch('/api/v1/csrf-token');
                const data = await response.json();
                commit('setCsrfToken', data.csrf_token);
            } catch (error) {
                console.error('Error fetching CSRF token:', error);
            }
        },
        async login({ commit, state }, credentials) {
            try {
                console.log(state.csrfToken);
                const response = await fetch('/api/v1/auth/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': state.csrfToken  // Use CSRF token from state
                    },
                    body: JSON.stringify(credentials)
                });
                const data = await response.json();

                if (data.access_token) {
                    commit('setToken', data.access_token);
                    commit('setUserId', data.user_id);
                    console.log(data.user_id);
                    Swal.fire({
                        icon: 'success',
                        title: 'Login Successful',
                    });
                } else {
                    throw new Error(data.message || 'Failed to retrieve token.');
                }
            } catch (error) {
                console.error('Login failed:', error.message);
                Swal.fire({
                    icon: 'error',
                    title: 'Login failed',
                    text: 'Wrong username or password',
                });
            }
        },
        logout({ commit }) {
            commit('removeToken');
            commit('removeCsrfToken');// Also clear CSRF token on logout
            commit("removeUserId");
            window.location.reload();
        }
    },
    plugins: [vuexLocal.plugin]
});
