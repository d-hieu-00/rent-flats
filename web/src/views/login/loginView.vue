<template>
    <div id="login">
        <div class="card shadow" style="width: 30%;">
            <img class="card-img-top img-head" src="@/assets/head.png" alt="Rent House">
            <form class="card-body" @submit.prevent="doLogin">
                <div class="input-group has-validation mb-3">
                    <span class="first-span input-group-text border-tr-0 border-br-0 border-tl-3 border-bl-3">Email</span>
                    <input class="form-control border-tl-0 border-bl-0 border-tr-3 border-br-3" :class="usernameErr ? 'is-invalid' : ''" type="text" v-model="username" placeholder="abc@company.org" autocomplete="off">
                </div>
                <div class="input-group has-validation mb-3">
                    <span class="first-span input-group-text border-tr-0 border-br-0 border-tl-3 border-bl-3">Password</span>
                    <input class="form-control border-tl-0 border-bl-0"
                        :class="[
                            passwordErr ? 'is-invalid' : '',
                            passwordIsInputed() ? 'border-tr-0 border-br-0' : 'border-tr-3 border-br-3'
                        ]"
                        v-model="password" :type="passwordFieldType()" placeholder="*******">
                    <span class="input-group-text border-tl-0 border-bl-0 border-tr-3 border-br-3" :hidden="!passwordIsInputed()">
                        <i @click="hidePassword = !hidePassword">
                            <font-awesome-icon :icon="passwordFieldIcon()" />
                        </i>
                    </span>
                </div>
                <div class="mb-3">
                    <input class="btn btn-success mb-3 w-100" type="submit" :value="loginText" style="border-radius: 3px;" :disabled="loginText !== 'Log In'">
                    <div class="form-text">By logging in you agree accept our <a href="#">Privacy Policy</a> and <a href="#">Terms of Use</a>.</div>
                </div>
            </form>
        </div>
    </div>
</template>

<style scoped>
    @import url("./loginView.scss");
</style>

<script setup lang="ts">
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { toast } from 'vue3-toastify';
import { useStore } from 'vuex';
import { userApis } from '@/apis/user';
import { SEESION_ID } from '@/config';
import { getCookie, fetchRespError, isRespError } from '@/utils'

// Define variables
var username = "";
var password = "";
var hidePassword = true;
var usernameErr = false;
var passwordErr = false;
var errorMessage = "";
var loginText = "Log In";
const store = useStore();

const passwordFieldIcon = () => { return hidePassword ? "fa-solid fa-eye" : "fa-solid fa-eye-slash"; };
const passwordFieldType = () => { return hidePassword ? "password" : "text"; };
const passwordIsInputed = () => { return password !== "" };
const validate = () => {
    usernameErr = false;
    passwordErr = false;
    errorMessage = "";

    if (username === "" || username.length < 4) {
        usernameErr = true;
        errorMessage = "Email must not empty and length must be greater than 4";
    }

    if (password === "" || password.length < 4) {
        passwordErr = true;
        errorMessage = "Password must not empty and length must be greater than 4";
    }

    return true && !usernameErr && !passwordErr;
};

const doLogin = () => {
    if (!validate()) {
        toast.warn(errorMessage);
        return;
    }

    loginText = "Loading...";
    userApis.login(username, password)
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
            // TODO: route to home
        }, async (respErr) => {
            const data = await respErr.json();
            throw fetchRespError(data);
        })
        .catch(err => {
            errorMessage = err;
            toast.error(err);
            store.dispatch("auth/delUserInfo");
        })
        .finally(() => {
            loginText = "Log In";
        })
};
</script>
