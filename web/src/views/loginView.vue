<template>
  <div id="login">
    <div class="card shadow" style="width: 40%;">
      <div class="card-header pt-3 pb-3" id="header">
        <p class="ps-4 m-0 fs-2 fw-semibold">Log In Form</p>
      </div>
      <form class="card-body ms-4 me-4 mt-3" @submit.prevent="doLogin">
        <p class="mt-3 mb-1 fw-bold">Welcome to Rent Houses.</p>
        <p>Please input your email and password to log in.</p>
        <div class="input-group has-validation mb-3 mt-4">
          <span class="first-span input-group-text border-tr-0 border-br-0 border-tl-3 border-bl-3">Email</span>
          <input class="form-control border-tl-0 border-bl-0 border-tr-3 border-br-3"
            :class="usernameErr ? 'is-invalid' : ''" type="text" v-model="username" placeholder="abc@company.org"
            autocomplete="off">
        </div>
        <div class="input-group has-validation mb-1">
          <span class="first-span input-group-text border-tr-0 border-br-0 border-tl-3 border-bl-3">Password</span>
          <input class="form-control border-tl-0 border-bl-0" :class="[
              passwordErr ? 'is-invalid' : '',
              passwordIsInputed() ? 'border-tr-0 border-br-0' : 'border-tr-3 border-br-3'
            ]" v-model="password" :type="passwordFieldType()" placeholder="*******">
          <span class="input-group-text border-tl-0 border-bl-0 border-tr-3 border-br-3" :hidden="!passwordIsInputed()">
            <i @click="hidePassword = !hidePassword">
              <font-awesome-icon :icon="passwordFieldIcon()" />
            </i>
          </span>
        </div>
        <a :class="customLinkClass" href="#">Forgot your password?</a>
        <input class="btn btn-success w-100 border-radius-3 mt-3" type="submit" :value="loginText" :disabled="loginText !== 'Log In'">
        <p class="mt-2 mb-2">Not a member? <RouterLink to="/signup" :class="customLinkClass">Sign up now</RouterLink>.</p>
      </form>
    </div>
  </div>
</template>

<style scoped>
@import url("./_scss/loginView.scss");
</style>

<script setup lang="ts">
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { toast } from 'vue3-toastify';
import { ref, onMounted } from 'vue';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';
import { userApis } from '@/apis/user';
import { SEESION_ID } from '@/config';
import { getCookie, fetchRespError, isRespError } from '@/utils'
import { RouterLink } from 'vue-router'

// Define variables
var username = ref("");
var password = ref("");
var hidePassword = ref(true);
var usernameErr = ref(false);
var passwordErr = ref(false);
var errorMessage = ref("");
var loginText = ref("Log In");
const store = useStore();
const router = useRouter();
const customLinkClass = "link-primary link-offset-2 link-underline-opacity-0 link-underline-opacity-100-hover";

const passwordFieldIcon = () => { return hidePassword.value ? "fa-solid fa-eye" : "fa-solid fa-eye-slash"; };
const passwordFieldType = () => { return hidePassword.value ? "password" : "text"; };
const passwordIsInputed = () => { return password.value !== "" };
const validate = () => {
  usernameErr.value = false;
  passwordErr.value = false;
  errorMessage.value = "";

  if (username.value === "" || username.value.length < 4) {
    usernameErr.value = true;
    errorMessage.value = "Email must not empty and length must be greater than 4";
  }

  if (password.value === "" || password.value.length < 4) {
    passwordErr.value = true;
    errorMessage.value = "Password must not empty and length must be greater than 4";
  }

  return true && !usernameErr.value && !passwordErr.value;
};

onMounted(() => {
  const token = getCookie(SEESION_ID);
  if (token) {
    routeToHome();
  }
});

const routeToHome = () => {
  router.push("/");
};

const doLogin = () => {
  if (!validate()) {
    toast.warn(errorMessage.value, { autoClose: 3000 });
    return;
  }

  loginText.value = "Loading...";
  userApis.login(username.value, password.value)
    .then(async (resp) => {
      const data = await resp.json();
      if (isRespError(data)) {
        throw fetchRespError(data);
      }
      if (!getCookie(SEESION_ID)) {
        throw "Not found cookie";
      }
      toast.success("Log In successfully");
      store.dispatch("auth/fetchUser");
      routeToHome();
    }, async (respErr) => {
      const data = await respErr.json();
      throw fetchRespError(data);
    })
    .catch(err => {
      errorMessage.value = err;
      toast.error(err, { autoClose: 3000 });
      store.dispatch("auth/delUserInfo");
    })
    .finally(() => {
      loginText.value = "Log In";
    })
};
</script>
