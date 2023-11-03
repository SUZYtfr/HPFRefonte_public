<template>
  <b-modal v-model="modalActive" width="300px" scroll="keep">
    <form ref="htmlLoginForm">
      <div class="modal-card" style="width: auto">
        <header class="modal-card-head">
          <p class="modal-card-title">
            Connexion
          </p>
          <button type="button" class="delete" @click="modalActive = false" />
        </header>
        <section class="modal-card-body">
          <b-field label="Identifiant">
            <b-input
              v-model="loginForm.username"
              type="text"
              placeholder="Votre pseudo"
              required
            />
          </b-field>
          <b-field label="Mot de passe">
            <b-input
              v-model="loginForm.password"
              type="password"
              password-reveal
              placeholder="Votre mot de passe"
              required
            />
          </b-field>
          <b-checkbox>Se souvenir de moi</b-checkbox>
        </section>
        <footer class="modal-card-foot">
          <b-button
            :disabled="!formIsValid"
            :expanded="true"
            label="Se connecter"
            type="is-primary"
            :loading="loading"
            @click="checkAndSubmitForm()"
          />
        </footer>
      </div>
    </form>
  </b-modal>
</template>

<script setup lang="ts">
import { VForm } from "@/utils/formHelper";
import { UserLoginData } from "@/types/users";

// TODO - Repasser sur un store ?
const modalActive: Ref<boolean> = useState("loginModalActive")

const loginForm = reactive<UserLoginData>({
  username: "",
  password: ""
})

const formIsValid = ref<boolean>(false)

// NOTE https://stackoverflow.com/questions/72139221/how-to-use-template-refs-in-nuxt-3
const htmlLoginForm = ref<HTMLInputElement | null>(null)
const form = computed<VForm>(() => htmlLoginForm.value as VForm)
watch(loginForm, () => { formIsValid.value = form.value.checkValidity() })

// FIXME - adapter quand le module d'authentification est implémenté
// Vérifier le formulaire avant l'envoi
function checkAndSubmitForm(): void {
  if (form.value.checkValidity()) {/*login()*/}
}
let loading: boolean = false;
// Envoyer le formulaire
// private async login(): Promise<void> {
//   this.loading = true;
//   try {
//       await this.$auth.loginWith("cookie", { data: this.loginForm });
//   } catch (error) {
//     if (process.client) {
//       this.$buefy.snackbar.open({
//         duration: 5000,
//         message: "Une erreur s'est produite lors de la tentative de connexion",
//         type: "is-danger",
//         position: "is-bottom-right",
//         actionText: null,
//         pauseOnHover: true,
//         queue: true
//       });
//     } else {
//       console.log(error);
//     }
//   } finally {
//     this.loading = false;
//   }
// }
</script>

<style lang="scss" scoped>
@import "~/assets/scss/custom.scss";
</style>
