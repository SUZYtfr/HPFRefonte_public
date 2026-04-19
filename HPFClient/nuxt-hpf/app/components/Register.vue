<template>
  <BModal v-model="ModalStatesModule.registerModalActive" scroll="clip">
    <form ref="html-signup-form" class="fullheight">
      <div id="registerCard" class="modal-card mx-5 fullheight">
        <header class="modal-card-head">
          <p class="modal-card-title">Inscription</p>
          <button type="button" class="delete" @click="ModalStatesModule.setRegisterModalActive(false)"></button>
        </header>
        <section class="modal-card-body pt-2 fixed-height-card">
          <p>
            En application du Règlement Général sur la Protection des Données n°2016/679 du 27 avril 2016 (RGPD), vous
            bénéficiez d’un droit d’accès et de rectification aux informations qui vous concernent.
          </p>
          <p>
            Vous trouverez plus d'informations dans le
            <a><u>règlement du site</u></a
            >, que vous consentez avoir lu par cette inscription.
          </p>
          <p>
            <strong>A l'intention des mineurs :</strong>
            avant toute nouvelle inscription d'un mineur sur le site, le responsable légal de celui-ci doit être informé
            qu'HPF contient des fanfictions à caractère érotique et sont invités à prendre connaissance des règles du
            site avant de donner ou non leur accord.
          </p>
          <hr class="mt-2 mb-4" />
          <div class="columns">
            <!-- Nom, Mail, Site web, Mot de passe, Avatar -->
            <div class="column is-6">
              <div class="columns">
                <div class="column is-6">
                  <BField label="Nom d'auteur *" label-position="on-border" custom-class="has-text-primary">
                    <BInput
                      v-model="signupForm.username"
                      type="text"
                      placeholder="Votre pseudo"
                      required
                      pattern="^[A-Za-z0-9_\- ]{3,30}$"
                      validation-message="Veuillez saisir un nom d'utilisateur compris entre 3 et 30 caractères"
                    />
                  </BField>
                </div>
                <div class="column is-6">
                  <BField label="Nom réel" label-position="on-border" custom-class="has-text-primary">
                    <BInput
                      v-model="signupForm.profile.realname"
                      type="text"
                      placeholder="Votre nom réel"
                      pattern="^[A-Za-zÀ-ÖØ-öø-ÿ\- ]{3,30}$"
                    />
                  </BField>
                </div>
              </div>
              <BField class="mb-5" label="Adresse mail *" label-position="on-border" custom-class="has-text-primary">
                <BInput
                  v-model="signupForm.email"
                  type="email"
                  placeholder="Votre adresse mail"
                  required
                  validation-message="L'adresse mail est invalide"
                />
              </BField>

              <BField class="mb-5" label="Site web" label-position="on-border" custom-class="has-text-primary">
                <BInput v-model="signupForm.profile.website" type="url" placeholder="Votre site web" />
              </BField>
              <BField class="mb-5" label="Mot de passe *" label-position="on-border" custom-class="has-text-primary">
                <BInput
                  v-model="signupForm.password"
                  password-reveal
                  placeholder="Votre mot de passe"
                  type="password"
                  required
                  :pattern="regexPasswordPattern"
                  validation-message="Une majuscule, une miniscule, un chiffre, un caractère spécial, minimum 8 caractères requis, maximum 32."
                />
              </BField>

              <BField
                class="mb-5"
                label="Confirmer le mot de passe *"
                label-position="on-border"
                custom-class="has-text-primary"
              >
                <BInput
                  v-model="checkPass"
                  password-reveal
                  placeholder="Votre mot de passe"
                  type="password"
                  required
                  :pattern="rgxConfirmPassword"
                  validation-message="Les mots de passe doivent correspondre."
                />
              </BField>
              <BField label="Avatar" label-position="on-border" custom-class="has-text-primary">
                <BUpload v-model="uploadedFile" drag-drop type="is-primary" expanded>
                  <section class="section p-4">
                    <div class="content has-text-centered">
                      <div v-if="uploadedFile">
                        <!-- <img
                          id="previewPicture"
                          :src="signupForm.profile.profile_picture"
                          :alt="uploadedFile.name"
                          width="256"
                          height="256"
                        /> -->
                        <button class="delete is-small" type="button" @click="deleteDropFile()"></button>
                      </div>
                      <div v-else>
                        <p>
                          <BIcon icon="upload" size="is-large" />
                        </p>
                        <p>Cliquez ou faites glisser votre avatar ici</p>
                      </div>
                    </div>
                  </section>
                </BUpload>
              </BField>
            </div>
            <!-- Bio -->
            <div class="column is-6">
              <RichtextEditor
                :config="tiptapConfig"
                @change="(value: { content: string }) => (signupForm.profile.bio = value.content)"
              />
            </div>
          </div>
        </section>
        <footer class="modal-card-foot">
          <BButton
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
  </BModal>
