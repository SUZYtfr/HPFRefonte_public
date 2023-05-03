<template>
  <b-modal v-model="modalActive" scroll="clip">
    <form ref="signupForm" class="fullheight">
      <div id="registerCard" class="modal-card mx-5 fullheight">
        <header class="modal-card-head">
          <p class="modal-card-title">
            Inscription
          </p>
          <button type="button" class="delete" @click="modalActive = false" />
        </header>
        <section class="modal-card-body pt-2 fixed-height-card">
          <p>
            En application du Règlement Général sur la Protection des Données
            n°2016/679 du 27 avril 2016 (RGPD), vous bénéficiez d’un droit
            d’accès et de rectification aux informations qui vous concernent.
          </p>
          <p>
            Vous trouverez plus d'informations dans le
            <a><u>règlement du site</u></a>, que vous consentez avoir lu par cette inscription.
          </p>
          <p>
            <strong>A l'intention des mineurs :</strong>
            avant toute nouvelle inscription d'un mineur sur le site, le
            responsable légal de celui-ci doit être informé qu'HPF contient des
            fanfictions à caractère érotique et sont invités à prendre
            connaissance des règles du site avant de donner ou non leur accord.
          </p>
          <hr class="mt-2 mb-4">
          <div class="columns">
            <!-- Nom, Mail, Site web, Mot de passe, Avatar -->
            <div class="column is-6">
              <div class="columns">
                <div class="column is-6">
                  <b-field
                    label="Nom d'auteur *"
                    label-position="on-border"
                    custom-class="has-text-primary"
                  >
                    <b-input
                      v-model="signupForm.username"
                      type="text"
                      placeholder="Votre pseudo"
                      required
                      pattern="^[A-Za-z0-9_\- ]{3,30}$"
                      validation-message="Veuillez saisir un nom d'utilisateur compris entre 3 et 30 caractères"
                    />
                  </b-field>
                </div>
                <div class="column is-6">
                  <b-field
                    label="Nom réel"
                    label-position="on-border"
                    custom-class="has-text-primary"
                  >
                    <b-input
                      v-model="signupForm.realname"
                      type="text"
                      placeholder="Votre nom réel"
                      pattern="^[A-Za-zÀ-ÖØ-öø-ÿ\- ]{3,30}$"
                    />
                  </b-field>
                </div>
              </div>
              <b-field
                class="mb-5"
                label="Adresse mail *"
                label-position="on-border"
                custom-class="has-text-primary"
              >
                <b-input
                  v-model="signupForm.email"
                  type="email"
                  placeholder="Votre adresse mail"
                  required
                  validation-message="L'adresse mail est invalide"
                />
              </b-field>

              <b-field
                class="mb-5"
                label="Site web"
                label-position="on-border"
                custom-class="has-text-primary"
              >
                <b-input
                  v-model="signupForm.website"
                  type="url"
                  placeholder="Votre site web"
                />
              </b-field>
              <b-field
                class="mb-5"
                label="Mot de passe *"
                label-position="on-border"
                custom-class="has-text-primary"
              >
                <b-input
                  v-model="signupForm.password"
                  password-reveal
                  placeholder="Votre mot de passe"
                  type="password"
                  required
                  :pattern="regexPasswordPattern"
                  validation-message="Une majuscule, une miniscule, un chiffre, un caractère spécial, minimum 8 caractères requis, maximum 32."
                />
              </b-field>

              <b-field
                class="mb-5"
                label="Confirmer le mot de passe *"
                label-position="on-border"
                custom-class="has-text-primary"
              >
                <b-input
                  v-model="checkPass"
                  password-reveal
                  placeholder="Votre mot de passe"
                  type="password"
                  required
                  :pattern="rgxConfirmPassword"
                  validation-message="Les mots de passe doivent correspondre."
                />
              </b-field>
              <b-field
                label="Avatar"
                label-position="on-border"
                custom-class="has-text-primary"
              >
                <b-upload
                  v-model="uploadedFile"
                  drag-drop
                  type="is-primary"
                  expanded
                >
                  <section class="section p-4">
                    <div class="content has-text-centered">
                      <div v-if="uploadedFile">
                        <img
                          id="previewPicture"
                          :src="signupForm.avatar"
                          :alt="uploadedFile.name"
                          width="256"
                          height="256"
                        >
                        <button
                          class="delete is-small"
                          type="button"
                          @click="deleteDropFile()"
                        />
                      </div>
                      <div v-else>
                        <p>
                          <b-icon icon="upload" size="is-large" />
                        </p>
                        <p>Cliquez ou faites glisser votre avatar ici</p>
                      </div>
                    </div>
                  </section>
                </b-upload>
              </b-field>
            </div>
            <!-- Bio -->
            <div class="column is-6">
              <TipTapEditor
                :placeholder="'Votre description'"
                :show-footer="false"
                @change="(value) => (signupForm.bio = value.content)"
              />
            </div>
          </div>
        </section>
        <footer class="modal-card-foot">
          <b-button
            :disabled="!formIsValid"
            :expanded="true"
            label="S'inscrire"
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
import { Component, Vue, Watch, Prop } from "nuxt-property-decorator";
import { ModalsStatesModule } from "@/utils/store-accessor";
import { signup } from "@/api/users";
import { VForm, regexPasswordPattern, OpenToast } from "@/utils/formHelper";
import TipTapEditor from "@/components/TipTapEditor.vue";
import { UserRegisterData } from "@/types/users";

