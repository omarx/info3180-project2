<script setup>
import {onMounted, ref} from 'vue';
import { useStore } from 'vuex';
import navbar from '../components/navbar.vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const store = useStore();
const showLogin = ref(false);




const toggleLoginForm = () => {
  showLogin.value = !showLogin.value;
}

if(store.state.token){
  router.push('/');

}

const login = async (event) => {
  event.preventDefault();

  const credentials = {
    username: document.getElementById('username').value,
    password: document.getElementById('password').value,
  };

  await store.dispatch('login', credentials);

  if (store.state.token) {
    console.log('Login successful!');
     router.push('/');
  } else {
    console.error('Login failed.');
  }
}
</script>

<template>
  <navbar/>
  <div class="container pt-3 mt-3">
    <div class="row mt-4">
      <div class="col-md">
        <img src="/images/sunset-beach.jpg" alt="" class="card-img-top register-img">
      </div>
      <div class="col-md d-flex flex-column align-items-center">
        <div class="card text-center">
          <div class="card-body" v-show="!showLogin">
            <span class="navbar-brand pt-2">
              <img class="photoLogo" src="/images/photo.svg" alt="logo"/> Photogram
            </span>
            <hr>
            <div class="col-md d-flex flex-column align-items-center">
              <p class="card-text p-2 pb-5 mb-5">
                Share photos of your favorite moments, with friends, family and the world
              </p>
            </div>
            <div class="row mb-4 d-flex justify-content-center align-items-center">
              <div class="col-md">
                <button class="btn btn-success text-center" @click="toggleLoginForm">Login</button>
              </div>
              <div class="col-md p-2">
                  <router-link to="/register" class="btn btn-primary text-center">Register</router-link>
              </div>
            </div>
          </div>

          <div class="login-form p-4" v-show="showLogin">
            <span class="navbar-brand pt-4">
              <img class="photoLogo" src="/images/photo.svg" alt="logo"/> Photogram
            </span>
            <hr>
            <form class="pt-4" @submit.prevent="login"> <div class="form-group mb-2 p-2">
              <label for="username">Username</label>
              <input type="text" class="form-control" id="username" placeholder="Enter username">
            </div>
              <div class="form-group mb-2 p-2">
                <label for="password">Password</label>
                <input type="password" class="form-control" id="password" placeholder="Enter password">
              </div>
              <button type="submit" class="btn btn-primary mt-4 p-2">Login</button>
              <div class="text-center mt-4" v-show="showLogin">
                Don't have a login? <router-link to="/register">Register Here</router-link>
              </div>
            </form>

          </div>

        </div>


      </div>
    </div>
  </div>
</template>

<style scoped>
.card {
  width: 100%;
  height: 100%;
}

.register-img {
  width: 100%;
}

.navbar-brand {
  font-family: "Lobster", sans-serif;
  font-weight: 400;
  font-style: normal;
  font-size: 2em;
}

.photoLogo {
  height: 4vh;
  padding: 2px;
}

hr {
  width: 80%;
}

.btn {
  width: 18rem;
}

.btn-success {
  background-color: #7ed321;
  border-color: #7ed321;
}

.btn-primary {
  background-color: #4a90e2;
  border-color: #4a90e2;
}

.card-text {
  font-size: 1.2em;
}

</style>
