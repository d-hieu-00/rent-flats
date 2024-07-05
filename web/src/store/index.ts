import { createStore, createLogger } from 'vuex'
import auth from './modules/auth'

export default createStore({
  modules: {
    auth,
  },
})
