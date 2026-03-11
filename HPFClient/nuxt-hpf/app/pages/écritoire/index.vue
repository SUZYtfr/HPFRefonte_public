<template>
  <div class="container px-5">
    <BSteps ref="steps" v-model="currentStep" :has-navigation="false">
      <BLoading v-model="pending" :is-full-page="false" />
      <!-- Règlement -->
      <BStepItem
        label="Règlement"
        step="rules"
        value="rules"
        icon-pack="fas"
        :icon="rulesAccepted ? 'square-check' : 'square'"
      >
        <LazyManagerRules v-if="currentStep === 'rules'" v-model:rules-accepted="rulesAccepted">
          <div class="p-2 is-flex is-flex-direction-row is-justify-content-space-between">
            <div></div>
            <BButton type="is-danger" @click.prevent="router.back">Annuler</BButton>
            <BButton type="is-primary" :disabled="!rulesAccepted" @click.prevent="() => steps?.next()">{{
              isEditing ? "Modifier la fiction" : "Créer une fiction"
            }}</BButton>
          </div>
        </LazyManagerRules>
      </BStepItem>
      <!-- Modification de fiction -->
      <BStepItem
        label="Fiction"
        step="fiction"
        value="fiction"
        icon-pack="fas"
        :icon="fictionComplete ? 'book' : 'book-open'"
      >
        <LazyManagerFiction
          v-if="currentStep === 'fiction'"
          :fiction="fiction"
          :unsaved-changes="unsavedChanges"
          :is-editing
        >
          <div class="p-2 is-flex is-flex-direction-row is-justify-content-space-between">
            <BButton @click.prevent="() => steps?.prev()">Relire le réglement</BButton>
            <BButton
              v-if="isEditing"
              type="is-danger"
              :disabled="!unsavedChanges"
              @click.prevent="
                () => {
                  fetchFiction(fiction.fanfictionId.toString());
                  unsavedChanges = false;
                }
              "
              >Annuler les modifications</BButton
            >
            <BButton
              type="is-primary"
              :disabled="!(rulesAccepted && fictionComplete)"
              @click.prevent="
                () => {
                  isEditing && unsavedChanges ? updateFiction() : undefined;
                  unsavedChanges = false;
                  steps?.next();
                }
              "
            >
              {{ isEditing && unsavedChanges ? "Enregistrer et aller aux chapitres" : "Aller aux chapitres" }}
            </BButton>
          </div>
        </LazyManagerFiction>
      </BStepItem>
      <!-- Modification de chapitre -->
      <BStepItem
        label="Chapitres"
        step="chapter"
        value="chapter"
        icon-pack="fas"
        :icon="chapterComplete ? 'file-lines' : 'file'"
      >
        <LazyManagerChapter
          v-if="currentStep === 'chapter'"
          v-model:chapter="chapter"
          v-model:active-tab="activeTab"
          v-model:unsaved-changes="unsavedChanges"
          :is-editing
          :chapter-ids="fiction.chapters?.map((c) => c.chapterId.toString()) || []"
        >
          <div class="p-2 is-flex is-flex-direction-row is-justify-content-space-between">
            <BButton @click.prevent="async () => steps?.prev()">Revenir à la fiction</BButton>
            <BButton
              v-if="activeTab"
              type="is-danger"
              :disabled="!unsavedChanges"
              @click.prevent="
                async () => {
                  await fetchChapter(activeTab); // FIXME pourquoi le chapitre ne se remet pas à zéro ?
                  unsavedChanges = false;
                }
              "
              >Annuler les modifications</BButton
            >
            <BField>
              <p class="control">
                <BButton
                  type="is-warning"
                  :disabled="!(rulesAccepted && fictionComplete && chapterComplete && unsavedChanges && !isEditing)"
                  @click.prevent="
                    () => {
                      if (isEditing) {
                        if (activeTab === '') {
                          createChapter(true);
                        } else {
                          updateChapter(true);
                        }
                      } else {
                        postFiction(true);
                      }
                      unsavedChanges = false;
                    }
                  "
                  >Brouillon</BButton
                >
              </p>
              <p class="control">
                <BButton
                  type="is-success"
                  :disabled="!(rulesAccepted && fictionComplete && chapterComplete && unsavedChanges)"
                  @click.prevent="
                    () => {
                      if (isEditing) {
                        if (activeTab === '') {
                          createChapter(false);
                        } else {
                          updateChapter(false);
                        }
                      } else {
                        postFiction(false);
                      }
                      unsavedChanges = false;
                    }
                  "
                >
                  {{ autoPublish ? "Publier" : "Envoyer à la modération" }}</BButton
                >
              </p>
            </BField>
          </div>
        </LazyManagerChapter>
      </BStepItem>
    </BSteps>
  </div>
</template>

