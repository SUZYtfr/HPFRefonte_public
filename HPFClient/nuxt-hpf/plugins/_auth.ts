/*
La prise en charge de @nuxtjs/auth est toujours en travaux.
En attendant, plutôt que de passer sur un autre module, voici
un "faux auth"
*/

class mockAuth {
    public loggedIn = false
    public user = null

    public setUser = () => {}
    public logout = () => {}
    public loginWith = () => {}
}

export default defineNuxtPlugin((nuxtApp) => {
    nuxtApp.vueApp.config.globalProperties.$auth = new mockAuth()
})