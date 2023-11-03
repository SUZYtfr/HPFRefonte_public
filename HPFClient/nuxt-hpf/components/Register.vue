<template>
  <b-modal v-model="modalActive" scroll="clip">
    <form ref="htmlSignupForm" class="fullheight">
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
                      v-model="signupForm.profile.realname"
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
                  v-model="signupForm.profile.website"
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
                  validation-message="Une majuscule, une minuscule, un chiffre, un caractère spécial, minimum 8 caractères requis, maximum 32."
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
                          :src="signupForm.profile.profile_picture"
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
                :config="tiptapConfig"
                @change="(value) => (signupForm.profile.bio = value.content)"
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

<script setup lang="ts">
import { signup as sendSignup } from "@/api/users";
import { VForm, regexPasswordPattern as rgxPasswordPattern, OpenToast } from "@/utils/formHelper";
import TipTapEditor from "@/components/TipTapEditor.vue";
import { UserRegisterData } from "@/types/users";
import { TipTapEditorConfig } from "@/types/tiptap";

interface RegisterProps {
  active?: boolean
}
const { active } = defineProps<RegisterProps>()

// TODO - Repasser sur un store ?
const modalActive = useState<boolean>("registerModalActive")

const uploadedFile = ref<Blob | null>(null)
// private previewAvatar!: Blob;
const checkPass = ref<string>("")

const signupForm = reactive<UserRegisterData>({
  email: "",
  password: "",
  username: "",
  profile: {
    realname: "",
    bio: "",
    website: "",
    profile_picture: null
  }
})

const formIsValid = ref<boolean>(false)

const tiptapConfig: TipTapEditorConfig = {
  showFooter: false,
  placeholder: "Votre description",
  readOnly: false,
  fixedHeight: true
};

const rgxConfirmPassword = computed<string>(() => {
  return (
    "^" +
    signupForm.password.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") +
    "$"
  );
})

const regexPasswordPattern = computed<string>(() => {
  return rgxPasswordPattern.source;
})

// NOTE https://stackoverflow.com/questions/72139221/how-to-use-template-refs-in-nuxt-3
const htmlSignupForm = ref<HTMLInputElement | null>(null)
const form = computed<VForm>(() => htmlSignupForm.value as VForm)
watch([signupForm, checkPass], () => {
  formIsValid.value = form.value.checkValidity()
})

watch(uploadedFile, () => {
  const reader = new FileReader();
  reader.onloadend = e => (signupForm.profile.profile_picture = reader.result);
  if (uploadedFile.value != null) reader.readAsDataURL(uploadedFile.value);
  // reader.readAsDataURL(
  //   this.uploadedFile != null ? this.uploadedFile : new Blob()
  // );
  console.log(uploadedFile);
  console.log(reader);
  console.log(signupForm.profile.profile_picture);
})

// Supprimer l'avatar uploadé
function deleteDropFile(): void {
  uploadedFile.value = null;
  signupForm.profile.profile_picture = "";
}

// Vérifier le formulaire avant l'envoi
function checkAndSubmitForm(): void {
  if (form.value.checkValidity()) signup()
}

const loading = ref<boolean>(false)
const { status, execute } = await sendSignup(signupForm)
watch(status, async (value: string) => {
  loading.value = false
  if (value === "success") {
    OpenToast("Inscription réussie", "is-primary", 5000, false, true, "is-bottom");
  } else if (value === "error") {
    OpenToast("Erreur", "is-danger", 5000, false, true, "is-bottom");
  } else if (value === "pending") {
    loading.value = true
  }
})

// Envoyer le formulaire
async function signup(): Promise<void> {
  execute()
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