<script setup lang="ts">
import { BButton, BSteps, BStepItem, BLoading, BField } from "buefy";
import { RecordStatusEnum } from "~/types/basics";
import { ChapterModel, FanfictionModel } from "~/models";
import { plainToInstance } from "class-transformer";

definePageMeta({
  auth: true,
});

const router = useRouter();
const route = useRoute();
const initialFictionId = (route.query["fiction"] as string) || undefined;
const initialChapterId = (route.query["chapitre"] as string) || undefined;
const { fandoms } = useConfigStore();

// Si une fiction ou un chapitre est indiqué en paramètre, on est en contexte de modification initialement
// Le règlement est considéré comme lu et on arrive directement sur l'étape en question
const isEditing = ref<boolean>(Boolean(initialFictionId || initialChapterId));
const unsavedChanges = ref<boolean>(false);
const steps = useTemplateRef("steps");
const currentStep = ref<"fiction" | "chapter" | "rules">(
  initialFictionId ? "fiction" : initialChapterId ? "chapter" : "rules",
);

const activeTab = ref<string>(initialChapterId || ""); // "" = nouveau chapitre
const autoPublish = true; // TODO depuis profileData ou payloadData

const pending = ref<boolean>(false);

const fiction = ref<FanfictionModel>(
  new FanfictionModel({
    recordStatus: RecordStatusEnum.New,
    fandoms: fandoms!.filter((f) => f.id === route.query["fandom"]),
    characteristics: [],
  }),
);
async function fetchFiction(fictionId: string): Promise<FanfictionModel> {
  pending.value = true;
  try {
    const data = await GqlGetPrivateFiction({ fictionId: fictionId });
    fiction.value = plainToInstance(FanfictionModel, data.fiction);
    return fiction.value;
  } finally {
    pending.value = false;
  }
}

const chapter = ref<ChapterModel>(new ChapterModel({ recordStatus: RecordStatusEnum.New, triggerWarnings: [] }));
async function fetchChapter(chapterId: string): Promise<ChapterModel> {
  pending.value = true;
  try {
    const data = await GqlGetPrivateChapter({ chapterId: chapterId });
    chapter.value = plainToInstance(ChapterModel, data.chapter);
    return chapter.value;
  } finally {
    pending.value = false;
  }
}

// Fetch initial si le contexte initial est la modification
if (initialFictionId) {
  await fetchFiction(initialFictionId);
  activeTab.value = fiction.value.chapters![0]!.chapterId.toString();
  await fetchChapter(activeTab.value);
}
else if (initialChapterId) {
  activeTab.value = initialChapterId;
  await fetchChapter(initialChapterId);
  //@ts-expect-error TODO ChapterData.fiction est un number, mais ChapterType.fiction est un object
  await fetchFiction(chapter.value.fiction!.id.toString());
}

watch(activeTab, async (newValue) => {
  if (newValue) {
    await fetchChapter(newValue);
  } else {
    // si "", c'est l'onglet nouveau chapitre
    chapter.value = new ChapterModel({ recordStatus: RecordStatusEnum.New, triggerWarnings: [] });
  }
});

// TODO méthode sur FanfictionModel, et/ou isComplete sur les composants / formulaires en question
const fictionComplete = computed<boolean>(() => {
  return [
    fiction.value.title,
    fiction.value.summary,
    fiction.value.status,
    fiction.value.rating,
    fiction.value.fandoms?.length,
    fiction.value.characteristics?.filter((c) => c.characteristicTypeId.toString() === "2").length,
  ].every((field) => Boolean(field));
});
const chapterComplete = computed<boolean>(() => {
  return Boolean(chapter.value.title && chapter.value.text);
});
const rulesAccepted = ref<boolean>(isEditing.value);

async function postFiction(isDraft: boolean): Promise<void> {
  pending.value = true;
  await GqlCreateFiction({
    fictionData: {
      title: fiction.value.title,
      summary: fiction.value.summary || "",
      storynote: fiction.value.storynote || "",
      status: Number(fiction.value.status),
      rating: Number(fiction.value.rating!),
      fandoms: {
        set: fiction.value.fandoms!.map((f) => f.id),
      },
      characteristics: {
        set: fiction.value.characteristics!.map((c) => c.characteristicId.toString()),
      },
    },
    firstChapterData: {
      title: chapter.value.title,
      text: chapter.value.text || "",
      startNote: chapter.value.startNote || "",
      endNote: chapter.value.endNote || "",
      triggerWarnings: {
        set: chapter.value.triggerWarnings!.map((tw) => tw.triggerWarningId.toString()),
      },
      isDraft: isDraft,
    },
  })
    .then(async (value) => {
      await fetchFiction(value.createFiction.id);
      await fetchChapter(value.createFiction.chapters.results![0]!.id);
      activeTab.value = value.createFiction.chapters.results![0]!.id;
      isEditing.value = true;
      snackbar.open({
        duration: 5000,
        message: isDraft
          ? "Le brouillon de la fiction a été enregistré"
          : autoPublish
            ? "La fiction a été publiée"
            : "La fiction est en attente de validation",
        type: "is-danger",
        position: "is-bottom-right",
        // actionText: "Revenir aux fictions",
        // onAction: () => navigateTo("/"),
        pauseOnHover: true,
        queue: true,
      });
    })
    .catch(() =>
      snackbar.open({
        duration: 5000,
        message: "Une erreur s'est produite lors de la création de la fiction",
        type: "is-danger",
        position: "is-bottom-right",
        pauseOnHover: true,
        queue: true,
      }),
    )
    .finally(() => (pending.value = false));
}

