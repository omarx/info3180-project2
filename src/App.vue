<script setup>
import { computed, onMounted } from 'vue';
import { useStore } from 'vuex';

const store = useStore();

store.dispatch('fetchCsrfToken');

const csrfToken = computed(() => store.state.csrfToken);


onMounted(() => {
  setTimeout(() => {
    console.log('CSRF Token:', csrfToken.value);
  }, 1000);
});
</script>

<template>
  <router-view/>
</template>

<style scoped>
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
</style>
