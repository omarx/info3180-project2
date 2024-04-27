<script setup>
import navbar from "../components/navbar.vue";
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useStore } from "vuex";
import Swal from 'sweetalert2';

const file = ref(null);
const router = useRouter();
const store = useStore();

// Redirect if already logged in
if (store.state.token) {
  router.push('/');
}

// Handle file change with robust error handling
const handleFileChange = (event) => {
  const files = event.target.files;
  if (files.length === 0) {
    Swal.fire({
      icon: 'error',
      title: 'Error',
      text: 'Please upload a profile photo'
    });
    return;
  }

  const file = files[0];  // Directly use the file object
  const extension = file.name.split('.').pop().toLowerCase();
  const allowedExtensions = ['jpg', 'jpeg', 'png'];
  if (!allowedExtensions.includes(extension)) {
    Swal.fire({
      icon: 'error',
      title: 'Error',
      text: 'Invalid file format. Only ' + allowedExtensions.join(', ') + ' allowed.'
    });
    return;
  }

  file.value = file; // Directly assign the file to file.value
}


// Register new user with form data
const register = async (event) => {
  event.preventDefault();

  const formData = new FormData(event.target);
  if (file.value) {
    formData.append('profile_photo', file.value);  // Access file directly
  }

  try {
    const response = await fetch('http://localhost:3001/auth/register', {
      method: 'POST',
      body: formData
    });

    if (!response.ok) {
      Swal.fire({
        icon: 'error',
        title: 'Registration Failed',
        text: `Failed with status: ${response.status}`
      });
      return;
    }
    Swal.fire({
      icon: 'success',
      title: 'Success',
      text: 'Registration successful!'
    });
    router.push('/login');
  } catch (error) {
    Swal.fire({
      icon: 'error',
      title: 'Error',
      text: 'Registration failed: ' + error.message
    });
  }
}




</script>

<template>
  <navbar />
  <div class="container d-flex justify-content-center align-items-center p-2">
    <h1>Register</h1>
  </div>
  <div class="container d-flex justify-content-center align-items-center ">
    <div class="row">
      <div class="card mt-2 mb-5">
        <div class="register-form p-2">
          <form class="pt-4" @submit.prevent="register">
            <div class="form-group mb-2 p-2">
              <label for="username">Username</label>
              <input type="text" class="form-control" id="username" name="username" placeholder="Enter username" required>
            </div>
            <div class="form-group mb-2 p-2">
              <label for="password">Password</label>
              <input type="password" class="form-control" id="password" name="password" placeholder="Enter password" required>
            </div>
            <div class="form-group mb-2 p-2">
              <label for="email">Email</label>
              <input type="email" class="form-control" id="email" name="email" placeholder="Enter email" required>
            </div>
            <div class="form-group mb-2 p-2">
              <label for="firstname">First Name</label>
              <input type="text" class="form-control" id="firstname" name="firstname" placeholder="Enter first name" required>
            </div>
            <div class="form-group mb-2 p-2">
              <label for="lastname">Last Name</label>
              <input type="text" class="form-control" id="lastname" name="lastname" placeholder="Enter last name" required>
            </div>
            <div class="form-group mb-2 p-2">
              <label for="location">Location</label>
              <input type="text" class="form-control" id="location" name="location" placeholder="Enter location" required>
            </div>
            <div class="form-group mb-2 p-2">
              <label for="biography">Biography</label>
              <textarea class="form-control" id="biography" name="biography" rows="3" placeholder="Write a short biography" required></textarea>
            </div>
            <div class="form-group mb-2 p-2">
              <label for="profile_photo">Profile Photo</label>
              <input type="file" class="form-control" id="profile_photo" name="profile_photo" @change="handleFileChange" >
            </div>
            <button type="submit" class="btn btn-success mt-4 p-2">Register</button>
          </form>
        </div>
     </div>
    </div>
  </div>
</template>

<style scoped>
.card {
  width: 100%;
  max-width: 800px;
}

.btn-success {
  background-color: #7ed321;
  border-color: #7ed321;
  width:18rem;
}

</style>
