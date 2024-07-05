<script setup lang="ts">
import { RouterLink } from 'vue-router'
import { useStore } from 'vuex'
import { ref } from 'vue'
import { onMounted, onUnmounted } from 'vue';
import { onEvent, offEvent } from '@/utils'

const store = useStore();
var isLoggedIn = ref(store.state.auth.loggedIn);

onMounted(() => {
    console.log("onMounted", isLoggedIn);
    onEvent('user-info-change', updateUserInfo)
});

onUnmounted(() => {
    offEvent('user-info-change', updateUserInfo);
});

const updateUserInfo = (data: any ) => {
    console.log("udpateUserInfo", data)
    isLoggedIn.value = store.state.auth.loggedIn;
    console.log("udpateUserInfod", isLoggedIn)
}

</script>

<template>
    <nav class="navbar navbar-expand-lg">
        <div class="navbar-left">
            <RouterLink to="/" class="logo"> <img src="@/assets/logo.png" width="100" height="100"> </RouterLink>
            <input type="text" placeholder="Search" class="search-input">
        </div>
        <ul class="nav navbar-right">
            <li class="nav-item"><RouterLink to="/" class="nav-link">Find Houses</RouterLink></li>
            <li v-if="isLoggedIn" class="nav-item"><RouterLink to="/" class="nav-link">Rented Houses</RouterLink></li>
            <li v-if="isLoggedIn" class="nav-item"><RouterLink to="/" class="nav-link">Bills</RouterLink></li>
            <li v-if="isLoggedIn" class="nav-item"><RouterLink to="/login" class="nav-link">Give Feedback</RouterLink></li>
            <li v-if="isLoggedIn" class="nav-item"><RouterLink to="/login" class="nav-link">My Profile</RouterLink></li>
            <li v-if="isLoggedIn" class="nav-item"><RouterLink to="/login" class="nav-link">Log out</RouterLink></li>
            <li v-if="!isLoggedIn" class="nav-item"><RouterLink to="/login" class="nav-link">Log In</RouterLink></li>
            <li v-if="!isLoggedIn" class="nav-item"><RouterLink to="/signup" class="nav-link card shadow bg-success">Sign Up</RouterLink></li>
        </ul>
    </nav>
</template>


<style scoped>
    @import url("./navigation.css");
</style>

<script lang="ts">
import { toast } from 'vue3-toastify';
export default {
    components: {},
    data() {
        return {
            // isLoggedIn: false,
        }
    },
    methods: {
        update() {
            
            // console.log(store.state.auth);
        },
    }
}
</script>
