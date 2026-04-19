<template>
  <BModal v-model="useModalsStateStore().registerModalActive">
    <div class="modal-card">
      <template v-if="step == 'account'">
        <header class="modal-card-head">
          <p class="modal-card-title">Inscription</p>
          <button type="button" class="delete" @click="useModalsStateStore().registerModalActive = false"></button>
        </header>
        <section class="modal-card-body">
          <form ref="html-signup-form">
            <BField label="Nom de plume *" label-position="on-border" custom-class="has-text-primary">
              <BInput
                v-model="signupForm.username"
                type="text"
                placeholder="Votre pseudo"
                required
                pattern="^[A-Za-z0-9_\-]{3,30}$"
                validation-message="Le pseudonyme doit contenir entre 3 et 20 caractères, sans espace ni caractères spéciaux."
              />
            </BField>
            <BField label="Adresse mail *" label-position="on-border" custom-class="has-text-primary">
              <BInput
                v-model="signupForm.email"
                type="email"
                placeholder="Votre adresse mail"
                required
                validation-message="L'adresse mail est invalide"
              />
            </BField>
            <BField class="mb-5" label="Mot de passe *" label-position="on-border" custom-class="has-text-primary">
              <BInput
                v-model="signupForm.password"
                password-reveal
                placeholder="Votre mot de passe"
                type="password"
                required
                pattern="^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,24}$"
                validation-message="Le mot de passe doit contenir entre 8 et 24 caractères, dont au moins une majuscule, une minuscule, un chiffre et un caractère spécial parmi @$!%*?&."
              />
            </BField>
            <BField
              class="mb-5"
              label="Confirmer le mot de passe *"
              label-position="on-border"
              custom-class="has-text-primary"
            >
              <BInput
                v-model="signupForm.confirm"
                password-reveal
                placeholder="Votre mot de passe"
                type="password"
                required
                :pattern="regexConfirmPassword"
                validation-message="Les mots de passe doivent correspondre."
              />
            </BField>
          </form>
        </section>
        <footer class="modal-card-foot buttons is-right">
          <BButton label="Suivant" type="is-primary" :disabled="!signupFormValid" @click="step = 'rules'" />
        </footer>
      </template>
      <template v-else-if="step == 'rules'">
        <header class="modal-card-head">
          <p class="modal-card-title">Règlement</p>
          <button type="button" class="delete" @click="useModalsStateStore().registerModalActive = false"></button>
        </header>
        <section class="modal-card-body">
          <div class="block">
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
              avant toute nouvelle inscription d'un mineur sur le site, le responsable légal de celui-ci doit être
              informé qu'HPF contient des fanfictions à caractère érotique et sont invités à prendre connaissance des
              règles du site avant de donner ou non leur accord.
            </p>
          </div>
          <BField>
            <BCheckbox v-model="rulesAccepted">Lu et accepté</BCheckbox>
          </BField>
        </section>
        <footer class="modal-card-foot buttons is-right">
          <BButton
            :disabled="!rulesAccepted"
            label="S'inscrire"
            type="is-success"
            :loading="loading"
            @click="handleSignUpButton()"
          />
        </footer>
      </template>
      <template v-else-if="step == 'profile'">
        <header class="modal-card-head">
          <p class="modal-card-title">Profil</p>
          <button type="button" class="delete" @click="useModalsStateStore().registerModalActive = false"></button>
        </header>
        <section class="modal-card-body">
          <form ref="html-profile-form">
            <div class="columns">
              <div class="column">
                <div class="block">Ces informations sont optionnelles et publiques</div>
                <BField label="Prénom" label-position="on-border" custom-class="has-text-primary">
                  <BInput
                    v-model="profileForm.realname"
                    type="text"
                    placeholder="Votre prénom"
                    pattern="^[A-Za-zÀ-ÖØ-öø-ÿ\- ]{0,24}$"
                  />
                </BField>
                <BField class="mb-5" label="Site web" label-position="on-border" custom-class="has-text-primary">
                  <BInput v-model="profileForm.website" type="url" placeholder="Votre site web" />
                </BField>
              </div>
              <div class="column">
                <BField label="Avatar" label-position="on-border" custom-class="has-text-primary">
                  <BUpload v-model="profileForm.profilePicture" drag-drop type="is-primary" expanded>
                    <section class="section p-4">
                      <div class="content has-text-centered">
                        <div v-if="profileForm.profilePicture">
                          <img
                            :src="base64ProfilePicture as string"
                            :alt="profileForm.profilePicture.name"
                            width="150"
                            height="150"
                          />
                          <button
                            class="delete is-small"
                            type="button"
                            @click="profileForm.profilePicture = undefined"
                          ></button>
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
            </div>
            <RichtextEditor :config="tiptapConfig" :text="profileForm.bio" />
          </form>
        </section>
        <footer class="modal-card-foot buttons is-right">
          <BButton
            label="Plus tard"
            type="is-primary is-light"
            @click="useModalsStateStore().registerModalActive = false"
          />
          <BButton
            :disabled="!profileFormValid"
            label="Enregistrer"
            type="is-success"
            @click="handleProfileSaveButtonClick"
          />
        </footer>
      </template>
    </div>
  </BModal>
