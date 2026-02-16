// mime le fonctionnement du middleware fourni par sidebase/nuxt-auth
// idéalement, à remplacer

export default defineNuxtRouteMiddleware((to, from) => {
    const { data, token, isAuthenticated, isStaff } = useCustomAuth();
    if (to.meta.auth && !isAuthenticated.value) {
        // Page auth
        return navigateTo("/");
    }
    else if (to.meta.requireStaff && !isStaff.value) {
        // Page admin
        return navigateTo("/");
    }
    return;
});