<template>
  <b-modal v-model="modalActive" width="600px" scroll="keep">
    <form ref="htmlContactForm">
      <div class="modal-card" style="width: auto">
        <header class="modal-card-head">
          <p class="modal-card-title">
            Nous contacter
          </p>
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
            :loading="loading"
            @click="checkAndSubmitForm()"
          />
        </footer>
      </div>
    </form>
  </b-modal>
</template>

<script setup lang="ts">
import { contact as sendContact } from "@/api/other";
import { VForm, OpenToast } from "@/utils/formHelper";
import { ContactFormData } from "@/types/other";

interface ContactProps {
  active?: boolean
}
const { active } = defineProps<ContactProps>()

// TODO - Repasser sur un store ?
const modalActive = useState<boolean>("contactModalActive")

const contactForm = reactive<ContactFormData>({
  email: "",
  subject_id: "",
  content: ""
})

const formIsValid = ref<boolean>(false)

// NOTE https://stackoverflow.com/questions/72139221/how-to-use-template-refs-in-nuxt-3
const htmlContactForm = ref<HTMLInputElement | null>(null)
const form = computed<VForm>(() => htmlContactForm.value as VForm)
watch(contactForm, () => { formIsValid.value = form.value.checkValidity() })

const loading = ref<boolean>(false)
const { status, execute } = await sendContact(contactForm)
watch(status, async (value: string) => {
  loading.value = false
  if (value === "success") {
    OpenToast("Envoi réussi", "is-primary", 5000, false, true, "is-bottom");
  } else if (value === "error") {
    OpenToast("Erreur", "is-danger", 5000, false, true, "is-bottom");
  } else if (value === "pending") {
    loading.value = true
  }
})

// Vérifier le formulaire avant l'envoi
function checkAndSubmitForm(): void {
  if (form.value.checkValidity()) contact()
}

// Envoyer le formulaire
async function contact(): Promise<void> {
  execute()
}
</script>

<style lang="scss">
@import "~/assets/scss/custom.scss";
.contact-textarea {
  resize: none !important;
}
</style>
