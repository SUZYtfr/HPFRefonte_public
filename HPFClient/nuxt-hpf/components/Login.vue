<template>
  <b-modal v-model="modalActive" width="300px" scroll="keep">
    <form ref="loginForm">
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

<script lang="ts">
import { Component, Vue, Watch } from "nuxt-property-decorator";
import { getModule } from "vuex-module-decorators";
import ModalsStates from "~/store/modules/ModalsStates";
import { VForm, OpenToast } from "@/utils/formHelper";
import { UserLoginData } from "@/types/users";

@Component({
  name: "Connexion"
})
export default class extends Vue {
  // #region Data
  public loginForm: UserLoginData = {
    username: "",
    password: ""
  };

  public formIsValid: boolean = false;

  public loading: boolean = false;
  // #endregion

  // #region Computed
  get ModalsStatesModule(): ModalsStates {
    return getModule(ModalsStates, this.$store);
  }

  get modalActive(): boolean {
    return this.ModalsStatesModule.loginModalActive;
  }

  set modalActive(value) {
    this.ModalsStatesModule.setLoginModalActive(value);
  }

  get form(): VForm {
    return this.$refs.loginForm as VForm;
  }

  // #endregion

  // #region Watchers
  @Watch("loginForm", { deep: true })
  private onFormChanged(): void {
    this.formIsValid = this.form.checkValidity();
  }
  // #endregion

  // #region Methods
  // Vérifier le formulaire avant l'envoi
  public checkAndSubmitForm():void {
    if (this.form.checkValidity()) this.login();
  }

  // Envoyer le formulaire
  private async login(): Promise<void> {
    this.loading = true;
    try {
      await this.$auth.loginWith("cookie", { data: this.loginForm });
    } catch (error) {
      if (process.client) {
        this.$buefy.snackbar.open({
          duration: 5000,
          message: "Une erreur s'est produite lors de la tentative de connexion",
          type: "is-danger",
          position: "is-bottom-right",
          actionText: null,
          pauseOnHover: true,
          queue: true
        });
      } else {
        console.log(error);
      }
    } finally {
      this.loading = false;
    }
  }
  // #endregion
}
</script>

<style lang="scss" scoped>
@import "~/assets/scss/custom.scss";
</style>
