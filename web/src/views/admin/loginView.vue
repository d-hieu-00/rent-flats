<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <h2>Welcome to ADMIN login page</h2>
  <p>This is the login form</p>

  <form @submit.prevent="handleSubmit">
    <div class="form-group">
      <label for="username">Username</label>
      <input type="text" id="username" v-model="username" required>
    </div>
    <div class="form-group">
      <label for="password">Password</label>
      <input type="password" id="password" v-model="password" required>
    </div>
    <button type="submit">Log In</button>
    <div v-if="errorMessage" class="error-message">
      {{ errorMessage }}
    </div>
  </form>
</template>

<style scoped>
/* .login-form {
} */

.error-message {
  color: red;
}
</style>

<script lang="ts">
export default {
  name: 'LoginForm',
  data() {
    return {
      username: '',
      password: '',
      errorMessage: '',
    };
  },
  methods: {
    handleSubmit() {
      // Simulate login logic (replace with actual authentication)
      if (this.username === 'user' && this.password === 'password') {
        // Success!
        this.$emit('loginSuccess');
      } else {
        // Failure
        this.errorMessage = 'Invalid username or password';
      }
    },
  },
};
</script>
