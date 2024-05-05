<script setup>
import navbar from "../components/navbar.vue";
import { useRouter } from "vue-router";
import { computed, ref, onMounted } from "vue";
import { useStore } from 'vuex';

const store = useStore();
const jwtToken = computed(() => store.state.token);
const posts = ref([]);
const router = useRouter();

const addPost = () => {
  router.push("/posts/new");
}

const getPosts = async () => {
  try {
    const response = await fetch('/api/v1/posts', {
      method: "GET",
      headers: {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": `Bearer ${jwtToken.value}`
      }
    });
    if (response.ok) {
      const data = await response.json();
      if (Array.isArray(data)) {
        posts.value = data.map(post => ({
          ...post,
          date: formatDate(post.created_at)
        }));
      } else if (data && Array.isArray(data.posts)) {
        posts.value = data.posts.map(post => ({
          ...post,
          date: formatDate(post.created_at)
        }));
      } else {
        throw new Error('Data format is incorrect or empty');
      }
    } else {
      throw new Error(`Failed to fetch posts: ${response.status}`);
    }
  } catch (error) {
    console.error('Error fetching posts:', error);
  }
}


const formatDate = (dateString) => {
  const options = { day: '2-digit', month: 'long', year: 'numeric' };
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', options);
}


onMounted(getPosts);
</script>


<template>
  <div>
    <navbar/>
    <div class="container d-flex justify-content-evenly">
      <!-- Main posts column -->
      <div class="posts-col">
        <div class="row">
          <div class="col-md-12 mb-5 pb-3" v-for="post in posts" :key="post.id">
            <div class="card my-2">
              <router-link :to="`/users/${post.user_id}`" class="top-area" ><img :src="`/api/v1/images/${post.profile_photo}`" alt="{{post.username}} pic" class="img-fluid profile-image" /> &nbsp;{{post.username}}</router-link>
              <img :src="`/api/v1/images/${post.photo}`" class="card-img-top" alt="Post Image">
              <div class="card-body">
                <p class="card-text">{{ post.caption }}</p>
                <div class="d-flex justify-content-between">
                  <span><i class="bi bi-suit-heart"></i> {{ post.likes_count }} Likes</span>
                  <span>{{ post.date }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <!-- Sticky New Post button column -->
      <div class="new-post-col align-items-end justify-content-center">
        <button class="btn btn-primary sticky-button ml-3" @click="addPost">New Post</button>
      </div>
    </div>
  </div>
</template>


<style scoped>
.container {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.posts-col {
  width: 60%;
}

.new-post-col {
  width: 20%;
  position: sticky;
  top: 3vh;
  height: 50vh;
}

.sticky-button {
  width: 100%;
}

.card-img-top {
  width: 100%;
  height: auto;
}
.profile-image {
  width: 5vh;
  height: 5vh;
  border-radius: 50%;
}

.card-text{
  color:grey;
  padding-top:10px;
  padding-bottom:10px;
}
.top-area{
  padding:10px;
  text-decoration: none;
  color:black;
  font-size:1.1em;
}

</style>
