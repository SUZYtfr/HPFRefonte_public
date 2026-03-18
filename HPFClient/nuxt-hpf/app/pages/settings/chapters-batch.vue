<template>
  <div class="container is-fluid">
    <BTabs v-model="activeTab" type="is-toggle" :animated="false" expanded>
      <BTabItem v-for="tab in tabs" :key="tab.status" :label="tab.label" :value="tab.status.toString()">
        <div class="columns">
          <div class="column is-narrow">
            <div class="card">
              <div class="card-content pl-3 pr-1 py-3">
                <div class="pr-4">
                  <div
                    class="mx-2 mb-1 has-text-weight-semibold is-italic is-size-7 has-text-primary is-flex is-flex-direction-row is-align-content-space-between is-justify-content-space-between"
                  >
                    <span class="mr-1">{{ headerFilterLabel }}</span>
                    <b v-if="(chapters?.length ?? 0) > 0">{{ " (" + chapters?.length.toString() + ")" }}</b>
                  </div>
                  <BInput
                    v-model="chapterFilters.searchTerm"
                    placeholder="Rechercher"
                    type="search"
                    icon="search"
                    class="mb-2"
                  />
                  <!-- Filtres des chapitres à valider -->
                  <div v-if="selectedTab?.status == ChapterValidationStatusEnum.AwaitingValidation">
                    <BField>
                      <BCheckbox v-model="chapterFilters.awaitingDiscussionOnly" size="is-small">
                        Chapitres "à discuter" uniquement
                      </BCheckbox>
                    </BField>
                  </div>
                  <BField>
                    <BCheckbox v-model="chapterFilters.watchedAuthors" size="is-small">
                      Marqués en "à surveiller"
                    </BCheckbox>
                  </BField>
                </div>
                <Simplebar class="custom-scrollbar-bio" data-simplebar-auto-hide="false">
                  <!-- <b-loading v-model="chaptersStatus" :is-full-page="false" /> -->
                  <ChaptersValidation
                    v-for="(chapter, index) in chapters"
                    :key="index"
                    :chapter="chapter"
                    :class="['mb-2', 'mr-4', { 'is-color-even': index % 2 != 0 }, { 'is-color-odd': index % 2 == 0 }]"
                    :is-selected="(selectedChapter?.chapterId ?? 0) == chapter.chapterId"
                    @click="() => onChapterSelected(chapter)"
                  />
                </Simplebar>
              </div>
            </div>
          </div>
          <!-- Contenu central, chapitre sélectionné -->
          <div class="column">
            <div v-if="selectedChapter != null" class="card">
              <div class="card-content pl-3 pr-1 py-3">
                <!-- Titre du chapitre / Auteur de la fiction-->
                <div
                  class="is-flex is-flex-direction-row is-flex-wrap-nowrap is-justify-content-space-between is-align-items-center"
                >
                  <span class="has-text-weight-bold"> {{ selectedChapter.title }} </span>
                  <div class="mr-3 white-space-nowrap">
                    <template
                      v-for="(author, index) in selectedChapter.authors"
                      :key="'author_' + author.userId.toString()"
                    >
                      <template v-if="index > 0"> , </template>
                      <BTooltip
                        v-if="author.watched"
                        label="Auteur à surveiller"
                        :append-to-body="true"
                        position="is-top"
                      >
                        <BIcon icon="warning" type="is-danger" />
                      </BTooltip>
                      <!-- TODO span à reconvertir en NuxtLink -->
                      <span
                        class="is-size-6 has-text-weight-normal"
                        :to="{ name: 'auteurs-id', params: { id: author.userId } }"
                      >
                        {{ author.username }}
                      </span>
                    </template>
                  </div>
                </div>
                <div class="is-flex is-flex-direction-row is-justify-content-space-between is-align-items-center">
                  <!-- Titre de la fiction -->
                  <div>
                    <BTooltip
                      v-if="selectedChapter.fictionMetadata?.watched"
                      label="Fiction à surveiller"
                      :append-to-body="true"
                      position="is-top"
                    >
                      <BIcon icon="warning" type="is-danger" />
                    </BTooltip>
                    <span class="is-italic is-size-6">{{ selectedChapter.fictionMetadata?.title }}</span>
                  </div>
                  <!-- Caétgorie -->
                  <BTaglist class="mb-0">
                    <a
                      v-for="characteristic in selectedChapter.fictionMetadata?.characteristics"
                      :key="'tag_' + characteristic.characteristicId.toString()"
                      :href="'auteurs/' + characteristic.characteristicId"
                      ><BTag :class="[getClassType(characteristic), 'mt-0  mb-1 mr-2 is-size-8']" type="is-info">{{
                        characteristic.name
                      }}</BTag></a
                    >
                  </BTaglist>
                </div>
                <!-- Raisons et auteur de la dernière invalidation -->
                <article v-if="selectedVersion?.invalidationReasonIds?.length ?? 0 > 0" class="message is-danger">
                  <div class="message-body px-2 py-2">
                    <BCollapse :open="false" aria-id="invalidationMessageDetails" animation="slide">
                      <template #trigger="props">
                        <div class="is-flex is-flex-direction-row is-justify-content-space-between">
                          <p aria-controls="invalidationMessageDetails" :aria-expanded="props.open">
                            Invalidé le
                            <strong>{{ selectedVersion?.invalidationDate?.toLocaleDateString() }}</strong> par
                            <strong>{{ selectedVersion?.invalidationUser?.username }}.</strong> Motif(s) :
                            <span
                              v-for="(invalidationReasonId, index) in selectedVersion?.invalidationReasonIds"
                              :key="index"
                            >
                              <span v-if="index > 0">, </span>
                              <strong>{{
                                configStore.invalidationReasons.find(
                                  (t) => t.invalidationReasonId == invalidationReasonId,
                                )?.reason
                              }}</strong>
                            </span>
                          </p>
                          <BIcon class="is-clickable" :icon="props.open ? 'caret-up' : 'caret-down'" />
                        </div>
                      </template>
                      <p v-if="(selectedVersion?.publicComment?.length ?? 0) > 0">
                        <strong class="is-size-7">Message à l'auteur :</strong>
                        <br />
                        <span class="is-size-7">{{ selectedVersion?.publicComment }}</span>
                      </p>
                      <p v-if="(selectedVersion?.privateComment?.length ?? 0) > 0">
                        <strong class="is-size-7">Commentaire de la modération :</strong>
                        <br />
                        <span class="is-size-7">{{ selectedVersion?.privateComment }}</span>
                      </p>
                    </BCollapse>
                  </div>
                </article>
                <!-- Sur les chapitres marqués en à discuter -> affichage de l'éventuel message de la modé -->
                <article
                  v-if="selectedChapter.validationStatus == ChapterValidationStatusEnum.AwaitingDiscussion"
                  class="message is-warning"
                >
                  <div class="message-body px-2 py-2">
                    <BCollapse :open="false" aria-id="invalidationMessageDetails" animation="slide">
                      <template #trigger="props">
                        <div class="is-flex is-flex-direction-row is-justify-content-space-between">
                          <p aria-controls="invalidationMessageDetails" :aria-expanded="props.open">A discuter</p>
                          <BIcon class="is-clickable" :icon="props.open ? 'caret-up' : 'caret-down'" />
                        </div>
                      </template>
                      <p v-if="(selectedVersion?.privateComment?.length ?? 0) > 0">
                        <strong class="is-size-7">Commentaire de la modération :</strong>
                        <br />
                        <span class="is-size-7">{{ selectedVersion?.privateComment }}</span>
                      </p>
                    </BCollapse>
                  </div>
                </article>
                <div class="columns">
                  <!-- Contenu du chapitre -->
                  <div class="column is-10">
                    <ChapterBody
                      :chapter="selectedChapter"
                      :summary="selectedChapter.fictionMetadata?.summary"
                      :storynotes="selectedChapter.fictionMetadata?.storynote"
                      :font-size-visible="false"
                      :tiptap-read-only-config="null"
                    />
                  </div>
                  <!-- Liste des versions -->
                  <div class="column">
                    <div class="card">
                      <div class="card-content pl-3 pr-1 py-3">
                        <div class="pr-4">
                          <div
                            class="is-italic is-size-7 has-text-primary is-flex is-flex-direction-row is-justify-content-space-between is-align-items-center"
                          >
                            <span class="has-text-weight-bold">Versions</span>
                            <b v-if="(availableVersions?.length ?? 0) > 0">{{
                              " (" + availableVersions?.length.toString() + ")"
                            }}</b>
                          </div>
                        </div>
                        <Simplebar class="custom-scrollbar-bio" data-simplebar-auto-hide="false">
                          <!-- <b-loading v-model="chaptersStatus" :is-full-page="false" /> -->
                          <ChaptersVersionItem
                            v-for="(version, index) in availableVersions"
                            :key="index"
                            :version="version"
                            :class="[
                              'mb-2',
                              'mr-4',
                              { 'is-color-even': index % 2 != 0 },
                              { 'is-color-odd': index % 2 == 0 },
                            ]"
                            :is-selected="(selectedVersion?.versionId ?? 0) == version.versionId"
                            @click="() => onVersionSelected(version)"
                          />
                        </Simplebar>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <!-- Footer -->
              <footer
                class="modal-card-foot p-3 is-flex is-flex-direction-row is-justify-content-space-between is-align-items-center"
              >
                <BButton
                  v-show="
                    selectedTab?.status == ChapterValidationStatusEnum.AwaitingDiscussion ||
                    selectedTab?.status == ChapterValidationStatusEnum.AwaitingValidation ||
                    selectedTab?.status == ChapterValidationStatusEnum.Published
                  "
                  label="Invalider"
                  type="is-danger"
                  :loading="false"
                  @click="
                    () => {
                      currentValidationOption = ModalActionEnum.Unvalidate;
                      batchModalActive = true;
                    }
                  "
                />
                <BButton
                  v-show="
                    selectedTab?.status == ChapterValidationStatusEnum.AwaitingValidation &&
                    selectedChapter.validationStatus == ChapterValidationStatusEnum.AwaitingValidation
                  "
                  label="A discuter"
                  type="is-warning"
                  :loading="false"
                  @click="
                    () => {
                      currentValidationOption = ModalActionEnum.Discuss;
                      batchModalActive = true;
                    }
                  "
                />
                <BButton
                  v-show="selectedTab?.status == ChapterValidationStatusEnum.AwaitingModification"
                  label="Renvoyer une notification"
                  type="is-warning"
                  :loading="false"
                  @click="
                    () => {
                      // TODO APPEL AU SERVEUR, SI SUCCES TOAST
                    }
                  "
                />
                <BButton
                  v-show="
                    selectedTab?.status == ChapterValidationStatusEnum.AwaitingDiscussion ||
                    selectedTab?.status == ChapterValidationStatusEnum.AwaitingModification ||
                    selectedTab?.status == ChapterValidationStatusEnum.AwaitingValidation
                  "
                  label="Valider"
                  type="is-primary"
                  :loading="false"
                  @click="
                    () => {
                      currentValidationOption = ModalActionEnum.Validate;
                      batchModalActive = true;
                    }
                  "
                />
              </footer>
            </div>
          </div>
        </div>
      </BTabItem>
    </BTabs>
    <!-- Modal de validation -->
    <BModal v-model="batchModalActive" scroll="keep" :has-modal-card="true" @after-enter="modalEntered">
      <form>
        <div class="modal-card">
          <header class="modal-card-head">
            <p class="modal-card-title">{{ selectedChapter?.title }}</p>
            <button type="button" class="delete" @click="() => (batchModalActive = false)"></button>
          </header>
          <section class="modal-card-body pb-1">
            <BField
              v-if="currentValidationOption == ModalActionEnum.Unvalidate"
              class="mb-4 input-border"
              label="Motif(s) d'invalidation"
              label-position="on-border"
              custom-class="has-text-primary"
            >
              <div class="pt-3 px-2">
                <BCheckbox
                  v-for="reason in configStore.invalidationReasons"
                  :key="reason.invalidationReasonId"
                  v-model="chapterValidationForm.invalidationReasonIds"
                  :native-value="reason.invalidationReasonId"
                  :required="currentValidationOption == ModalActionEnum.Unvalidate"
                >
                  {{ reason.reason }}
                </BCheckbox>
              </div>
            </BField>
            <BField
              v-if="
                currentValidationOption == ModalActionEnum.Unvalidate ||
                currentValidationOption == ModalActionEnum.Validate
              "
              label="Message à l'auteur"
              label-position="on-border"
              custom-class="has-text-primary"
            >
              <BInput
                v-model="chapterValidationForm.publicComment"
                maxlength="500"
                type="textarea"
                placeholder="Ce message sera visible par l'auteur"
                custom-class="pb-0"
                :required="currentValidationOption == ModalActionEnum.Unvalidate"
              />
            </BField>
            <BField
              label="Commentaire de la modération (non visible par l'auteur)"
              label-position="on-border"
              custom-class="has-text-primary"
            >
              <BInput
                v-model="chapterValidationForm.privateComment"
                maxlength="200"
                type="textarea"
                placeholder="Ce message ne sera pas visible par l'auteur"
                custom-class="pb-0"
              />
            </BField>
          </section>
          <footer class="modal-card-foot">
            <BButton
              :expanded="true"
              :disabled="modalValidateFormIsValid == false"
              :label="modalValidateButton"
              :type="modalValidateType"
              :loading="isModalLoading"
              @click="versionModelUpdated"
            />
          </footer>
        </div>
      </form>
    </BModal>
  </div>
