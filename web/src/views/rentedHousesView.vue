<template>
  <div id="rented-houses">
    <House class="houses" :search-type="1" ></House>
  </div>
</template>

<style scoped>
@import url("./_scss/rentedHousesView.scss");
</style>

<script setup lang="ts">
import House from '@/components/houses/houses.vue'
import { onMounted } from 'vue'
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';
import { getCookie, isUndefined } from '@/utils'
import { SEESION_ID } from '@/config'

const store = useStore();
const router = useRouter();

const routeToLogin = () => {
  router.push("/login");
};

onMounted(() => {
  // Check if user is logged in and redirect to login page if not.
  const token = getCookie(SEESION_ID);
  if (isUndefined(token)) {
    routeToLogin();
  }
});

</script>
