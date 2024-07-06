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

<script setup lang="ts">
import 'bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.min.js';
import Navigation from '@/components/navigation/navigation.vue'
import { RouterView } from 'vue-router'

</script>