</template>

<script setup lang="ts">
import { BButton, BField, BUpload, BInput, BModal, BCheckbox, BIcon } from "buefy";
import { snackbar } from "#imports";
import type { TipTapEditorConfig } from "~/types/other";

const { signIn } = useCustomAuth();

// Les formulaires en tant qu'élément HTML
const htmlSignupForm = useTemplateRef<HTMLFormElement>("html-signup-form");
const htmlProfileForm = useTemplateRef<HTMLFormElement>("html-profile-form");

// L'objet lié des informations du formulaire
const signupForm = reactive<{
  username?: string;
  email?: string;
  password?: string;
  confirm?: string;
}>({});
const profileForm = reactive<{
  realname?: string;
  bio?: string;
  website?: string;
  profilePicture?: File;
}>({});

const toBase64 = (file: File): Promise<string | ArrayBuffer | null> =>
  new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => resolve(reader.result);
    reader.onerror = reject;
  });

const base64ProfilePicture = ref<string | ArrayBuffer | null>(null);
watch(
  () => profileForm.profilePicture,
  async () => {
    if (profileForm.profilePicture) {
      base64ProfilePicture.value = await toBase64(profileForm.profilePicture);
    }
  },
);

const regexConfirmPassword = computed<string>(() => {
  return "^" + (signupForm.password || "").replace(/[.*+?^${}()|[\]\\]/g, "\\$&") + "$";
});

const step = ref<"account" | "rules" | "profile">("account");
const rulesAccepted = ref<boolean>(false);

// Si les informations changent, utiliser la validation de l'élément HTML
const signupFormValid = ref(false);
watch(signupForm, () => {
  signupFormValid.value = Boolean(htmlSignupForm.value!.checkValidity());
});
const profileFormValid = ref(false);
watch(profileForm, () => {
  profileFormValid.value = Boolean(htmlProfileForm.value!.checkValidity());
});

const tiptapConfig = reactive<TipTapEditorConfig>({
  showFooter: false,
  placeholder: "Votre bio",
  fixedHeight: true,
  height: 150,
  oneLineToolbar: true,
  canUseImage: true,
});

const loading = ref(false);
async function handleSignUpButton(): Promise<void> {
  loading.value = true;
  if (!signupFormValid.value) return;
  try {
    await GqlCreateAccount({
      accountData: {
        username: signupForm.username!,
        email: signupForm.email!,
        password: signupForm.password!,
      },
    });
    signIn({ username: signupForm.username!, password: signupForm.password! });
  } catch {
    snackbar.open({
      message: "Erreur",
      type: "is-danger",
      duration: 5000,
      indefinite: false,
      pauseOnHover: true,
      position: "is-bottom",
    });
  } finally {
    loading.value = false;
  }
  snackbar.open({
    message: "Inscription réussie",
    type: "is-primary",
    duration: 5000,
    indefinite: false,
    pauseOnHover: true,
    position: "is-bottom",
  });
  step.value = "profile";
}

async function handleProfileSaveButtonClick(): Promise<void> {
  loading.value = true;
  if (!profileFormValid.value) return;
  try {
    await GqlUpdateProfile({
      profileData: {
        realname: profileForm.realname,
        website: profileForm.website,
        bio: profileForm.bio,
      },
    });
  } catch {
    snackbar.open({
      message: "Erreur",
      type: "is-danger",
      duration: 5000,
      indefinite: false,
      pauseOnHover: true,
      position: "is-bottom",
    });
  } finally {
    loading.value = false;
  }
  snackbar.open({
    message: "Votre profil a été mis à jour",
    type: "is-primary",
    duration: 5000,
    indefinite: false,
    pauseOnHover: true,
    position: "is-bottom",
  });
  useModalsStateStore().registerModalActive = false;
}
</script>
