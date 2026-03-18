<template>
  <div class="container px-5">
    <BSteps ref="steps" v-model="currentStep" :has-navigation="false">
      <BLoading v-model="pending" :is-full-page="false" />
      <!-- Règlement -->
      <BStepItem label="Règlement" step="rules" value="rules" icon-pack="fas" icon="square-check">
        <LazyManagerRules
          v-if="currentStep === 'rules'"
          v-model:rules-accepted="rulesAccepted"
          :is-editing
          @click-cancel="router.back()"
          @click-next="steps?.next()"
        />
      </BStepItem>
      <!-- Modification de fiction -->
      <BStepItem label="Fiction" step="fiction" value="fiction" icon-pack="fas" icon="book-open">
        <LazyManagerFiction
          v-if="currentStep === 'fiction'"
          v-model:fiction="fiction"
          v-model:unsaved-changes="unsavedChanges"
          :is-editing
          @click-previous="steps?.prev()"
          @click-cancel="
            fetchFiction(fiction.fanfictionId.toString());
            unsavedChanges = false;
          "
          @click-next="
            isEditing && unsavedChanges ? updateFiction() : undefined;
            unsavedChanges = false;
            steps?.next();
          "
        />
      </BStepItem>
      <!-- Modification de chapitre -->
      <BStepItem label="Chapitres" step="chapter" value="chapter" icon-pack="fas" icon="file-lines">
        <LazyManagerChapter
          v-if="currentStep === 'chapter'"
          v-model:chapter="chapter"
          v-model:unsaved-changes="unsavedChanges"
          v-model:active-tab="activeTab"
          :is-editing
          :chapter-ids="fiction.chapters?.map((c) => c.chapterId.toString()) || []"
          @click-previous="steps?.prev()"
          @click-cancel="
            async () => {
              await fetchChapter(activeTab); // FIXME pourquoi le chapitre ne se remet pas à zéro ?
              unsavedChanges = false;
            }
          "
          @click-save="
            (isDraft) => {
              if (isEditing) {
                if (activeTab === '') {
                  createChapter(isDraft);
                } else {
                  updateChapter(isDraft);
                }
              } else {
                postFiction(isDraft);
              }
              unsavedChanges = false;
            }
          "
        />
      </BStepItem>
    </BSteps>
  </div>
</template>

<script setup lang="ts">
import { BSteps, BStepItem, BLoading } from "buefy";
import { RecordStatusEnum } from "~/types/basics";
import { ChapterModel, FanfictionModel } from "~/models";
import { plainToInstance } from "class-transformer";

definePageMeta({
  auth: true,
});

const router = useRouter();
const route = useRoute();
const initialFictionId = route.query["fiction"] as string | undefined;
const initialChapterId = route.query["chapitre"] as string | undefined; // chapitre= => "" => nouveau chapitre
const { fandoms } = useConfigStore();

// Si une fiction ou un chapitre est indiqué en paramètre, on est en contexte de modification initialement
// Le règlement est considéré comme lu et on arrive directement sur l'étape en question
const isEditing = ref<boolean>(Boolean(initialFictionId || initialChapterId));
const unsavedChanges = ref<boolean>(false);
const steps = useTemplateRef("steps");
const currentStep = ref<"fiction" | "chapter" | "rules">(
  initialChapterId !== undefined ? "chapter" : initialFictionId ? "fiction" : "rules",
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
  if (initialChapterId === undefined) {
    activeTab.value = fiction.value.chapters![fiction.value.chapters!.length - 1]!.chapterId.toString(); // dernier chapitre par défaut
    await fetchChapter(activeTab.value);
  } else if (initialChapterId !== "") {
    activeTab.value = initialChapterId;
    await fetchChapter(activeTab.value);
  }
}

watch(activeTab, async (newValue) => {
  if (newValue) {
    await fetchChapter(newValue);
  } else {
    // si "", c'est l'onglet nouveau chapitre
    chapter.value = new ChapterModel({ recordStatus: RecordStatusEnum.New, triggerWarnings: [] });
  }
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
