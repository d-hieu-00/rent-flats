<template>
  <nav class="navbar navbar-expand-lg">
    <div class="navbar-left">
      <RouterLink to="/" class="logo"> <img src="@/assets/head.png" width="50" height="50"> </RouterLink>
    </div>
    <RouterLink to="/" class="m-0 fw-semibold text-warning link-underline link-underline-opacity-0">
      Rent Smarter, Live Better
    </RouterLink>
    <ul class="nav navbar-right">
      <li class="nav-item" v-for="nav in navItems">
        <RouterLink v-if="nav.path !== '#' && nav.display" class="link-offset-2 nav-link"
          :class="[nav.class, nav.active ? activeNavClass : '']" :to="nav.path">{{ nav.txt }}
        </RouterLink>
        <a href="#" v-if="nav.path === '#' && nav.display" class="link-offset-2"
          :class="nav.class" :to="nav.path" @click="nav.click">{{ nav.txt }}
        </a>
      </li>
    </ul>
  </nav>
</template>

<style scoped>
@import url("../_scss/navigation.scss");
</style>

<script setup lang="ts">
import { RouterLink } from 'vue-router'
import { useStore } from 'vuex'
import { toast } from 'vue3-toastify'
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { onMounted, onUnmounted } from 'vue';
import { onEvent, offEvent, isRespError, fetchRespError, isUndefined } from '@/utils'
import { userApis } from '@/apis/user';

var navItems = ref([
  {
    val: "feedback",
    txt: "Give Feedback",
    class: "shadow btn btn-warning",
    path: "#",
    click: () => {},
    active: false,
    roles: { admin: false, user: true, public: false },
    display: false
  },
  {
    val: "rented",
    txt: "Rented Houses",
    class: "",
    path: "/rented",
    click: () => {},
    active: false,
    roles: { admin: false, user: true, public: false },
    display: false
  },
  {
    val: "bill",
    txt: "Bills",
    class:"",
    path: "/bill",
    click: () => {},
    active: false,
    roles: { admin: false, user: true, public: false },
    display: false
  },
  {
    val: "profile",
    txt: "My Profile",
    class: "",
    path: "/profile",
    click: () => {},
    active: false,
    roles: { admin: false, user: true, public: false },
    display: false
  },
  {
    val: "login",
    txt: "Login",
    class: "",
    path: "/login",
    click: () => {},
    active: false,
    roles: { admin: false, user: false, public: true },
    display: false
  },
  {
    val: "signup",
    txt: "Sign Up",
    class: "shadow fw-bold btn bg-success",
    path: "/signup",
    click: () => {},
    active: false,
    roles: { admin: false, user: false, public: true },
    display: false
  },
  {
    val: "logout",
    txt: "Log out",
    class: "shadow fw-bold btn btn-light text-dark bg-light",
    path: "#",
    click: () => logout(),
    active: false,
    roles: { admin: false, user: true, public: false },
    display: false
  },
]);

const store = useStore();
const router = useRouter();
const activeNavClass = "fw-bold text-decoration-underline"
var isLoggedIn = ref(store.getters["auth/isLoggedIn"]);
var isAdmin = ref(store.getters["auth/isAdmin"]);
var activeNavigation = ref(store.getters["nav/activeNavigation"]);

onMounted(() => {
  onEvent("user-info-change", updateUserInfo)
  onEvent("update-navigation", updateNavigation)
  updateNavItems();
});

onUnmounted(() => {
  offEvent('user-info-change', updateUserInfo);
  offEvent("update-navigation", updateNavigation)
});

const updateNavigation = (_: any | undefined) => {
  activeNavigation.value = store.getters["nav/activeNavigation"];
  updateNavItems();
}

const updateUserInfo = (_: any | undefined) => {
  isLoggedIn.value = store.getters["auth/isLoggedIn"];
  isAdmin.value = store.getters["auth/isAdmin"];
  updateNavItems();
}

const updateNavItems = () => {
  navItems.value.forEach((nav: any) => {
    nav.active = nav.val === activeNavigation.value;
    nav.display = navOkToDisplay(nav);
  });
}

const navOkToDisplay = (nav: any) => {
  let ok = false;
  ok = ok || (nav.roles.admin === true &&  nav.roles.admin === isAdmin.value);
  ok = ok || (nav.roles.user === true &&  nav.roles.user === isLoggedIn.value);
  ok = ok || (nav.roles.public === true && isLoggedIn.value === false);
  return ok;
}

const logout = () => {
  userApis.logout()
    .then(async (resp: Response) => {
      const data = await resp.json();
      if (isRespError(data)) {
        throw fetchRespError(data);
      }
      toast.success("Logged out successfully");
      store.dispatch("auth/delUserInfo");
      router.push("/login");
    }, async (respErr: Response) => {
      throw fetchRespError(await respErr.json());
    }).catch(err => {
      toast.error(err, { autoClose: 3000 });
    });
}
</script>
