<script setup>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useStore } from 'vuex';
import Swal from 'sweetalert2';
import navbar from '../components/navbar.vue';

const router = useRouter();
const store = useStore();
const file = ref(null);  // Ensure file is reactive

if (store.state.token) {
  router.push('/');
}

const csrfToken = computed(() => store.state.csrfToken);

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

const register = async (event) => {
  event.preventDefault();

  const formData = new FormData(event.target);
  if (file.value) {
    formData.append('profile_photo', file.value);
  }

  try {
    const response = await fetch('/api/v1/auth/register', {
      method: 'POST',
      headers: {
        'X-CSRFToken': csrfToken.value
      },
      body: formData
    });
    const data = await response.json();

    if (!response.ok) {
      let errorMessage = 'Registration failed.';
      if (data.errors && data.errors.length > 0) {
        errorMessage = data.errors.join(' '); // Join multiple errors into a single message
      }
      Swal.fire({
        icon: 'error',
        title: 'Registration Failed',
        text: errorMessage
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
};
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
              <label for="password">Confirm Password</label>
              <input type="password" class="form-control" id="confirm_password" name="confirm_password" placeholder="Re-enter password" required>
            </div>
            <div class="form-group mb-2 p-2">
              <label for="email">Email</label>
              <input type="email" class="form-control" id="email" name="email" placeholder="Enter email" required>
            </div>
            <div class="form-group mb-2 p-2">
              <label for="firstname">First Name</label>
              <input type="text" class="form-control" id="firstname" name="first_name" placeholder="Enter first name" required>
            </div>
            <div class="form-group mb-2 p-2">
              <label for="lastname">Last Name</label>
              <input type="text" class="form-control" id="lastname" name="last_name" placeholder="Enter last name" required>
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
            <button type="submit" class="btn btn-success mt-4 mb-4 p-2 ">Register</button>
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

.btn-success{
  background-color: #7ed321;
  border-color: #7ed321;
  width:18rem;
}

</style>