</template>

<script setup lang="ts">
//#region Imports
import {
  ChapterModel,
  type CharacteristicModel,
  FanfictionModel,
  VersionModel,
  type BatchChapterFilters,
} from "~/models";
import { ChapterValidationStatusEnum, type ChapterValidationData } from "~/types/fanfictions";
import { AuthorData, UserData } from "~/types/users";
import { getClassTypeColor } from "~/utils/characteristics";
import type { CharacteristicData } from "~/types/characteristics";
//#endregion

//#region Internal types
enum ModalActionEnum {
  Unvalidate = 1,
  Discuss = 2,
  Validate = 3,
}
//#endregion

//#region Usings
const { data } = useCustomAuth();
//#endregion

//#region Reactive
const activeTab = ref<number>(0);
const tabs = ref([
  { label: "En attente", status: ChapterValidationStatusEnum.AwaitingValidation },
  { label: "Invalidés", status: ChapterValidationStatusEnum.AwaitingModification },
  { label: "Validés", status: ChapterValidationStatusEnum.Published },
]);
const chapterFilters = ref<BatchChapterFilters>({
  searchTerm: null,
  awaitingDiscussionOnly: false,
  watchedAuthors: false,
});
const selectedChapter = ref<ChapterModel | null>(null);
const availableVersions = ref<VersionModel[] | null>(null);
const selectedVersion = ref<VersionModel | null>(null);
const batchModalActive = ref<boolean>(false);
const chapterValidationForm = ref<ChapterValidationData>({
  publicComment: null,
  privateComment: null,
  invalidationReasonIds: [],
});
const isModalLoading = ref<boolean>(false);
const currentValidationOption = ref<ModalActionEnum>(ModalActionEnum.Unvalidate);
//#endregion

