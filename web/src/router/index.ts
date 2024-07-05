import { useStore } from 'vuex'
import { router } from './router';

router.beforeEach((to, from, next) => {
    const store = useStore();
    const isAdmin = store.getters.isAdmin;
    const isLoggedIn = store.getters.isLoggedIn;
    if (to.matched.some(record => record.meta.requiredLoggedIn) && !isLoggedIn) {
        next({ name: 'login' });
    } else if (to.matched.some(record => record.meta.requiredAdmin) && !isAdmin) {
        next({ name: 'adminLogin' });
    } else {
        next();
    }
});

export default router
