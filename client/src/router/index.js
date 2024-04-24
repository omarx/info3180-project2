import { createRouter, createWebHistory } from 'vue-router';
import home from '../pages/home.vue';
import explore from '../pages/explore.vue';
import profile from '../pages/profile.vue';
import login from '../pages/login.vue';

const routes = [
    { path: '/', component: home },
    { path: '/explore', component: explore },
    { path: '/profile', component: profile },
    { path: '/login', component: login }
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

export default router;
