<template>
  <div class="row m-5" id="profile">
    <div class="col d-flex flex-column align-items-end">
      <img src="@/assets/avatar.png" alt="User Avatar" class="avatar rounded border shadow" width="250" height="250">
      <a :class="CUSTOM_LINK_CLASS + ' link-primary'" href="#">Change password</a>
      <a :class="CUSTOM_LINK_CLASS + ' link-danger'" href="#">Delete account</a>
    </div>
    <div class="col card shadow">
      <a  data-bs-toggle="tooltip" data-bs-placement="top" data-bs-title="Tooltip on top">heheheheeheh</a>
      <p class="fs-5 p-4 pb-0 mb-0">Hi <b>{{ user.username }}</b>,</p>
      <div class="card-body mt-0 pt-0 ms-3 me-3">
        <div class="input-group has-validation mb-3 mt-4">
          <span class="first-span input-group-text border-r-0 border-l-3">Email</span>
          <input class="form-control border-l-0 border-r-3" disabled type="text" :value="user.email">
        </div>
        <div class="input-group has-validation mb-3 mt-4">
          <span class="first-span input-group-text border-r-0 border-l-3">Username</span>
          <input class="form-control border-l-0 border-r-3" disabled type="text" :value="user.username">
        </div>
        <div class="input-group has-validation mb-3 mt-4">
          <span class="first-span input-group-text border-r-0 border-l-3">Address</span>
          <input class="form-control border-l-0 border-r-3" type="text" :value="user.address">
        </div>
        <div class="input-group has-validation mb-3 mt-4">
          <span class="first-span input-group-text border-r-0 border-l-3">Phone</span>
          <input class="form-control border-l-0 border-r-3" type="text" :value="user.phone">
        </div>
        <div class="input-group has-validation mb-3 mt-4">
          <!-- TODO: dropdown -->
          <span class="first-span input-group-text border-r-0 border-l-3">Gender</span>
          <input class="form-control border-l-0 border-r-3" type="text" :value="user.gender">
        </div>
        <button class="btn btn-success mt-1 mb-2">Update Information</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
@import url("./_scss/profileView.scss");
</style>

<script setup>
import { ref, onMounted, onUnmounted } from "vue";
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';
import { SEESION_ID, CUSTOM_LINK_CLASS } from "@/config";
import { onEvent, offEvent, getCookie, isRespError, fetchRespError, isUndefined } from '@/utils';

var user = ref({ });
const store = useStore();
const router = useRouter();

onMounted(() => {
  onEvent("user-info-change", updateUserInfo);
  updateUserInfo();
  // Check if user is logged in and redirect to login page if not.
  const token = getCookie(SEESION_ID);
  if (isUndefined(token)) {
    routeToLogin();
  }
});

onUnmounted(() => {
  offEvent("user-info-change", updateUserInfo)
});

const routeToLogin = () => {
  router.push("/login");
};

const updateUserInfo = () => {
  const userInfo = store.getters["auth/otherInfo"];
  user.value.username = store.getters["auth/username"];
  user.value.email = userInfo["email"];
  user.value.address = userInfo.additional?.address;
  user.value.phone = userInfo.additional?.phone;
  user.value.gender = userInfo.additional?.gender;
};

</script>