async function createChapter(isDraft: boolean): Promise<void> {
  pending.value = true;
  await GqlCreateChapter({
    fictionId: fiction.value.fanfictionId.toString(),
    chapterData: {
      title: chapter.value.title,
      text: chapter.value.text || "",
      startNote: chapter.value.startNote || "",
      endNote: chapter.value.endNote || "",
      triggerWarnings: {
        set: chapter.value.triggerWarnings!.map((tw) => tw.triggerWarningId.toString()),
      },
      isDraft: isDraft,
    },
  })
    .then(async (value) => {
      await fetchFiction(fiction.value.fanfictionId.toString()); // màj de la liste des chapitres
      await fetchChapter(value.createChapter.id);
      activeTab.value = value.createChapter.id;
      snackbar.open({
        duration: 5000,
        message: isDraft
          ? "Le brouillon du chapitre a été enregistré"
          : autoPublish
            ? "Le chapitre a été publié"
            : "Le chapitre été envoyé à la modération",
        type: "is-success",
        position: "is-bottom-right",
        // actionText: "Revenir aux fictions",
        // onAction: () => navigateTo("/"),
        pauseOnHover: true,
        queue: true,
      });
    })
    .catch(() =>
      snackbar.open({
        duration: 5000,
        message: "Une erreur s'est produite lors de l'envoi du chapitre",
        type: "is-danger",
        position: "is-bottom-right",
        pauseOnHover: true,
        queue: true,
      }),
    )
    .finally(() => (pending.value = false));
}

async function updateFiction(): Promise<void> {
  pending.value = true;
  await GqlUpdateFiction({
    fictionId: fiction.value.fanfictionId.toString(),
    fictionData: {
      title: fiction.value.title,
      summary: fiction.value.summary || "",
      storynote: fiction.value.storynote,
      status: Number(fiction.value.status),
      rating: Number(fiction.value.rating!),
      fandoms: {
        set: fiction.value.fandoms!.map((f) => f.id),
      },
      characteristics: {
        set: fiction.value.characteristics!.map((c) => c.characteristicId.toString()),
      },
    },
  })
    .then(() =>
      snackbar.open({
        duration: 5000,
        message: "Les changements ont été enregistrés",
        type: "is-success",
        position: "is-bottom-right",
        // actionText: "Revenir aux fictions",
        // onAction: () => navigateTo("/"),
        pauseOnHover: true,
        queue: true,
      }),
    )
    .catch(() =>
      snackbar.open({
        duration: 5000,
        message: "Une erreur s'est produite lors de la modification de la fiction",
        type: "is-danger",
        position: "is-bottom-right",
        pauseOnHover: true,
        queue: true,
      }),
    )
    .finally(() => (pending.value = false));
}

async function updateChapter(isDraft: boolean): Promise<void> {
  pending.value = true;
  await GqlUpdateChapter({
    chapterId: chapter.value.chapterId.toString(),
    chapterData: {
      title: chapter.value.title,
      text: chapter.value.text || "",
      startNote: chapter.value.startNote || "",
      endNote: chapter.value.endNote || "",
      triggerWarnings: {
        set: chapter.value.triggerWarnings!.map((tw) => tw.triggerWarningId.toString()),
      },
      isDraft: isDraft,
    },
  })
    .then(() =>
      snackbar.open({
        duration: 5000,
        message: isDraft
          ? "La nouvelle version du brouillon a été enregistrée"
          : autoPublish
            ? "La nouvelle version du chapitre a été publiée"
            : "La nouvelle version du chapitre été envoyée à la modération",
        type: "is-success",
        position: "is-bottom-right",
        // actionText: "Revenir aux fictions",
        // onAction: () => navigateTo("/"),
        pauseOnHover: true,
        queue: true,
      }),
    )
    .catch(() =>
      snackbar.open({
        duration: 5000,
        message: "Une erreur s'est produite lors de la modification du chapitre",
        type: "is-danger",
        position: "is-bottom-right",
        pauseOnHover: true,
        queue: true,
      }),
    )
    .finally(() => (pending.value = false));
}

useHead({
  title: "HPF - " + (isEditing.value ? "Modification de la fiction" : "Nouvelle fiction"),
});
</script>
