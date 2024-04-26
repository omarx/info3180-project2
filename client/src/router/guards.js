import { useRouter } from 'vue-router';
import {useStore} from "vuex";

export default function (to, from, next) {
    const router = useRouter();
    const store = useStore();

    if (!store.state.token && to.path !== '/login') {
        router.push('/login');
    } else {
        next();
    }
}