//#region Reférences de la template
//const cboInvalidationMotif = useTemplateRef<HTMLElement>("cboInvalidationMotif");
//#endregion

//#region Data
// Chapitres en attente de validation
// TODO POUR LE DEBUG UNIQUEMENT
const configStore = useConfigStore();
const debug_chapters = ref<ChapterModel[]>([]);
const debug_versions = ref<VersionModel[]>([]);
for (let i = 1; i <= 100; i++) {
  // Ajout des chapitres debug
  const c = new ChapterModel({
    chapterId: i,
    order: i % 3 == 0 ? 1 : i,
    title: "Chapitre " + i.toString(),
    validationStatus:
      i == 2 || i == 5 || i == 20 || i == 48
        ? ChapterValidationStatusEnum.AwaitingDiscussion
        : ChapterValidationStatusEnum.AwaitingValidation,
    submissionDate: new Date(),
    authors:
      i % 2 == 0
        ? [new AuthorData({ username: "SUZYtfr", watched: i == 5 })]
        : [new AuthorData({ username: "PasseMontagne48", watched: i == 5 })],
    startNote:
      "Notre jeune toucher défendre paraître. Engager veille cour. Herbe par monter matière environ là supérieur. Remettre connaître passer oncle créer rêver. Refuser rire demande corps important voiture calmer couche. Haine brusquement frapper travers combien. Joue menacer pays éprouver envie. Sorte quelque supporter énorme. Aider coûter ainsi rocher guère. Résoudre parti conscience.",
    endNote:
      "Cesse retrouver blanc souffrance quatre mine rayon. Jeune hauteur verre attitude sans. Exécuter aile résistance ton. Décrire musique malgré naître émotion inconnu. Me puis chambre puissance. Supporter regretter reconnaître spectacle.",
    fictionMetadata: new FanfictionModel({
      title: "Le titre de ma fiction " + i.toString(),
      summary:
        "Un bain. Qui a dit que prendre un bain au milieu de la nuit, qui plus est chez une inconnue, ne pouvait pas rendre ce cadeau plus délicieux ? Le FanArt est de LathronAniron",
      storynote:
        "OS cadeau pour Gudulette. Un grand merci à Lucette pour son aide et ses précieux conseils ainsi qu'à LaLouisaBlack.",
      watched: i == 6,
      characteristics:
        configStore.characteristics != null
          ? ([
              configStore.characteristics[Math.floor(Math.random() * (configStore.characteristics?.length - 1))],
              configStore.characteristics[Math.floor(Math.random() * (configStore.characteristics?.length - 1))],
              configStore.characteristics[Math.floor(Math.random() * (configStore.characteristics?.length - 1))],
              configStore.characteristics[Math.floor(Math.random() * (configStore.characteristics?.length - 1))],
            ] as CharacteristicModel[])
          : [],
    }),
  });
  if (i < 80)
    c.validationStatus =
      i == 2 || i == 5 || i == 20 || i == 48
        ? ChapterValidationStatusEnum.AwaitingDiscussion
        : ChapterValidationStatusEnum.AwaitingValidation;
  else if (i >= 80 && i < 90) c.validationStatus = ChapterValidationStatusEnum.AwaitingModification;
  else c.validationStatus = ChapterValidationStatusEnum.Published;
  c.submissionDate?.setDate(c.submissionDate.getDate() - i);
  debug_chapters.value.push(c);

  // Ajout des versions debug, pour chaque chapitre entre 1 et 5 versions
  for (let j = 1; j < Math.random() * 5 + 1; j++) {
    const v = new VersionModel({
      versionId: j * i,
      chapterId: i,
      authors: c.authors,
      words: Math.random() * 5000,
      text: "<p style=\"text-align:justify\">Stewart Ackerley n’était pas dupe. Revenir à Poudlard après tant d’années ne devait pas aider son frère. Il pouvait voir ce dos se dessiner devant lui et marcher d’un pas presque furieux dans la forêt interdite. Ils étaient arrivés à la limite de la protection anti-transplanage de Poudlard et ils avaient dû remonter tous les deux la forêt jusqu’au lieu de rendez-vous. Stewart n’entendait pas les bruits mystérieux de cet endroit, il n’entendait plus rien de toute façon. Ni les brindilles qui craquaient sous leurs pas, ni les récriminations de son frère qui lui demandait d’avancer plus vite. <br> Andrew se retournait toutes les vingt secondes environ, Stewart les comptait. Son frère signait rapidement de se dépêcher à chaque fois mais Andrew n’arrivait pas à partager son impatience. Ils allaient vers quelque chose de dangereux et, si près d’eux, se déroulait la cérémonie officielle. <br><br> Evidemment, Stewart avait reçu l’invitation du Ministère. L’enveloppe était restée posée sur le meuble de l’entrée trois semaines avant qu’il ne l’ouvre. Il l’avait déchirée en si petits morceaux, comme un puzzle impossible à résoudre ; il n’irait pas. Il n’irait plus jamais dans ces cérémonies hypocrites où chacun et chacune montrait que tout allait bien. Que, dorénavant, leurs vies étaient sereines, apaisées. Qu’ils faisaient partie du bien, et puis c’était tout ce qui comptait. <br><br> Quand Nott leur avait parlé de son projet, Stewart n’avait pas tout de suite adhéré à l’idée. Il n’approuvait toujours pas que le rassemblement soit si prêt des Héros, des employés du Ministère, de ses Aurors et de sa Brigade de crédules. Il aurait aimé un endroit plus discret. Mais il avait quand même suivi Andrew, avait enfilé sa robe noire de sorcier et glissé sur son visage un masque simple qui, dans le miroir, le terrifiait. Son frère avait encore cette colère sourde de la mutilation imposée à son frère pendant la Bataille, cette haine contre ceux qui avaient tué leurs parents. <br><br> A vingt-cinq ans, Stewart était encore terrifié par bien des choses. C’était son jardin secret. Des aveux qu’il ne ferait jamais à son frère ; il n’en avait pas le droit. <br> Andrew avait tout donné pour l’aider après la Bataille de Poudlard et la chute du Ministère. Il avait plaidé pour son retour à Poudlard malgré la surdité, pour l’importance des ASPICS, du diplôme et une place dans une société honnie. <br> Andrew avait dissimulé ses dénonciations et n’avait pas perdu son travail. Et depuis que Stewart n’arrivait pas à trouver de travail, son frère s’était occupé de lui. <br><br> Plus que par lien familial, les deux frères partageaient la conviction que le monde devrait être meilleur pour eux. Auraient dû. Qu’ils avaient le sang qu’il fallait, qu’ils auraient dû avoir les métiers mis pourtant dans des mains impures. Mais ils s’étaient tus. <br> Jusqu’à aujourd’hui. <br><br> Ils arrivèrent rapidement dans la clairière éclairée par le feu magique qui brûlait. Andrew vit une jeune femme arriver et se vêtir elle aussi du signe encore commun aux Mangemorts. Il ne dit rien à son frère, elle ne devait pas non plus être aussi à l’aise que d’autres parmi les partisans. Leur cérémonie à eux commença dès que le cercle des silhouettes sombres fut complet. Qu’importe ce qui se passait de l’autre côté de la lisière, qu’importe que ces hommes et femmes pleuraient eux aussi des morts. Ils ne se réjouissaient même pas de leur victoire et préféraient se morfondre de leurs pertes. Remuer la plaie, année après année. Sans aucune considération pour les perdants. <br><br> Ceux qui ont perdu leur famille mais aussi leur idéal. <br> Ceux qui n’arrivent pas aujourd’hui à partager leurs idées. <br> Ceux qui sont purs mais reniés, pour un défaut, pour un pécher. <br> <br> Pour leur surdité. <br> Stewart n’entendait pas ce que disait l’homme qui venait de se diriger au centre du cercle. L’homme ou la femme, qu’importe. Il avait déjà vu chez son frère des femmes incroyables débattre des mesures à prendre, mais il avait toujours été mis de côté aussi par ses propres camarades. Il ne pouvait pas participer à une conversation qui se déroulait trop vite ; il apprenait à lire sur les lèvres depuis dix ans à présent ; il parlait en langue des signes avec son frère, mais il restait solitaire. <br> Finalement, Stewart se sentait aussi seul à cette commémoration que s’il était allé à celle du Ministère. Il ne pouvait pas vraiment partager ses pensées, son frère se sentirait blessé. Trahi. Le Mangemort au centre de leur cercle continuait de parler. Stewart ne pouvait pas lire sur les lèvres, il regrettait le secret imposé de leurs masques. Alors il passait à côté de l’essence même qui animait leur assemblée. Il n’opinait pas pour des propos dont il devinait le sens. D’abord parce qu’il n’était pas certain de tout approuver, ensuite parce qu’il n’arrivait pas à sentir au fond de lui cet enthousiasme indéfectible. <br> Andrew lui reprocherait plus tard, Steward le devinait. Il hocherait les épaules puis demanderait la retranscription incomplète de ce qui s’était dit. C'était tout. <br><br> A cet instant cependant, il se sentait mis au banc de leur assemblée. Son seul refuge devenait-il pire encore que la société qu’ils critiquaient ? Il secoua la tête pour chasser ses pensées et se concentra sur les flammes ardentes qui dansaient au milieu d’eux. <br><br> Tandis que l’homme au centre du cercle - Nott surement, finit-il par réaliser - continuait de ponctuer son discours de mouvements vifs, Stewart sentit le grondement se propager dans son corps. Il le sentit bien avant le reste des Mangemorts qui ne se préoccupaient pas de la vie propre de la forêt autour d’eux. <br><br> D’où ce grondement sourd venait-il ? D’où venait le tremblement qui peu à peu sema la panique dans le cercle des hommes et femmes vêtus de noir ? Pris de peur, Stewart se retourna brusquement et vit cette masse arriver vers eux à travers les arbres. <br> Les centaures esquivaient habilement les arbres, comme si ces obstacles n’étaient rien et que leur seul but était ce cercle à détruire. Ce cercle de résistance. <br> Tous prirent la fuite dans un mouvement si désordonné que Stewart fut certain de voir un corps renversé dans la précipitation. Il pensa un instant qu'il aurait aimé voir le sorcier au centre lever sa baguette, puis voir le mince filet de lumière verte et noire s'élever jusqu'au ciel. Que les hypocrites de la cérémonie officielle paniquent, eux aussi. Mais le Mangemort ne l'avait pas fait et il partait à présent vers Poudlard, dans la direction opposée. <br> Andrew arracha Stewart de ses pensées. Il lui attrapa le bras et ils coururent tous les deux de toutes leurs forces vers l’endroit le plus proche pour transplaner. Qu’importe les autres ! Qu'importe si les Centaures préviendraient le Ministère, qu'importe si de n'être pas venu à la commémoration serait par la suite mal vu ! <br> Qu’importe tout ça ! Il n’y avait que Andrew et Stewart courant dans leurs robes pour leur sécurité. <br> Finalement, il n’était pas si seul.</p>",
      versionDate: new Date(),
    });
    v.versionDate?.setDate(v.versionDate.getDate() - j);
    // Version invalidée
    if (c.validationStatus == ChapterValidationStatusEnum.AwaitingModification) {
      v.invalidationReasonIds = [
        configStore.invalidationReasons[Math.floor(Math.random() * (configStore.invalidationReasons.length - 1))]!
          .invalidationReasonId,
      ];
      v.invalidationDate = new Date();
      v.publicComment =
        "Votre texte comporte des fautes d'orthographe et de grammaire. Merci de vous relire ou de vous faire relire.";
      v.privateComment = "Ce morceau de commentaire n'est visible que par la modération.";
      if (data.value != null) {
        v.invalidationUserId = data.value.id ?? 0;
        v.invalidationUser = new UserData({ username: data.value.username, userId: data.value.id });
      }
    }
    debug_versions.value.push(v);
  }
}