@Component({
  name: "Inscription",
  components: {
    TipTapEditor
  }
})
export default class extends Vue {
  // #region Props
  @Prop() public active!: boolean;
  // #endregion

  // #region Data
  public uploadedFile: Blob | null = null;
  // private previewAvatar!: Blob;
  public checkPass: string = "";

  public signupForm: UserRegisterData = {
    email: "",
    password: "",
    username: "",
    realname: "",
    bio: "",
    website: "",
    avatar: null
  };

  public formIsValid: boolean = false;

  public loading: boolean = false;
  // #endregion

  // #region Computed
  get rgxConfirmPassword(): string {
    return (
      "^" +
      this.signupForm.password.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") +
      "$"
    );
  }

  get regexPasswordPattern(): string {
    return regexPasswordPattern.source;
  }

  get modalActive(): boolean {
    return ModalsStatesModule.registerModalActive;
  }

  set modalActive(value) {
    ModalsStatesModule.setRegisterModalActive(value);
  }

  get form(): VForm {
    return this.$refs.signupForm as VForm;
  }
  // #endregion

  // #region Watchers
  @Watch("signupForm", { deep: true })
  @Watch("checkPass", { deep: true })
  public onFormChanged(): void {
    this.formIsValid = this.form.checkValidity();
  }

  @Watch("uploadedFile", { deep: true })
  public onChanged(): void {
    const reader = new FileReader();
    reader.onloadend = e => (this.signupForm.avatar = reader.result);
    if (this.uploadedFile != null) reader.readAsDataURL(this.uploadedFile);
    // reader.readAsDataURL(
    //   this.uploadedFile != null ? this.uploadedFile : new Blob()
    // );
    console.log(this.uploadedFile);
    console.log(reader);
    console.log(this.signupForm.avatar);
  }
  // #endregion

  // #region Methods
  // Vérifier le formulaire avant l'envoi
  public checkAndSubmitForm(): void {
    if (this.form.checkValidity()) this.signup();
  }

  // Supprimer l'avatar uploadé
  public deleteDropFile(): void {
    this.uploadedFile = null;
    this.signupForm.avatar = "";
  }

  // Envoyer le formulaire
  private async signup(): Promise<void> {
    try {
      this.loading = true;
      const data = await signup(this.signupForm);
      OpenToast(
        "Inscription réussie",
        "is-primary",
        5000,
        false,
        true,
        "is-bottom"
      );
    } catch (exception) {
      OpenToast("Erreur", "is-danger", 5000, false, true, "is-bottom");
    } finally {
      this.loading = false;
    }
  }
  // #endregion
}
</script>

<style lang="scss" scoped>
@import "~/assets/scss/custom.scss";

#registerCard {
  width: auto;
}

#previewPicture {
  max-width: 128px;
  max-height: 128px;
}

.fullheight {
  height: 100%;
  min-height: 250px;
}
</style>
