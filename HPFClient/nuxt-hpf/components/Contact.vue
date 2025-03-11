<template>
  <b-modal v-model="ModalStatesModule.contactModalActive" width="600px" scroll="keep">
    <form ref="html-contact-form">
      <div class="modal-card" style="width: auto">
        <header class="modal-card-head">
          <p class="modal-card-title">
            Nous contacter
          </p>
          <button type="button" class="delete" @click="ModalStatesModule.setContactModalActive(false)" />
        </header>
        <section class="modal-card-body pt-2 pb-1">
          <p>
            Pour discuter entre membres de la communauté, trouver de l'aide pour
            une histoire, chercher un relecteur ou simplement passer un bon
            moment entre fans de littérature et de Harry Potter, rendez-vous sur
            le <a href="https://www.herosdepapierfroisse.fr/forum/index.php" target="_blank">forum HPF</a>.
          </p>
          <p class="mb-3">
            Vous rencontrez un problème ? Vous avez une question ? Vous
            souhaitez nous faire part d'une suggestion ? Contactez-nous en
            remplissant le formulaire suivant.
          </p>
          <b-field
            class="mb-4"
            label="Adresse mail"
            label-position="on-border"
            custom-class="has-text-primary"
          >
            <b-input
              v-model="contactForm.email"
              type="email"
              placeholder="Votre adresse mail"
              required
              validation-message="L'adresse mail est invalide"
            />
          </b-field>
          <b-field
            class="mb-4"
            label="Objet"
            label-position="on-border"
            custom-class="has-text-primary"
          >
            <b-select
              v-model="contactForm.subject_id"
              placeholder="Objet du message"
              required
            >
              <option value="0">
                Je rencontre un problème lié à la publication de mes textes, à
                la lecture ou autre.
              </option>
              <option value="1">
                Je rencontre un problème technique (bug du site).
              </option>
              <option value="2">
                Je souhaite contacter l'association qui gère les sites HPF.
              </option>
              <option value="3">
                Je souhaite contacter la maison d'édition Héros de Papier Froissé.
              </option>
              <option value="4">
                Autre raison
              </option>
            </b-select>
          </b-field>
          <b-field
            label="Message"
            label-position="on-border"
            custom-class="has-text-primary"
          >
            <b-input
              v-model="contactForm.content"
              placeholder="Votre message"
              maxlength="1000"
              type="textarea"
              required
              custom-class="contact-textarea"
            />
          </b-field>
        </section>
        <footer class="modal-card-foot">
          <b-button
            :disabled="!formIsValid"
            :expanded="true"
            label="Envoyer"
            type="is-primary"
            :loading="status === 'pending'"
            @click="checkAndSubmitForm()"
          />
        </footer>
      </div>
    </form>
  </b-modal>
</template>

<script setup lang="ts">
import type { ContactFormData } from "@/types/other";

// const { active } = defineProps<{
//   active: boolean;
// }>();

const ModalStatesModule = ModalsStates();

// Le formulaire en tant qu'élément HTML
const htmlContactForm = useTemplateRef("html-contact-form");

// L'objet lié des informations du formulaire
const contactForm = reactive<ContactFormData>({
  email: "",
  subject_id: "",
  content: ""
});

// Si les informations changent, utiliser la validation de l'élément HTML
const formIsValid = ref(false);
watch(contactForm, () => { formIsValid.value = htmlContactForm.value.checkValidity() });

// TODO réparer les toasts !
const { status, execute: submitForm, error } = await useFetch("/api/contact", { immediate: false });
watch(status, () => {
  if (status.value === "success") {
    OpenToast("Envoi réussi", "is-primary", 5000, false, true, "is-bottom");
  }
  else if (status.value === "error") {
    console.log("essai");
    OpenToast("Erreur", "is-danger", 5000, false, true, "is-bottom");
  }
});

// Vérifier le formulaire avant l'envoi
function checkAndSubmitForm(): void {
  if (formIsValid) submitForm();
}
</script>

<style lang="scss">
@use "~/assets/scss/custom.scss";
.contact-textarea {
  resize: none !important;
}
</style>
