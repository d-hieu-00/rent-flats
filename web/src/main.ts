import '@/assets/main.css';
import 'vue3-toastify/dist/index.css';

import { createApp } from 'vue'
import app from './app.vue'
import store from './store'
import router from './router';
import Vue3Toastify, { type ToastContainerOptions } from 'vue3-toastify';

import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faSpinner } from '@fortawesome/free-solid-svg-icons'
import { faEye } from '@fortawesome/free-solid-svg-icons'
import { faEyeSlash } from '@fortawesome/free-solid-svg-icons'

// Fortawesome icon
library.add(
    faSpinner,
    faEye,
    faEyeSlash
);

createApp(app)
    .component('font-awesome-icon', FontAwesomeIcon)
    .use(store)
    .use(router)
    .use(Vue3Toastify, {
            autoClose: 1500,
            position: "bottom-left",
            pauseOnHover: false,
            hideProgressBar: true
        } as ToastContainerOptions)
    .mount('#app');
