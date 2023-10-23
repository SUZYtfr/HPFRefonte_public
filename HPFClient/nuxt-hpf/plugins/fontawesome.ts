/* eslint vue/component-definition-name-casing: 0 */
import Buefy from 'buefy'
import 'buefy/dist/buefy.css'
import { library, config } from "@fortawesome/fontawesome-svg-core";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { fas } from "@fortawesome/free-solid-svg-icons";
import { fab } from "@fortawesome/free-brands-svg-icons";

export default defineNuxtPlugin((nuxtApp) => {
    // This is important, we are going to let Nuxt.js worry about the CSS
    config.autoAddCss = false;

    // You can add your icons directly in this plugin. See other examples for how you
    // can add other styles or just individual icons.
    library.add(fas);
    library.add(fab);

    // Register the component globally
    nuxtApp.vueApp.component("font-awesome-icon", FontAwesomeIcon);
    // Buefy-Next, remplace l'ancien module "nuxt/buefy"
    nuxtApp.vueApp.use(Buefy, {
        defaultIconComponent: "font-awesome-icon",
        defaultIconPack: "fas"
    })
})
