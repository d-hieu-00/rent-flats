import { createRouter, createWebHistory } from 'vue-router';

export const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            name: 'home',
            component: () => import('@/views/homeView.vue')
        },
        {
            path: '/login',
            name: 'login',
            component: () => import('@/views/loginView.vue')
        },
        {
            path: '/signup',
            name: 'signup',
            component: () => import('@/views/signupView.vue')
        },
        {
            path: '/profile',
            name: 'profile',
            component: () => import('@/views/profileView.vue')
        },
        {
            path: '/about',
            name: 'about',
            component: () => import('@/views/aboutView.vue'),
            meta: {
                requiredLoggedIn: true,
                requiredAdmin: true,
            },
        },
        {
            path: '/admin/login',
            name: 'adminLogin',
            component: () => import('@/views/admin/loginView.vue')
        },
    ]
});
