<script setup lang="ts">
import 'bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.min.js';
import Navigation from './components/navigation/navigation.vue'
import { RouterLink, RouterView } from 'vue-router'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
</script>

<template>
    <Navigation />
    <div class="router-view">
        <RouterView />
    </div>
</template>

<style scoped>
    .router-view {
        margin: 0 6rem;
        height: 100%;
    }
</style>

<script lang="ts">
import { ref } from 'vue'
import { toast } from 'vue3-toastify';
import { useStore } from 'vuex'


export default {
    components: {},
    data() {
    },
    methods: {
    },
}
</script>