import '@/assets/main.css';
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.min.js'
import 'vue3-toastify/dist/index.css';

import { createApp } from 'vue'
import { store } from './store'
import { router } from './router';
import app from './app.vue'
import Vue3Toastify, { type ToastContainerOptions } from 'vue3-toastify';

import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faSpinner,
         faEye,
         faEyeSlash,
         faLocationDot,
         faPerson,
         faSackDollar,
         faPhone,
         faEnvelope,
       } from '@fortawesome/free-solid-svg-icons'
import { faFacebookF,
         faTwitter,
         faYoutube,
         faLinkedinIn,
         faGooglePlusG,
       } from '@fortawesome/free-brands-svg-icons'

// Fortawesome icon
library.add(
    faSpinner,
    faEye,
    faEyeSlash,
    faLocationDot,
    faPerson,
    faSackDollar,
    faPhone,
    faEnvelope,
    faFacebookF,
    faTwitter,
    faYoutube,
    faLinkedinIn,
    faGooglePlusG
);

createApp(app)
    .component('font-awesome-icon', FontAwesomeIcon)
    .use(store)
    .use(router)
    .use(Vue3Toastify, {
            autoClose: 2000,
            position: "bottom-left",
            pauseOnHover: false,
            hideProgressBar: true,
            clearOnUrlChange: false,
            transition: "flip"
        } as ToastContainerOptions)
    .mount('#app');
