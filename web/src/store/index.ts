import { createStore } from 'vuex'
import auth from './modules/auth'
import nav from './modules/nav'

function storeInitialized(store: any) {
    store.dispatch("auth/fetchUser");
    store.dispatch("auth/startInterval");
}

export const store = createStore({
    modules: {
        auth,
        nav,
    },
    plugins: [
        storeInitialized
    ]
})

export {}
