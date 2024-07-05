<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { toast } from 'vue3-toastify';
import { useStore } from 'vuex';
</script>

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

<script lang="ts">
import { userApis } from '../../apis/user';
import { getCookie, fetchRespError, isRespError } from '@/utils'
import { SEESION_ID } from '../../config';

export default {
    name: 'LoginForm',
    data() {
        return {
            username: "",
            password: "",
            passwordFieldIcon: function () { return this.hidePassword ? "fa-solid fa-eye" : "fa-solid fa-eye-slash"; },
            passwordFieldType: function () { return this.hidePassword ? "password" : "text"; },
            passwordIsInputed: function () { return this.password !== "" },
            hidePassword: true,
            usernameErr: false,
            passwordErr: false,
            errorMessage: "",
            loginText: "Log In",
            store: useStore(),
        };
    },
    methods: {
        validate() {
            this.usernameErr = false;
            this.passwordErr = false;
            this.errorMessage = "";

            if (this.username === "" || this.username.length < 4) {
                this.usernameErr = true;
                this.errorMessage = "Email must not empty and length must be greater than 4";
            }

            if (this.password === "" || this.password.length < 4) {
                this.passwordErr = true;
                this.errorMessage = "Password must not empty and length must be greater than 4";
            }

            return true && !this.usernameErr && !this.passwordErr;
        },
        doLogin() {
            if (!this.validate()) {
                toast.warn(this.errorMessage);
                return;
            }

            this.loginText = "Loading...";
            userApis.login(this.username, this.password)
                .then(async (resp) => {
                    const data = await resp.json();
                    if (isRespError(data)) {
                        throw fetchRespError(data);
                    }
                    if (!getCookie(SEESION_ID)) {
                        throw "Not found cookie";
                    }
                    toast.success("Log In successfully");
                    this.store.dispatch("auth/fetchUser");
                    // TODO: route to home
                }, async (respErr) => {
                    const data = await respErr.json();
                    throw fetchRespError(data);
                })
                .catch(err => {
                    this.errorMessage = err;
                    toast.error(err);
                    this.store.dispatch("auth/delUserInfo");
                })
                .finally(() => {
                    this.loginText = "Log In";
                })
        },
    },
};
</script>
