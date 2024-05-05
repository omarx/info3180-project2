<script setup>
import { useStore } from "vuex";
import { computed } from "vue";

const store = useStore();
const myID = computed(() => store.state.userId);
const userProfilePath = computed(() => `/profile/${myID.value}`);

const logout = () => {
  store.dispatch('logout');
}
</script>


  <template>
    <nav class="navbar navbar-expand-lg navbar-dark mb-3 bg-primary">
      <router-link to="/" class="navbar-brand p-2">
        <img class="photoLogo" src="/images/photo.svg" alt="logo"/> Photogram
      </router-link>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarColor02" aria-controls="navbarColor02" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarColor02">
        <div class="navbar-nav ms-auto">
          <router-link to="/" class="nav-link" active-class="active">Home</router-link>
          <router-link to="/explore" class="nav-link" active-class="active">Explore</router-link>
          <router-link :to="userProfilePath" class="nav-link" active-class="active">My Profile</router-link>
          <template v-if="!store.state.token">
            <router-link to="/login" class="nav-link" active-class="active">Login</router-link>
          </template>
          <template v-if="store.state.token">
            <span class="nav-link" @click="logout">Logout</span>
          </template>
        </div>
      </div>
    </nav>
  </template>



<style scoped>
.navbar {
  background-color: #4b90e3;
  color: white;
}
.navbar-brand {
  font-family: "Lobster", sans-serif;
  font-weight: 400;
  font-style: normal;
  font-size: 1.5em;
}
.photoLogo {
  height: 4vh;
  padding: 2px;
}
</style>
