export default defineNuxtPlugin((nuxtApp) => {
    const api = $fetch.create({
        baseURL: "http://localhost:8585/api",
    })

    return {
        provide: {
            api
        }
    }
});