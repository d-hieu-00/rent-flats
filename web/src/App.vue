<template>
  <Navigation />
  <div class="main">
    <div><RouterView class="router-view"/></div>
    <Footer />
</div>
</template>

<style scoped>
  .router-view {
    margin: 0 20rem;
  }
  .main {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    min-height: 100%;
  }
</style>

<script setup lang="ts">
import Navigation from '@/components/navigation/navigation.vue'
import Footer from '@/components/footer/footer.vue'
import { RouterView } from 'vue-router'
</script>
