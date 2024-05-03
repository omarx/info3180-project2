import { createRouter, createWebHistory } from 'vue-router';
import home from '../pages/home.vue';
import explore from '../pages/explore.vue';
import profile from '../pages/profile.vue';
import login from '../pages/login.vue';
import register from '../pages/register.vue'
import addPost from '../pages/addPost.vue';
import guards from "./guards.js";

const routes = [
    { path: '/', component: home },
    { path: '/explore', component: explore },
    { path: '/profile', component: profile },
    { path: '/login', component: login },
    { path: '/register', component: register },
    { path: '/posts/new', component: addPost },
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

router.beforeEach(guards);
export default router;
