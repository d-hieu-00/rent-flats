import { useStore } from 'vuex'
import { router } from './router';

router.beforeEach((to, from, next) => {
    const store = useStore();
    const isAdmin = store.getters["auth/isAdmin"];
    const isLoggedIn = store.getters["auth/isLoggedIn"];

    if (to.matched.some(record => record.meta.requiredLoggedIn) && !isLoggedIn) {
        next({ name: 'login' });
    } else if (to.matched.some(record => record.meta.requiredAdmin) && !isAdmin) {
        next({ name: 'adminLogin' });
    } else {
        store.dispatch("nav/routedTo", to.path);
        next();
    }
});

export { router }