// Vrai appel
// const {
//   data: chaptersAwaitingValidation,
//   status: chaptersAwaitingValidationStatus,
//   execute,
//   clear,
// } = await getChapters(chapterFilters.value, {
//   immediate: false,
// });
//#endregion

//#region Computed
const selectedTab = computed(() => {
  if (activeTab.value >= tabs.value.length) return null;
  return tabs.value[activeTab.value];
});

const headerFilterLabel = computed(() => {
  if (activeTab.value >= tabs.value.length) return "";
  switch (tabs.value[activeTab.value]!.status) {
    case ChapterValidationStatusEnum.AwaitingValidation:
      return "Chapitres en attente de validation";
    case ChapterValidationStatusEnum.AwaitingModification:
      return "Chapitres invalidés";
    case ChapterValidationStatusEnum.Published:
      return "Chapitres validés";
    default:
      return "";
  }
});

const chapters = computed(() => {
  if (selectedTab?.value == null) {
    return null;
  } else if (selectedTab.value.status == ChapterValidationStatusEnum.AwaitingValidation) {
    return debug_chapters.value.filter((t) => {
      return (
        (chapterFilters.value.awaitingDiscussionOnly
          ? t.validationStatus == ChapterValidationStatusEnum.AwaitingDiscussion
          : t.validationStatus == ChapterValidationStatusEnum.AwaitingDiscussion ||
            t.validationStatus == ChapterValidationStatusEnum.AwaitingValidation) &&
        (chapterFilters.value.watchedAuthors
          ? t.fictionMetadata?.watched || t.authors?.some((x) => x.watched)
          : true) &&
        ((chapterFilters.value.searchTerm?.length ?? 0) > 0
          ? t.title
              .trim()
              .toLowerCase()
              .normalize("NFD")
              .replace(/[\u0300-\u036F]/g, "")
              .includes(
                (chapterFilters.value.searchTerm ?? "")
                  .trim()
                  .toLowerCase()
                  .normalize("NFD")
                  .replace(/[\u0300-\u036F]/g, ""),
              ) ||
            t.authors?.some(
              (x) =>
                x.username != null &&
                x.username
                  .trim()
                  .toLowerCase()
                  .normalize("NFD")
                  .replace(/[\u0300-\u036F]/g, "")
                  .includes(
                    (chapterFilters.value.searchTerm ?? "")
                      .trim()
                      .toLowerCase()
                      .normalize("NFD")
                      .replace(/[\u0300-\u036F]/g, ""),
                  ),
            )
          : true)
      );
    });
  } else if (selectedTab.value.status == ChapterValidationStatusEnum.AwaitingModification) {
    return debug_chapters.value.filter((t: ChapterModel) => {
      return (
        t.validationStatus == ChapterValidationStatusEnum.AwaitingModification &&
        (chapterFilters.value.watchedAuthors ? t.fictionMetadata?.watched || t.authors?.some((x) => x.watched) : true)
      );
    });
  } else if (selectedTab.value.status == ChapterValidationStatusEnum.Published) {
    return debug_chapters.value.filter((t: ChapterModel) => {
      return (
        t.validationStatus == ChapterValidationStatusEnum.Published &&
        (chapterFilters.value.watchedAuthors ? t.fictionMetadata?.watched || t.authors?.some((x) => x.watched) : true)
      );
    });
  } else return null;
});

