<script setup>
import navbar from "@/components/navbar.vue";
import {ref,computed} from 'vue';
import {useStore} from 'vuex';
import Swal from "sweetalert2";
import {useRouter} from "vue-router";

const store = useStore();
const router = useRouter();
const csrfToken = computed(() => store.state.csrfToken)
const userId=computed(() => store.state.userId);
const jwtToken = computed(() => store.state.token);

const file = ref(null);

const handleFileChange = (event) => {
  file.value = event.target.files[0];  // Update file ref to the selected file
  if (!file.value) {
    Swal.fire({
      icon: 'error',
      title: 'Error',
      text: 'Please upload a profile photo'
    });
    return;
  }
  const extension = file.value.name.split('.').pop().toLowerCase();
  const allowedExtensions = ['jpg', 'jpeg', 'png'];
  if (!allowedExtensions.includes(extension)) {
    Swal.fire({
      icon: 'error',
      title: 'Error',
      text: 'Invalid file format. Only ' + allowedExtensions.join(', ') + ' allowed.'
    });
    file.value = null;  // Reset file input if invalid
  }
};

const newPost=async(event)=>{
  event.preventDefault();
  const formData=new FormData(event.target);
  if(file.value){
    formData.append('photo',file.value);
  }
  formData.append('user_id',userId.value);
  try{
    const response = await fetch('/api/v1/posts/new', {
      method: 'POST',
      headers:{
        'X-CSRFToken': csrfToken.value,
        'Authorization': `Bearer ${jwtToken.value}`
      },
      body:formData
    });
    const data = await response.json();

    if (!response.ok) {
      let errorMessage = 'Unable to add post';
      if (data.errors && data.errors.length > 0) {
        errorMessage = data.errors.join(' '); // Join multiple errors into a single message
      }
      Swal.fire({
        icon: 'error',
        title: 'Unable to add post',
        text: errorMessage
      });
      return;
    }

    Swal.fire({
      icon: 'success',
      title: 'Success',
      text: 'Post successfully saved',
    });
    router.push('/');
  } catch (error) {
    Swal.fire({
      icon: 'error',
      title: 'Error',
      text: 'Unable to add post: ' + error.message
    });
  }
};

</script>

<template>
  <navbar/>
  <div class="container mt-5 d-flex justify-content-center">
    <form class="mb-3 p-2 w-50" @submit.prevent="newPost">
      <h1>New Post</h1>
      <div class="card">
        <div class="card-body p-4">
          <h4>Photo</h4>
          <input type="file" id="photo" name="photo" class="form-control mb-3" @change="handleFileChange" required/>
          <h4>Caption</h4>
          <div class="mb-3">
            <textarea id="caption" name="caption" cols="30" rows="4" placeholder="Write a caption..." class="form-control" required></textarea>
          </div>
          <button type="submit" class="btn btn-success mt-3 w-75">Submit</button>
        </div>
      </div>
    </form>
  </div>
</template>


<style scoped>

.btn-success{
  background-color: #7ed321;
  border-color: #7ed321;
  width:18rem;
}
</style>