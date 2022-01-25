<template>
  <b-modal v-model="modalActive" width="600px" scroll="keep">
    <form ref="contactForm">
      <div class="modal-card" style="width: auto">
        <header class="modal-card-head">
          <p class="modal-card-title">Nous contacter</p>
          <button type="button" class="delete" @click="modalActive = false" />
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
            ></b-input>
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
              <option value="4">Autre raison</option>
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
            ></b-input>
          </b-field>
        </section>
        <footer class="modal-card-foot">
          <b-button
            :disabled="!formIsValid"
            :expanded="true"
            label="Envoyer"
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
import { contact } from "@/api/other";
import { VForm, OpenToast } from "@/utils/formHelper";
import { ContactFormData } from "@/types/other";

@Component({
  name: "NousContacter",
})
export default class extends Vue {
  //#region Props
  @Prop() private active!: boolean;
  //#endregion

  //#region Data
  private contactForm: ContactFormData = {
    email: "",
    subject_id: "",
    content: "",
  };

  private formIsValid: boolean = false;

  private loading: boolean = false;
  //#endregion

  //#region Computed
  get modalActive() {
    return this.active;
  }

  set modalActive(value) {
    this.$emit("change", value);
  }

  get form(): VForm {
    return this.$refs["contactForm"] as VForm;
  }
  //#endregion

  //#region Watchers
  @Watch("contactForm", { deep: true })
  private onFormChanged() {
    this.formIsValid = this.form.checkValidity();
  }
  //#endregion

  //#region Methods
  // Vérifier le formulaire avant l'envoi
  private checkAndSubmitForm() {
    if (this.form.checkValidity()) this.contact();
  }

  // Envoyer le formulaire
  private async contact() {
    this.loading = true;
    try {
      const { data } = await contact(this.contactForm);
      OpenToast("Envoi réussi", "is-primary", 5000, false, true, "is-bottom");
    } catch (exception) {
      console.log(exception);
      OpenToast("Erreur", "is-danger", 5000, false, true, "is-bottom");
    } finally {
      this.loading = false;
    }
  }
  //#endregion
}
</script>

<style lang="scss">
@import "~/assets/scss/custom.scss";
.contact-textarea {
  resize: none !important;
}
</style>