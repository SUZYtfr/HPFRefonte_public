import { defineStore } from "pinia";

export const ModalsStates = defineStore("ModalsStatesModule", () => {
    const loginModalActive = ref(false);
    const registerModalActive = ref(false);
    const contactModalActive = ref(false);
    
    function setLoginModalActive(isActive: boolean) { loginModalActive.value = isActive }
    function setRegisterModalActive(isActive: boolean) { registerModalActive.value = isActive }
    function setContactModalActive(isActive: boolean) { contactModalActive.value = isActive }
  
    return {
        loginModalActive,
        registerModalActive,
        contactModalActive,
        setLoginModalActive,
        setRegisterModalActive,
        setContactModalActive,
    }
});
  