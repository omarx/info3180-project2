import { createStore } from 'vuex';
import VuexPersistence from 'vuex-persist';

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
                const response = await fetch('http://localhost:3001/auth/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(credentials)
                });
                const data = await response.json();
                if (data.token) {
                    commit('setToken', data.token);
                } else {
                    throw new Error(data.message || 'Failed to retrieve token.');
                }
            } catch (error) {
                console.error('Login failed:', error.message);
            }
        },
        logout({ commit }) {
            commit('removeToken');
            window.location.reload();
        }
    },
    plugins: [vuexLocal.plugin]
});