</template>

<script setup lang="ts">
import { BButton, BField, BUpload, BInput, BModal } from "buefy";
// import { regexPasswordPattern, OpenToast } from "@/utils/formHelper";
import type { UserRegisterData } from "@/types/users";
// import type { TipTapEditorConfig } from "@/types/tiptap";

const regexPasswordPattern =
  /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&_\-^~#\|`\\\/\[\]\(\)\{\}=+*\.;:§<>²°])[A-Za-z\d@$!%*?&_\-^~#\|`\\\/\[\]\(\)\{\}=+*\.;:§<>²°]{8,32}$/;

const ModalStatesModule = useModalsStateStore();

// Le formulaire en tant qu'élément HTML
const htmlContactForm = useTemplateRef("html-signup-form");

// L'objet lié des informations du formulaire
const signupForm = reactive<UserRegisterData>({
  email: "",
  password: "",
  username: "",
  profile: {
    realname: "",
    bio: "",
    website: "",
    profilePicture: null,
  },
});

// Si les informations changent, utiliser la validation de l'élément HTML
const formIsValid = ref(false);
watch(signupForm, () => {
  formIsValid.value = Boolean(htmlContactForm.value?.checkValidity());
});

const tiptapConfig = reactive({
  showFooter: false,
  placeholder: "Votre description",
  readOnly: false,
  fixedHeight: true,
  defaultValue: "",
  canQuote: false,
  quoteLimit: 0,
  fontSize: 100,
  height: 150,
  oneLineToolbar: false,
  canUseImage: true,
});

const loading = false;
const checkPass = ref("");
function checkAndSubmitForm(): void {}
function deleteDropFile(): void {}
const uploadedFile = ref<File | null | undefined>(null);
const rgxConfirmPassword = "";

// // #region Computed
// get rgxConfirmPassword(): string {
//   return (
//     "^" +
//     this.signupForm.password.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") +
//     "$"
//   );
// }

// // #region Watchers
// @Watch("signupForm", { deep: true })
// @Watch("checkPass", { deep: true })
// public onFormChanged(): void {
//   this.formIsValid = this.form.checkValidity();
// }

// @Watch("uploadedFile", { deep: true })
// public onChanged(): void {
//   const reader = new FileReader();
//   reader.onloadend = e => (this.signupForm.profile.profile_picture = reader.result);
//   if (this.uploadedFile != null) reader.readAsDataURL(this.uploadedFile);
//   // reader.readAsDataURL(
//   //   this.uploadedFile != null ? this.uploadedFile : new Blob()
//   // );
//   console.log(this.uploadedFile);
//   console.log(reader);
//   console.log(this.signupForm.profile.profile_picture);
// }
// // #endregion

// // #region Methods
// // Vérifier le formulaire avant l'envoi
// public checkAndSubmitForm(): void {
//   if (this.form.checkValidity()) this.signup();
// }

// // Supprimer l'avatar uploadé
// public deleteDropFile(): void {
//   this.uploadedFile = null;
//   this.signupForm.profile.profile_picture = "";
// }

// // Envoyer le formulaire
// private async signup(): Promise<void> {
//   try {
//     this.loading = true;
//     const data = await signup(this.signupForm);
//     OpenToast(
//       "Inscription réussie",
//       "is-primary",
//       5000,
//       false,
//       true,
//       "is-bottom"
//     );
//   } catch (exception) {
//     OpenToast("Erreur", "is-danger", 5000, false, true, "is-bottom");
//   } finally {
//     this.loading = false;
//   }
// }
</script>

<style lang="scss" scoped>
@use "~/assets/scss/custom.scss";

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
