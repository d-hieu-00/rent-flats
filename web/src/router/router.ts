import { createRouter, createWebHistory } from 'vue-router';

export const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            name: 'home',
            component: () => import('../views/HomeView.vue')
        },
        {
            path: '/login',
            name: 'login',
            component: () => import('../views/loginView.vue')
        },
        {
            path: '/admin/login',
            name: 'adminLogin',
            component: () => import('../views/admin/loginView.vue')
        },
        {
            path: '/about',
            name: 'about',
            component: () => import('../views/AboutView.vue'),
            meta: {
                requiredLoggedIn: true,
                requiredAdmin: true,
            },
        }
    ]
});
