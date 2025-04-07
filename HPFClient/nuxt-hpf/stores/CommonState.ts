export const CommonState = defineStore("CommonState", () => {
    const wasRefreshed = ref<boolean>(false);

    function setWasRefreshed(wRefreshed: boolean): void {
        wasRefreshed.value = wRefreshed; 
    }

    return {
        wasRefreshed,
        setWasRefreshed
    }
});
