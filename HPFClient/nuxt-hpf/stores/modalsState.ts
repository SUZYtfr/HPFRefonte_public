// Store pour gérer l'état des modals globales de l'application
export const useModalsStateStore = defineStore("modalsState", () => {
    
    //#region State
    const loginModalActive = ref(false);
    const registerModalActive = ref(false);
    const contactModalActive = ref(false);
    //#endregion

    //#region Action
    function setLoginModalActive(value: boolean): void {
        loginModalActive.value = value;
    }

    function setRegisterModalActive(value: boolean): void {
        registerModalActive.value = value;
    }

    function setContactModalActive(value: boolean): void {
        contactModalActive.value = value;
    }
    //#endregion
  
    return { loginModalActive, registerModalActive, contactModalActive, setLoginModalActive, setRegisterModalActive, setContactModalActive };
  });