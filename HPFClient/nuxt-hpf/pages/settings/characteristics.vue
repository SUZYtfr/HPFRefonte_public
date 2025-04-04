<template>
  <div class="container is-fluid">
    <div class="columns">
      <div class="column is-auto">
        <div style="/*overflow-y: auto; height: 400px;*/">
          <b-dropdown aria-role="list" class="mb-2" @active-change="onDropdownToggled">
            <template #trigger="{ active }">
              <b-button
                label="Ajouter une nouvelle entrée"
                type="is-primary"
                :icon-right="active ? 'chevron-up' : 'chevron-down'"
              />
            </template>
            <b-dropdown-item
              v-for="(type, index) in characteristics_types"
              :key="'option_type_' + index.toString()"
              :class="[getCaracteristicTypeColor(type.id), '']"
              :value="type.id"
              aria-role="menuitem"
              @click="onNewCarac(type)"
            >
              Ajouter aux <b>{{ type.name }}</b>
            </b-dropdown-item>
            <!-- Plus tard -->
            <!--<hr class="dropdown-divider">
            <b-dropdown-item aria-role="listitem">
              Ajouter une nouvelle catégorie
            </b-dropdown-item>-->
          </b-dropdown>
          <!-- <b-button @click="test">
            TEST
          </b-button> -->
          <b-table
            ref="carac-table"
            :data="filteredCharacteristicType"
            :paginated="false"
            :loading="listLoading"
            :striped="true"
            :hoverable="true"
            detailed
            custom-detail-row
            sort-icon="chevron-up"
            default-sort="user.first_name"
            aria-next-label="Page suivante"
            aria-previous-label="Page précédente"
            aria-page-label="Page"
            aria-current-label="Page actuelle"
            :debounce-search="1000"
            :selected="selectedItem"
            :show-detail-icon="true"
            :sticky-header="true"
            :row-class="(row, index) => getTableParentRowClass(row, index)"
            @click.native="onRowClickNative"
          >
            <!-- Libelle -->
            <b-table-column
              field="name"
              label="Libellé"
            >
              <template #subheading>
                <b-input
                  v-model="refreshFilter"
                  placeholder="Filtrer"
                  type="search"
                  icon="search"
                  size="is-small"
                />
              </template>
              <template #default="props">
                {{ props.row.name + " (" + props.row.characteristics.length.toString() + ")" }}
              </template>
            </b-table-column>

            <!-- Activé -->
            <b-table-column field="enabled" label="Activé" width="10" centered>
              <template #subheading>
                <b-checkbox
                  type="search"
                  class="mt-1"
                />
              </template>
              <template #default="props">
                <b-checkbox
                  :value="props.row.enabled"
                  type="is-primary"
                  :disabled="true"
                />
              </template>
            </b-table-column>

            <!-- Visible -->
            <b-table-column field="visible" label="Visible" width="10" centered>
              <template #subheading>
                <b-checkbox
                  type="search"
                  class="mt-1"
                />
              </template>
              <template #default="props">
                <b-checkbox
                  :value="props.row.visible"
                  type="is-primary"
                  :disabled="true"
                />
              </template>
            </b-table-column>

            <!-- Nombre de référence -->
            <b-table-column field="fiction_count" label="Références" centered>
              {{ "" }}
            </b-table-column>

            <!-- Ordre -->
            <b-table-column field="order" label="Ordre" centered>
              {{ "" }}
            </b-table-column>

            <!-- Ligne enfant -->
            <template #detail="props">
              <tr
                v-for="(item, index) in props.row.characteristics"
                :key="item.id"
                :ref="(el) => { instance.refs[`child-row-${item.id.toString()}`] = el }"
                :class="[((index % 2 == 0) ? getCaracteristicTypeColorLight(item.characteristic_type_id) : getCaracteristicTypeColorLighter(item.characteristic_type_id)),
                         { 'highlighted': (item.characteristic_type_id === (droppedOnRow?.object?.characteristic_type_id ?? -1) && index === (droppedOnRow?.index ?? -1) && (droppedOnRow?.dropAsChild ?? false) === false) },
                         { 'highlighted-child': (item.characteristic_type_id === (droppedOnRow?.object?.characteristic_type_id ?? -1) && index === (droppedOnRow?.index ?? -1) && (droppedOnRow?.dropAsChild ?? false) === true) }]"
                :selected="selectedItem"
                draggable="true"
                @click="selectedItem = item"
                @dragstart="dragstart(item, index, $event)"
                @drop="drop(item, index, $event)"
                @dragover="dragover(item, index, $event)"
              >
                <!-- { 'highlighted': item.order === (droppedOnRow?.object?.order ?? -1) } -->
                <td />
                <!-- └ ├ -->
                <!-- <td>&nbsp;&nbsp;&nbsp;&nbsp;{{ (item.parent_id === null ? item.name : (item.name) ) }}</td> -->
                <td>
                  <span v-if="item.parent_id == null">&nbsp;&nbsp;&nbsp;&nbsp;</span>
                  <span v-for="(number, index) in item.depth" :key="index">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>
                  <font-awesome-icon v-if="item.parent_id != null" icon="level-up-alt" rotation="90" class="" />
                  <span :class="[{'ml-2': (item.parent_id !== null)}]">{{ item.name }}</span>
                </td>
                <td class="has-text-centered" data-label="Activé">
                  <b-checkbox
                    :value="item.enabled"
                    type="is-primary"
                    :disabled="true"
                  />
                </td>
                <td class="has-text-centered" data-label="Activé">
                  <b-checkbox
                    :value="item.visible"
                    type="is-primary"
                    :disabled="true"
                  />
                </td>
                <td class="has-text-centered">
                  {{ item.fiction_count }}
                </td>
                <td class="has-text-centered">
                  {{ (item.order + 1).toString() }}
                </td>
              </tr>
            </template>

            <!-- Template si vide -->
            <template #empty>
              <div class="has-text-centered">
                Aucune donnée (essayez d'ajuster les filtres)
              </div>
            </template>
          </b-table>
        </div>
      </div>

      <!-- Colonne de droite éditeur d'utilisateur -->
      <div v-if="selectedItem != null" class="column is-narrow">
        <div class="card">
          <header class="card-header sub-title">
            <p class="card-header-title is-centered">
              {{ selectedItem.name }}
            </p>
          </header>
          <div class="card-content px-3 py-3">
            <b-field
              label="Libellé"
              label-position="on-border"
              custom-class="has-text-primary"
            >
              <b-input
                v-model="selectedItem.name"
                type="text"
                placeholder="Libellé"
                required
                pattern="^.{3,30}$"
                validation-message="Veuillez saisir un libellé compris entre 3 et 30 caractères"
                :expanded="true"
              />
            </b-field>

            <b-field
              v-if="(selectedItem instanceof CharacteristicModel)"
              label="Description"
              label-position="on-border"
              custom-class="has-text-primary"
            >
              <b-input
                v-model="selectedItem.description"
                type="textarea"
                placeholder="Description"
              />
            </b-field>
            <b-field>
              <b-checkbox :value="selectedItem.enabled">
                Activée
              </b-checkbox>
            </b-field>
            <b-field>
              <b-checkbox :value="selectedItem.visible">
                Visible
              </b-checkbox>
            </b-field>
            <div v-if="(selectedItem instanceof CharacteristicTypeModel)">
              <b-field
                label="Occurences min"
                label-position="on-border"
                custom-class="has-text-primary"
              >
                <b-numberinput
                  v-model="selectedItem.min_occurence"
                  placeholder="Occurences min"
                  :min="0"
                  size="is-small"
                  type="is-primary"
                />
              </b-field>
              <div class="is-flex is-flex-direction-row">
                <p class="control">
                  <b-checkbox v-model="maxOccurenceEnable" class="mt-1" />
                </p>
                <b-field
                  label="Occurences max"
                  label-position="on-border"
                  custom-class="has-text-primary"
                >
                  <b-numberinput
                    v-model="selectedItem.max_occurence"
                    placeholder="Occurences max"
                    :min="0"
                    size="is-small"
                    type="is-primary"
                    :disabled="selectedItem.max_occurence === null"
                  />
                </b-field>
              </div>
            </div>
            <div class="is-flex is-flex-direction-row is-align-items-center is-align-content-space-between" />
          </div>
          <footer class="modal-card-foot p-3">
            <b-button
              :disabled="!formIsValid"
              label="Enregistrer"
              type="is-primary"
              :loading="loading"
              @click="updateItem()"
            />
            <b-button
              label="Supprimer"
              type="is-danger"
              :loading="loading"
              @click="deleteItem()"
            />
          </footer>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { CharacteristicModel, CharacteristicTypeModel } from "~/models/characteristics";
import { getCaracteristicTypeColor, getCaracteristicTypeColorLight, getCaracteristicTypeColorLighter } from "@/utils/characteristics";
import { searchCharacteristics, searchCharacteristicsTypes, updateCharacteristic, updateCharacteristicsType, deleteCharacteristic, createCharacteristic, reorderCharacteristics } from "~/api/private/characteristics";
import { SnackbarProgrammatic as Snackbar } from "buefy";
import { nextTick, getCurrentInstance } from "vue";

// https://stackoverflow.com/a/79534157/13038487
const instance = getCurrentInstance()!;

const caracTable = useTemplateRef("carac-table");

let selectedItem = ref<CharacteristicModel | CharacteristicTypeModel | null>(null);

let timerId: number = 0;

const maxOccurenceEnable = ref<boolean>(false);
const refreshFilter = ref<string | null>(null);
const caracFilter = ref<string | null>(null);

// Ligne en cours de déplacement
const draggedRow = ref<any>({
  target: null,
  object: null,
  index: null,
  childs: []
});

// Ligne sur laquelle on drop
const droppedOnRow = ref<any>({
  target: null,
  object: null,
  index: null,
  dropAsChild: false
});

const formIsValid = computed<boolean>(() => {
  if (selectedItem.value == null) return false;
  return true;
});

watch(maxOccurenceEnable, () => {
  if (selectedItem.value instanceof CharacteristicTypeModel) {
    if (maxOccurenceEnable) selectedItem.value.max_occurence = 0;
    else selectedItem.value.max_occurence = null;
  }
});

watch(refreshFilter, () => {
  clearTimeout(timerId);
  timerId = window.setTimeout(() => caracFilter.value = refreshFilter.value, 500);
});

const { data: characteristics, status: characteristicStatus } = await searchCharacteristics(null);
const { data: characteristics_types, status: characteristicTypeStatus } = await searchCharacteristicsTypes();

watch(characteristics_types, () => {
  characteristics_types.value?.forEach((parent: CharacteristicTypeModel) => {
    parent.characteristics = characteristics.value?.filter((item: CharacteristicModel) => {
      return item.characteristic_type_id === parent.id;
    });
  });
});

const filteredCharacteristicType = computed<CharacteristicTypeModel[]>(() => {
  if (characteristics_types.value && characteristics.value) {
    return prepareFilteredCarac();
  }
  return [];
})

const listLoading = computed<boolean>(() => {
  return (characteristicStatus.value === 'pending' || characteristicTypeStatus.value === 'pending');
});

const loading = ref<boolean>(false);

// Mettre à jour la caratéristique
async function updateItem(): Promise<void> {
  try {
    loading.value = true;
    if (selectedItem.value instanceof CharacteristicModel) {
      if (selectedItem.value.characteristic_id > 0) {
        await updateCharacteristic(selectedItem.value);
      } else {
        await createCharacteristic(selectedItem.value);
      }
    } else if (selectedItem.value instanceof CharacteristicTypeModel) {
      if (selectedItem.value.characteristic_type_id > 0) {
        await updateCharacteristicsType(selectedItem.value as CharacteristicTypeModel);
      }
    } else {
      throw "Erreur"
    }
    OpenToast(
      "Caractéristique mise à jour",
      "is-primary",
      5000,
      false,
      true,
      "is-bottom"
    );
  } catch (exception) {
    OpenToast("Erreur", "is-danger", 5000, false, true, "is-bottom");
  } finally {
    loading.value = false;
  }
}

async function deleteItem(): Promise<void> {
  if (selectedItem.value === null) return;

  // Confirmer l'action (seulement si ce n'est pas un nouvel item)
  if (selectedItem.value.id > 0) {
    new Snackbar().open({
      indefinite: true,
      message: "Confirmer la suppression ? (action irréversible)",
      cancelText: "Annuler",
      actionText: "Confirmer",
      type: "is-warning",
      onAction: () => {
        try {
          loading.value = true;
          if (selectedItem.value instanceof CharacteristicModel) {
            deleteCharacteristic(selectedItem.value);
          }
          selectedItem.value = null;
          characteristics.value = characteristics.value.filter((item: CharacteristicModel) => item.id !== 0);
          // prepareFilteredCarac();
          OpenToast(
            "Caractéristique supprimée",
            "is-primary",
            5000,
            false,
            true,
            "is-bottom"
          );
        } catch (exception) {
          OpenToast("Erreur", "is-danger", 5000, false, true, "is-bottom");
        } finally {
          loading.value = false;
        }
      }
    });
  } else {
    selectedItem.value = null;
    characteristics.value = characteristics.value.filter((item: CharacteristicModel) => item.id !== 0);
    // prepareFilteredCarac();
  }
}

// Construire les caractéristiques affichées (éventuellement filtrées)
function prepareFilteredCarac(): CharacteristicTypeModel[] {
  // On récupère les caractéristiques qui correspondent au filtre
  const filteredCharacteristics = characteristics.value?.filter((child: CharacteristicModel) => {
    return child.name.toUpperCase().includes((caracFilter.value?.toUpperCase() ?? ""));
  });

  // On récupère les caractétistiques types qui correspondent
  const caracTypeIds = filteredCharacteristics.map(({ characteristic_type_id }) => characteristic_type_id);
  const filteredCharacteristicsTypes = characteristics_types.value?.filter((item: CharacteristicTypeModel) => {
    return caracTypeIds.includes(item.id);
  });

  // On récupère l'arborescence complète
  filteredCharacteristics.forEach((item: CharacteristicModel) => {
    if (item.parent_id != null && filteredCharacteristics.find((parent: CharacteristicModel) => parent.id === item.parent_id) == null) {
      const missingParent = characteristics.value.filter((parent: CharacteristicModel) => {
        return parent.id === item.parent_id;
      });
      filteredCharacteristics.push(...missingParent);
    }
  });

  // Calculer la profondeur de chaque élément
  filteredCharacteristics.forEach((item) => {
    item.depth = getDepth(item, filteredCharacteristics);
  });

  // Enfin on remplit les caracatéristiques types
  filteredCharacteristicsTypes.forEach((parent: CharacteristicTypeModel) => {
    // On vide
    parent.characteristics = [];
    // On met uniquement celles filtrées
    parent.characteristics = filteredCharacteristics.filter((item: CharacteristicModel) => {
      return item.characteristic_type_id === parent.id;
    });
    // On tri sur l'ordre
    parent.characteristics = sortItems(parent.characteristics);
  });
  return filteredCharacteristicsTypes
}

// Préparer le style des lignes parent du tableau
function getTableParentRowClass(row: object, index: number): string {
  let style = "";
  if (row instanceof CharacteristicTypeModel) style += getCaracteristicTypeColor(row.id);
  return style;
}

// Gestion du style sélection des colonnes
// FIXME - @click ne donne plus un event comme avant mais la valeur de event.target.value directement
// event est toujours accessible via window, mais est déprécié
function onRowClickNative(item: any): void {
  selectedItem.value = item;
  const target: HTMLElement = event.target as HTMLElement;
  if (target.nodeName.toLowerCase() !== "td" && target.nodeName.toLowerCase() !== "tr") return;
  (caracTable.value as any).$el.querySelectorAll("tr").forEach((row: HTMLElement) => {
    row.classList.remove("is-selected");
  });
  if (target.nodeName.toLowerCase() === "td") target.parentElement.classList.add("is-selected");
  else target.classList.add("is-selected");
} 

// Ajout d'une nouvelle caractéristique
function onNewCarac(caracteristicType: CharacteristicTypeModel): void {
  // Enlever les précédents nouveaux items non poussés
  characteristics.value = characteristics.value.filter((item: CharacteristicModel) => item.id !== 0);

  // Créer la nouvelle entrée
  const newItem = new CharacteristicModel({
    characteristic_type_id: caracteristicType.id,
    parent_id: null,
    name: "Nouvelle entrée",
    description: null,
    visible: false,
    enabled: false
  });

  // console.log(newItem);
  // console.log(newItem instanceof CharacteristicModel);
  // L'ajouter aux entrées existantes
  characteristics.value.push(newItem);

  // prepareFilteredCarac();
  // // Reset les éventuels filtres
  // if ((this.caracFilter?.length ?? 0) > 0) this.caracFilter = null;

  // Expand la caractéristique type parent
  const caracType = filteredCharacteristicType.value.filter((item: CharacteristicTypeModel) => {
    return item.id === newItem.characteristic_type_id;
  });
  (caracTable.value as any).openDetailRow(caracType[0]);

  // Après l'ajout dans le dom, afficher et cliquer sur le nouvel élément
  nextTick(() => {
    const newTableRow = (instance.refs[`child-row-${newItem.id.toString()}`] as any);
    console.log(newTableRow)
    newTableRow.scrollIntoView({ behavior: "smooth" });
    newTableRow.click();
    newTableRow.classList.add("animate__animated", "animate__flash");
  });
}

// A l'ouverture du dropdown, reset les filtres éventuels
function onDropdownToggled(active: boolean): void {
  if (active && ((caracFilter.value?.length ?? 0) > 0)) caracFilter.value = null;
}

// Démarrer le déplacement d'une ligne enfant
function dragstart(row: CharacteristicModel, index: number, e: DragEvent): void {
  // Avant un drag, reset les filtres éventuels
  if (((caracFilter.value?.length ?? 0) > 0)) {
    caracFilter.value = null;
    e.preventDefault();
    return;
  }

  // Impossible de drag une carac non commitée (nouvel item)
  if (row.id === 0) {
    e.preventDefault();
    return;
  }

  // Enlever les précédentes marques de sélection
  (caracTable.value as any).$el.querySelectorAll("tr").forEach((row: HTMLElement) => {
    row.classList.remove("is-selected");
  });
  selectedItem = null;

  // Récupérer en mémoire l'élément qu'on déplace
  draggedRow.value = { target: e.target, object: row, index: index, childs: getAllChildren(characteristics.value, row.id).map(item => item.id) };

  // Mise en évidence de l'élément qu'on déplace
  draggedRow.value.target.classList.add("is-selected");
}

// Comportement lors du déplacement d'une ligne
function dragover(row: CharacteristicModel, index: number, e: DragEvent):void {
  e.preventDefault();
  if (e.target == null || e.dataTransfer == null) return;
  if ((droppedOnRow.value?.index ?? -1) === index && (droppedOnRow.value?.dropAsChild ?? false) === e.shiftKey) return;

  // On ne peut pas bouger une carac en dehors de son parent ni bouger un parent dans un enfant
  if (row.characteristic_type_id !== draggedRow.value.object.characteristic_type_id ||
    draggedRow.value.childs.includes(row.id)
  ) {
    droppedOnRow.value = null;
    e.dataTransfer.dropEffect = "none";
  } else {
    droppedOnRow.value = { target: e.target, object: row, index: index, dropAsChild: e.shiftKey };
    e.dataTransfer.dropEffect = "move";
  }
}

// Après un glisser déposer d'un élément
function drop(row: CharacteristicModel, index: number, e: DragEvent):void {
  // Vérifications de base
  if (droppedOnRow.value == null || // Impossible si pas de cible
    row.id === 0 || // Impossible de drop une carac non commitée (nouvel item)
    draggedRow.value.index === droppedOnRow.value.index // Pas de mouvement
  ) {
    e.preventDefault();

    // Reset
    draggedRow.value = null;
    droppedOnRow.value = null;
    return;
  }

  // Demander une confirmation après drop pour valider le changement d'ordre
  let parentObject: CharacteristicModel | null = null;
  let newPos = droppedOnRow.value.object.order;
  if (droppedOnRow.value.dropAsChild) {
    parentObject = droppedOnRow.value.object;
    newPos = 0;
  } else if (droppedOnRow.value.object.parent_id != null) {
    parentObject = characteristics.value.filter(item => item.id === droppedOnRow.value.object.parent_id)[0];
  }

  let message = "Confirmer le déplacement de \"" + draggedRow.value.object.name + "\" (position " + (draggedRow.value.object.order + 1).toString() + ") vers la position " + (newPos + 1).toString();
  if (parentObject != null) message += " (sous élement de \"" + parentObject.name + "\") ";
  message += "?";
  const confirmSnackbar = new Snackbar().open({
    indefinite: true,
    message: message,
    cancelText: "Annuler",
    actionText: "Confirmer",
    type: "is-warning",
    onAction: () => {
      // Récupérer le type de caractéristiques parent
      const characteristicType = filteredCharacteristicType.value.find((parent: CharacteristicTypeModel) => {
        return parent.characteristic_type_id === draggedRow.value.object.characteristic_type_id;
      })!;

      // Récupére l'élément qu'on drag
      const draggedItem = characteristicType.characteristics.splice(draggedRow.value.index, 1)[0];

      // Gestion du drop en tant que child
      draggedItem.parent_id = (parentObject != null ? parentObject.id : null);

      // Calculer sa nouvelle profondeur
      draggedItem.depth = getDepth(draggedItem, characteristicType.characteristics);

      // Insérer l'élément déplacé à sa nouvelle position
      characteristicType!.characteristics.splice((droppedOnRow.value.dropAsChild ? droppedOnRow.value.index + 1 : droppedOnRow.value.index), 0, draggedItem);

      // Mettre à jour l'ordre dans le tableau
      reOrder(characteristicType.characteristics, characteristicType.characteristics.filter(t => t.parent_id == null));

      // S'il faut  déplacer les enfants, on regénère la totalité du tree
      // if (draggedRow.value.childs.length > 0) prepareFilteredCarac();

      // Réordonner dans la bdd
      reorderCharacteristics(characteristicType, characteristicType.characteristics.map(characteristic => characteristic.id));
      // Mettre-à-jour la caractéristique (peut-être que le parent a changé)
      updateCharacteristic(draggedItem);
    }
  });

  // Récupérer l'événement de fermeture de base en mémoire
  const baseClose = confirmSnackbar.close;

  // Binder l'événement de close custom (avec annulation)
  confirmSnackbar.close = () => {
    // Reset
    draggedRow.value = null;
    droppedOnRow.value = null;
    baseClose();
  };
}

// Trier récursivement les items
function sortItems(items: CharacteristicModel[]): CharacteristicModel[] {
  // Trier les items racines
  const rootItems = items
    .filter(item => item.parent_id === null)
    .sort((a, b) => a.order - b.order);

  const sortedList = [];
  // Pour chaque root item ajouter ses enfants en dessous
  for (const rootItem of rootItems) {
    sortedList.push(rootItem);
    addChildren(items, sortedList, rootItem.id);
  }

  return sortedList;
}

// Obtenir les enfants d'un item donné, dans le bon ordre
function getChildren(items: CharacteristicModel[], parentId: number | null): CharacteristicModel[] {
  if (parentId == null) return [];
  return items
    .filter(item => item.parent_id === parentId)
    .sort((a, b) => a.order - b.order);
}

// Pour ajouter les enfants triés à la liste de façon récursive
function addChildren(items: CharacteristicModel[], sortedList: CharacteristicModel[], parentId: number): void {
  const children = getChildren(items, parentId);
  for (const child of children) {
    sortedList.push(child);
    addChildren(items, sortedList, child.id); // Ajouter les enfants de l'enfant trié
  }
}

// Obtenir les enfants et sous enfants d'un item donné de façon récursive
function getAllChildren(items: CharacteristicModel[], parentId: number | null): CharacteristicModel[] {
  let result: CharacteristicModel[] = [];
  if (parentId == null) return result;

  const children = items.filter(item => item.parent_id === parentId);
  result = children;
  for (const child of children) {
    result.push(...getAllChildren(characteristics.value, child.id));
  }
  return result;
}

//  Ré-ordonner un arbre de façon récursive
function reOrder(refArray: CharacteristicModel[], items: CharacteristicModel[]): void {
  if (items == null || items.length === 0) return;
  items.forEach((child: CharacteristicModel, index: number) => {
    child.order = index;
    reOrder(refArray, refArray.filter(t => t.parent_id === child.id));
  });
}

// Récupérer la profondeur d'un élément
function getDepth(item: CharacteristicModel, items: CharacteristicModel[]): number {
  let depth: number = 0;
  let currentItem: CharacteristicModel | null | undefined = item;
  while (currentItem != null && currentItem.parent_id !== null) {
    depth++;
    currentItem = items.find(item => item.id === currentItem?.parent_id);
  }
  return depth;
}
</script>

<style lang="scss">
@use "~/assets/scss/custom.scss";

// .b-table .table-wrapper {
//   height: 600px;
//   overflow-y: auto;
//   max-height: 25%;
// }
// .element {
//   background-color: $couleur-existante; /* couleur existante */
//   background-color: lighten($couleur-existante, 20%); /* couleur éclaircie */
// }

table tr.is-subheading, table tr.is-subheading th {
  background-color: white !important;
}

table tr.is-selected {
  -webkit-box-shadow: inset 8px 0px 0px 0px var(--primary) !important;
  box-shadow: inset 8px 0px 0px 0px var(--primary) !important;
  font-weight: bold !important;
}

table tr.highlighted {
  //background-color: red !important; /* Changer la couleur de fond */
  /* Autres styles pour indiquer la ligne cible */
  //-webkit-box-shadow: inset 0px 35px 0px -30px  var(--primary)  !important;
  //box-shadow: inset 0px 35px 0px -30px  var(--primary)  !important;
  -webkit-box-shadow: 0px -5px 0px 0px  var(--primary)  !important;
  box-shadow: 0px -5px 0px 0px  var(--primary)  !important;
}

table tr.highlighted-child {
  -webkit-box-shadow: 70px -5px 0px 0px  var(--primary), 0px -5px 0px 0px  var(--primary-light) !important;
  box-shadow: 70px -5px 0px 0px  var(--primary), 0px -5px 0px 0px  var(--primary-light) !important;
}

table{
  // border-collapse: collapse !important;
  border: 1px solid var(--primary) !important;
  border-radius: 4px;
}

table tr:not(.is-selected, .is-subheading):hover {
  /*background-color: var(--primary-light) !important;
  color: whitesmoke !important;*/
  box-shadow: inset 0 0 0 99999px rgba(0,0,0,0.1) !important;
  cursor: pointer !important;
}

.b-table .table-wrapper.has-sticky-header {
  height: 75vh !important;
  overflow-y: auto !important;
}

.dropdown-menu {
  padding-top: 0px !important;
  .dropdown-content {
    padding-top: 0px !important;
    .dropdown-divider {
      margin-top: 0px !important;
    }
  }
}

</style>