// Label du bouton de la modal d'invalidation / discuter / validation
const modalValidateButton = computed((): string => {
  switch (currentValidationOption.value) {
    case ModalActionEnum.Unvalidate:
      return "Invalider le chapitre";
    case ModalActionEnum.Discuss:
      return 'Marquer le chapitre en "à discuter"';
    case ModalActionEnum.Validate:
      return "Valider le chapitre";
  }
  return "";
});

// Type (danger, warning, primary) modale d'invalidation / discuter / validation
const modalValidateType = computed((): string => {
  switch (currentValidationOption.value) {
    case ModalActionEnum.Unvalidate:
      return "is-danger";
    case ModalActionEnum.Discuss:
      return "is-warning";
    case ModalActionEnum.Validate:
      return "is-primary";
  }
  return "";
});

// La form est-elle valide
const modalValidateFormIsValid = computed((): boolean => {
  if (currentValidationOption.value == ModalActionEnum.Unvalidate)
    return (
      (chapterValidationForm.value?.publicComment?.length ?? 0) > 0 &&
      (chapterValidationForm.value?.invalidationReasonIds?.length ?? 0) > 0
    );
  return true;
});
//#endregion

//#region Watchers
// Au changement d'onglet, reset du contenu
watch(selectedTab, () => {
  selectedVersion.value = null;
  selectedChapter.value = null;
});
//#endregion

