<script setup>
import navbar from "@/components/navbar.vue";
import { useStore } from "vuex";
import { computed, onMounted, ref } from "vue";
import { useRoute } from "vue-router";
import Swal from 'sweetalert2';

const store = useStore();
const jwtToken = computed(() => store.state.token);
const myID = computed(() => store.state.userId); // Ensure this correctly fetches the logged-in user's ID
const user = ref({});
const posts = ref([]);
const route = useRoute();
const csrfToken = computed(() => store.state.csrfToken);

const isMyProfile = computed(() => {
  return route.params.userId == myID.value; // Check if the profile belongs to the logged-in user
});

const isFollowing = computed(() => {
  return user.value.followers_ids && user.value.followers_ids.includes(myID.value);
});

const follow = async () => {
  const userId = route.params.userId;
  try {
    const response = await fetch(`/api/v1/users/${userId}/follow`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": `Bearer ${jwtToken.value}`,
        "X-CSRFToken": csrfToken.value
      }
    });
    if (response.ok) {
      await fetchUserInfo();
      Swal.fire({
        icon: 'success',
        title: 'Following',
        showConfirmButton: false,
        timer: 1500
      });
    } else {
      console.error('Failed to follow:', await response.text());
      throw new Error(`Failed to follow: ${response.status}`);
    }
  } catch (err) {
    console.error(`Error during follow action: ${err.message}`);
    Swal.fire({
      icon: 'error',
      title: 'Failed to Follow',
      text: 'There was a problem following the user.'
    });
  }
}


const fetchUserInfo = async () => {
  const userId = route.params.userId;
  try {
    const response = await fetch(`/api/v1/user/${userId}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": `Bearer ${jwtToken.value}`
      }
    });
    if (response.ok) {
      const data = await response.json();
      user.value = data;
    } else {
      console.error('Failed to fetch:', await response.text());
      throw new Error(`Failed to fetch data: ${response.status}`);
    }
  } catch (err) {
    console.error(`Error getting user information: ${err.message}`);
  }
}

const fetchPosts = async () => {
  const userId = route.params.userId;
  try {
    const response = await fetch(`/api/v1/users/${userId}/posts`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": `Bearer ${jwtToken.value}`
      }
    });
    if (response.ok) {
      const data = await response.json();
      posts.value = data;
    } else {
      console.error('Failed to fetch:', await response.text());
      throw new Error(`Failed to fetch data: ${response.status}`);
    }
  } catch (error) {
    console.error(`Error getting user posts: ${error.message}`);
  }
}

const formatDate = (dateString) => {
  const options = { month: 'long', year: 'numeric' };
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', options);
}

onMounted(() => {
  fetchUserInfo();
  fetchPosts();
});
</script>



<template>
  <navbar/>
  <div class="container p-2">
    <div class="card">
      <div class="card-body">
        <div class="row">
          <div class="col-sm-3">
            <img :src="`/api/v1/images/${user.profile_photo}`" class="img-fluid profile-pic" alt="User profile photo"/>
          </div>
          <div class="col col-xl-6">
            <h1>{{ user.first_name }} {{ user.last_name }}</h1>
            <p>{{ user.location }}</p>
            <p>Member since {{ formatDate(user.joined_on) }}</p>
            <p>{{ user.biography }}</p>
          </div>
          <div class="col col-md">
            <div class="row">
              <h4>{{ user.posts_count }}</h4>
              <h5>Posts</h5>
            </div>
          </div>
          <div class="col col-md">
            <div class="row">
              <h4>{{ user.follower_count }}</h4>
              <h5>Followers</h5>
            </div>
          </div>
          <div class="d-flex align-items-start justify-content-end" v-if="!isMyProfile">
            <button class="btn btn-primary follow-btn" v-if="!isFollowing" @click="follow" :disabled="followingLoading">Follow</button>
            <button class="btn btn-primary following-btn" v-if="isFollowing">Following</button>
          </div>
        </div>
      </div>
    </div>
    <div class="posts-container pt-3">
      <div class="row">
        <div class="col-md-4" v-for="post in posts" :key="post.post_id">
          <div class="post-card">
            <img :src="`/api/v1/images/${post.photo}`" alt="Post image" class="post-image">
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
h5{
  color:grey;
}
p{
  color:grey;
}
.follow-btn{
width:20%;
  padding:10px;
  font-size:1.2em;
  background-color:#4b90e3;
}
.post-card {
  margin-bottom: 20px;
  border: 1px solid #ccc;
  border-radius: 10px;
  overflow: hidden;
}

.post-image {
  width: 100%;
  height: 50vh;
  object-fit: cover;
}

.posts-container {
  margin-top: 20px;
}

.profile-pic {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  object-fit: cover;
  margin-right: 20px;
}

.follow-btn {
  width: 20%;
  padding: 10px;
  font-size: 1.2em;
  background-color: #4b90e3;
}

.following-btn {
  width: 20%;
  padding: 10px;
  font-size: 1.2em;
  background-color: #7ed321;
  border-color:#7ed321;
}

</style>

