<script setup>
import navbar from "../components/navbar.vue";
</script>

<template>
<navbar/>
  <div class="container">
<div class="card">
  <div class="card-body">
    <div class="row">
      <div class="col-sm-3">
        <img src="/images/sunset-beach.jpg" class="img-fluid profile-pic" alt="logo"/>
      </div>
      <div class="col col-xl-6">
        <h1>Rosa Diza</h1>
        <p>test</p>
        <p>test2</p>
        <p>test3</p>
      </div>
      <div class="col col-md">
        <p>test col</p>
      </div>
    </div>
  </div>
</div>
  </div>
</template>

<style scoped>
.col-md {
  height: 100%;
}
.profile-pic {
  width: 200px;
  height: 200px;
  border-radius: 50%;
  object-fit: cover;
}
</style>