//#region Functions
// Sélection d'un chapitre
const onChapterSelected = (chapter: ChapterModel): void => {
  // TODO lancer les appels de chargement du chapitre et de la liste des version
  // Pour l'instant simulé ci-dessous
  selectedChapter.value = chapter;
  availableVersions.value = debug_versions.value.filter((t: VersionModel) => t.chapterId == chapter.chapterId);
  selectedVersion.value = availableVersions.value[0]!;
};

const onVersionSelected = (version: VersionModel): void => {
  // TODO appeler pour récupérer le text de la version
  selectedVersion.value = version;
};

const getClassType = (characteristic: CharacteristicData): string => {
  return getClassTypeColor(characteristic);
};

const modalEntered = (): void => {
  //cboInvalidationMotif.value?.focus();
};

const versionModelUpdated = (): void => {
  // TODO, pour l'instant sur l'objet local mais sur l'API plus tard
  if (selectedVersion.value == null || selectedChapter.value == null || data.value == null) return;
  switch (currentValidationOption.value) {
    case ModalActionEnum.Unvalidate:
      selectedChapter.value.validationStatus = ChapterValidationStatusEnum.AwaitingModification;
      selectedVersion.value.privateComment = chapterValidationForm.value.privateComment;
      selectedVersion.value.publicComment = chapterValidationForm.value.publicComment;
      selectedVersion.value.invalidationReasonIds = chapterValidationForm.value.invalidationReasonIds;
      selectedVersion.value.invalidationUserId = data.value.id;
      selectedVersion.value.invalidationUser = new UserData({ username: data.value.username, userId: data.value.id });
      selectedVersion.value.invalidationDate = new Date();
      // TODO côté serveur il faut envoyer un mail de notification
      break;
    case ModalActionEnum.Discuss:
      selectedChapter.value.validationStatus = ChapterValidationStatusEnum.AwaitingDiscussion;
      selectedVersion.value.privateComment = chapterValidationForm.value.privateComment;
      break;
    case ModalActionEnum.Validate:
      selectedChapter.value.validationStatus = ChapterValidationStatusEnum.Published;
      selectedVersion.value.privateComment = chapterValidationForm.value.privateComment;
      selectedVersion.value.publicComment = chapterValidationForm.value.publicComment;
      break;
  }
  // Reset
  batchModalActive.value = false;
  chapterValidationForm.value = { invalidationReasonIds: [], privateComment: "", publicComment: "" };
  selectedVersion.value = null;
  selectedChapter.value = null;
};
//#endregion

//DEBUG
selectedChapter.value = debug_chapters.value[0]!;
</script>

<style lang="scss" scoped>
.custom-scrollbar-bio {
  height: auto;
  max-height: 50vh;
}

.input-border {
  border: 1px solid #d6d9e0;
  border-radius: 3px;
}
.input-border:hover {
  border: 1px solid #b5b5b5;
}
</style>
