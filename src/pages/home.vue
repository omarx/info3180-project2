<script setup>
import navbar from "../components/navbar.vue";
import {useRouter} from "vue-router";
const router = useRouter();
router.push("/explore");
</script>

<template>
  <div>
    <navbar/>
  </div>
</template>

<style scoped>
</style>
