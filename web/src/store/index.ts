import { createStore } from 'vuex'
import auth from './modules/auth'

function storeInitialized(store: any) {
    store.dispatch("auth/fetchUser");
    store.dispatch("auth/startInterval");
}

export default createStore({
    modules: {
        auth,
    },
    plugins: [
        storeInitialized
    ]
})
