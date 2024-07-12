<template>
  <div id="signup">
    <div class="card shadow" style="width: 55%;">
      <div class="card-header pt-3 pb-3" id="header">
        <p class="ps-4 m-0 fs-2 fw-semibold">Sign Up Form</p>
      </div>
      <form class="card-body ms-4 me-4 mt-3" @submit.prevent="doSignup">
        <div class="input-group has-validation mb-3">
          <span class="first-span input-group-text border-tr-0 border-br-0 border-tl-3 border-bl-3">Name</span>
          <input class="form-control border-tl-0 border-bl-0 border-tr-3 border-br-3"
            :class="nameErr ? 'is-invalid' : ''" type="text" v-model="name" placeholder="John Doe"
            autocomplete="off">
        </div>
        <div class="input-group has-validation mb-3">
          <span class="first-span input-group-text border-tr-0 border-br-0 border-tl-3 border-bl-3">Email</span>
          <input class="form-control border-tl-0 border-bl-0 border-tr-3 border-br-3"
            :class="emailErr ? 'is-invalid' : ''" type="text" v-model="email" placeholder="abc@company.org"
            autocomplete="off">
        </div>
        <div class="input-group has-validation mb-3">
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
        <div class="input-group has-validation mb-3">
          <span class="first-span input-group-text border-tr-0 border-br-0 border-tl-3 border-bl-3">Confirm Password</span>
          <input class="form-control border-tl-0 border-bl-0" :class="[
              cPasswordErr ? 'is-invalid' : '',
              cPasswordIsInputed() ? 'border-tr-0 border-br-0' : 'border-tr-3 border-br-3'
            ]" v-model="cPassword" :type="cPasswordFieldType()" placeholder="*******">
          <span class="input-group-text border-tl-0 border-bl-0 border-tr-3 border-br-3" :hidden="!cPasswordIsInputed()">
            <i @click="cHidePassword = !cHidePassword">
              <font-awesome-icon :icon="cPasswordFieldIcon()" />
            </i>
          </span>
        </div>
        <div class="mb-3">
          <input class="btn btn-success mb-2 w-100" type="submit" :value="signupText" style="border-radius: 3px;"
            :disabled="signupText !== 'Sign Up'">
          <div class="form-text">*By signing up you agree accept our <a href="#">Privacy Policy</a> and <a href="#">Terms of Use</a>.</div>
        </div>
      </form>
    </div>
  </div>
</template>

<style scoped>
@import url("./_scss/signupView.scss");
</style>

<script setup lang="ts">
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { toast } from 'vue3-toastify';
import { useRouter } from 'vue-router';
import { ref } from 'vue';
import { userApis } from '@/apis/user';
import { isRespError, fetchRespError } from '@/utils';

// Define variables
var name = ref("");
var email = ref("");
var password = ref("");
var hidePassword = ref(true);
var cPassword = ref("");
var cHidePassword = ref(true);
var nameErr = ref(false);
var emailErr = ref(false);
var passwordErr = ref(false);
var cPasswordErr = ref(false);
var errorMessage = ref("");
var signupText = ref("Sign Up");
const router = useRouter();

const passwordFieldIcon = () => { return hidePassword.value ? "fa-solid fa-eye" : "fa-solid fa-eye-slash"; };
const passwordFieldType = () => { return hidePassword.value ? "password" : "text"; };
const passwordIsInputed = () => { return password.value !== "" };
const cPasswordFieldIcon = () => { return cHidePassword.value ? "fa-solid fa-eye" : "fa-solid fa-eye-slash"; };
const cPasswordFieldType = () => { return cHidePassword.value ? "password" : "text"; };
const cPasswordIsInputed = () => { return cPassword.value !== "" };
const validate = () => {
  nameErr.value = false;
  emailErr.value = false;
  passwordErr.value = false;
  cPasswordErr.value = false;
  errorMessage.value = "";

  if (name.value === "" || name.value.length < 4) {
    nameErr.value = true;
    errorMessage.value = "Name must not empty and length must be greater than 4";
  }

  if (email.value === "" || email.value.length < 4) {
    emailErr.value = true;
    errorMessage.value = "Email must not empty and length must be greater than 4";
  }

  if (!/^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/.test(email.value)) {
    emailErr.value = true;
    errorMessage.value = "Invalid email format";
  }

  if (password.value === "" || password.value.length < 4) {
    passwordErr.value = true;
    errorMessage.value = "Password must not empty and length must be greater than 4";
  }

  if (cPassword.value === "" || cPassword.value.length < 4) {
    cPasswordErr.value = true;
    errorMessage.value = "Confirm Password must not empty and length must be greater than 4";
  }

  if (cPassword.value !== password.value) {
    cPasswordErr.value = true;
    errorMessage.value = "Confirm Password does not match";
  }

  return true && !nameErr.value && !emailErr.value && !passwordErr.value && !cPasswordErr.value;
};

const doSignup = () => {
  if (!validate()) {
    console.log("Form invalid", errorMessage);
    toast.warn(errorMessage.value, { autoClose: 3000 });
    return;
  }

  signupText.value = "Loading...";
  const data = {
    username: name.value, email: email.value, password: password.value
  };

  userApis.signup(data)
    .then(async (resp) => {
      const data = await resp.json();
      if (isRespError(data)) {
        throw fetchRespError(data);
      }
      toast.success("Sign Up successfully");
      routeToLogin();
    }, async (respErr) => {
      const data = await respErr.json();
      throw fetchRespError(data);
    })
    .catch(err => {
      errorMessage.value = err;
      toast.error(err, { autoClose: 3000 });
    })
    .finally(() => {
      signupText.value = "Sign Up";
    })
};

const routeToLogin = () => {
  router.push("/login");
};
</script>