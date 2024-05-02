import { createStore } from 'vuex';
import VuexPersistence from 'vuex-persist';
import Swal from 'sweetalert2';

const vuexLocal = new VuexPersistence({
    storage: window.localStorage
})

export default createStore({
    state: {
        token: null,
    },
    mutations: {
        setToken(state, token) {
            state.token = token;
        },
        removeToken(state) {
            state.token = null;
        }
    },
    actions: {
        async login({ commit }, credentials) {
            try {
                const response = await fetch('/api/v1/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(credentials)
                });
                const data = await response.json();
                if (data.token) {
                    commit('setToken', data.token);
                    Swal.fire({
                        icon: 'success',
                        title: 'Login Successful',
                    })
                } else {
                    throw new Error(data.message || 'Failed to retrieve token.');
                }
            } catch (error) {
                console.error('Login failed:', error.message);
                Swal.fire({
                    icon: 'error',
                    title: 'Login failed',
                    text: 'Wrong username or password',
                })
            }
        },
        logout({ commit }) {
            commit('removeToken');
            window.location.reload();
        }
    },
    plugins: [vuexLocal.plugin]
});
