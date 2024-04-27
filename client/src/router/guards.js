import { useRouter } from 'vue-router';
import { useStore } from "vuex";

export default function (to, from, next) {
    const router = useRouter();
    const store = useStore();

    const allowedRoutesWithoutAuth = ['/login', '/register']; // List of allowed routes

    if (!store.state.token && !allowedRoutesWithoutAuth.includes(to.path)) {
        router.push('/login');
    } else {
        next();
    }
}
