import { createApp } from 'vue'
import App from './App.vue'
import './style.css'
import router from "./router/index";
import store from './utils/store.js';

const app = createApp(App);
app.use(store)
app.use(router);
app.mount('#app');
