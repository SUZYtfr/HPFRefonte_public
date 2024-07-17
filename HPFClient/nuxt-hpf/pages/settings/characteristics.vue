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
            ref="carac_table"
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
            :selected.sync="selectedItem"
            :show-detail-icon="true"
            :sticky-header="true"
            :row-class="(row, index) => getTableParentRowClass(row, index)"
            @click.native="onRowClickNative($event)"
          >
            <!-- Libelle -->
            <b-table-column
              field="name"
              label="Libellé"
            >
              <template #subheading>
                <b-input
                  v-model="caracFilter"
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
            <template slot="detail" slot-scope="props">
              <tr
                v-for="(item, index) in props.row.characteristics"
                :key="item.id"
                :ref="'child_row_' + item.id.toString()"
                :class="[((index % 2 == 0) ? getCaracteristicTypeColorLight(item.characteristic_type_id) : getCaracteristicTypeColorLighter(item.characteristic_type_id)),
                         { 'highlighted': (item.characteristic_type_id === (droppedOnRow?.object?.characteristic_type_id ?? -1) && index === (droppedOnRow?.index ?? -1) && (droppedOnRow?.dropAsChild ?? false) === false) },
                         { 'highlighted-child': (item.characteristic_type_id === (droppedOnRow?.object?.characteristic_type_id ?? -1) && index === (droppedOnRow?.index ?? -1) && (droppedOnRow?.dropAsChild ?? false) === true) }]"
                :selected="selectedItem"
                draggable="true"
                @click="onChildRowClicked(item, $event)"
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

<script lang="ts">
import { Component, Vue, Watch } from "nuxt-property-decorator";
import { getModule } from "vuex-module-decorators";
import { SerialiseClass } from "@/serialiser-decorator";
import { VForm, OpenToast } from "@/utils/formHelper";
import Config from "~/store/modules/Config";
import { CharacteristicModel, CharacteristicTypeModel } from "~/models/characteristics";
import { getCaracteristicTypeColor, getCaracteristicTypeColorLight, getCaracteristicTypeColorLighter } from "@/utils/characteristics";
import { getCharacteristics, getCharacteristicsTypes, updateCharacteristic, updateCharacteristicsType, deleteCharacteristic, createCharacteristic } from "~/api/characteristics";

@Component({
  name: "SettingsCharateristics",
  fetchOnServer: true,
  fetchKey: "settings-charateristics"
})
export default class extends Vue {
  // #region Data
  @SerialiseClass(CharacteristicModel)
  private characteristics: CharacteristicModel[] = [];

  @SerialiseClass(CharacteristicTypeModel)
  public characteristics_types: CharacteristicTypeModel[] = [];

  // Caractéristiques filtrées
  public filteredCharacteristicType: CharacteristicTypeModel[] = [];

  public listLoading: boolean = false;
  public totalUsers: number = 0;

  public selectedItem: CharacteristicModel | CharacteristicTypeModel | null = null;

  public loading: boolean = false;

  private timerId: number = 0;

  public maxOccurenceEnable: boolean = false;

  public caracFilter: string | null = null;

  // Ligne en cours de déplacement
  private draggedRow: any = {
    target: null,
    object: null,
    index: null,
    childs: []
  };

  // Ligne sur laquelle on drop
  public droppedOnRow: any = {
    target: null,
    object: null,
    index: null,
    dropAsChild: false
  };
  // #endregion

  // #region Computed
  get formIsValid(): boolean {
    if (this.selectedItem == null) return false;
    return true;
    // return (((this.selectedUser.username?.length ?? 0) > 0) &&
    //   ((this.selectedUser.email?.length ?? 0) > 0) &&
    //   ((this.selectedUser.status === UserStatus.Banned && this.selectedUser.ban_reason.length > 0) || this.selectedUser.status !== UserStatus.Banned));
  }

  get form(): VForm {
    return this.$refs.signupForm as VForm;
  }

  get ConfigModule(): Config {
    return getModule(Config, this.$store);
  }

  // #endregion

  // #region Watchers
  @Watch("maxOccurenceEnable")
  public onMaxOccurenceEnabledChanged(): void {
    if (this.selectedItem == null || (this.selectedItem instanceof CharacteristicTypeModel) === false) return;
    if (this.maxOccurenceEnable) (this.selectedItem as CharacteristicTypeModel).max_occurence = 0;
    else (this.selectedItem as CharacteristicTypeModel).max_occurence = null;
  }

  @Watch("caracFilter")
  public onFiltersChanged(): void {
    clearTimeout(this.timerId);
    this.timerId = window.setTimeout(this.prepareFilteredCarac, 500);
  }
  // #endregion

  // #region Hooks
  private mounted(): void {
    this.caracFilter = null;
    this.caracFilter = "";
  }

  private async fetch(): Promise<void> {
    this.listLoading = true;
    // Récupération des caractéristiques
    await this.getCharacteristics();
    this.listLoading = false;
  }
  // #endregion

  // #region Methods
  public getCaracteristicTypeColor(characteristic_type_id: number): string {
    return getCaracteristicTypeColor(characteristic_type_id);
  }

  public getCaracteristicTypeColorLight(characteristic_type_id: number): string {
    return getCaracteristicTypeColorLight(characteristic_type_id);
  }

  public getCaracteristicTypeColorLighter(characteristic_type_id: number): string {
    return getCaracteristicTypeColorLighter(characteristic_type_id);
  }

  private async getCharacteristics(): Promise<void> {
    this.characteristics = (await getCharacteristics(null));
    this.characteristics_types = (await getCharacteristicsTypes());
    this.characteristics_types.forEach((parent: CharacteristicTypeModel) => {
      parent.characteristics = this.characteristics.filter((item: CharacteristicModel) => {
        return item.characteristic_type_id === parent.id;
      });
    });
  }

  // private async getUsers(): Promise<void> {
  //   try {
  //     const response = (await searchUsers(this.userFilters));
  //     this.users = response.results;
  //     // console.log(this.users);
  //     // console.log("User: " + (this.users[0] instanceof UserModel));
  //     this.userFilters.page = response.current;
  //     this.totalUsers = response.count;
  //   } catch (error) {
  //     if (process.client) {
  //       this.$buefy.snackbar.open({
  //         duration: 5000,
  //         message: "Une erreur s'est produite lors de la récupération des utilisateurs",
  //         type: "is-danger",
  //         position: "is-bottom-right",
  //         actionText: null,
  //         pauseOnHover: true,
  //         queue: true
  //       });
  //     } else {
  //       console.log(error);
  //     }
  //   }
  // }

  // Mettre à jour la caratéristique
  public async updateItem(): Promise<void> {
    try {
      this.loading = true;
      if (this.selectedItem instanceof CharacteristicModel) {
        if (this.selectedItem.characteristic_id > 0) {
          updateCharacteristic(this.selectedItem);
        } else {
          createCharacteristic(this.selectedItem);
        }
      } else if (this.selectedItem instanceof CharacteristicTypeModel) {
        if (this.selectedItem.characteristic_type_id > 0) {
          updateCharacteristicsType(this.selectedItem as CharacteristicTypeModel);
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
      this.loading = false;
    }
  }

  public async deleteItem(): Promise<void> {
    if (this.selectedItem === null) return;

    // Confirmer l'action (seulement si ce n'est pas un nouvel item)
    if (this.selectedItem.id > 0) {
      this.$buefy.snackbar.open({
        indefinite: true,
        message: "Confirmer la suppression ? (action irréversible)",
        cancelText: "Annuler",
        actionText: "Confirmer",
        type: "is-warning",
        onAction: () => {
          try {
            this.loading = true;
            if (this.selectedItem instanceof CharacteristicModel) {
              deleteCharacteristic(this.selectedItem);
            }
            this.selectedItem = null;
            this.characteristics = this.characteristics.filter((item: CharacteristicModel) => item.id !== 0);
            this.prepareFilteredCarac();
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
            this.loading = false;
          }
        }
      });
    } else {
      this.selectedItem = null;
      this.characteristics = this.characteristics.filter((item: CharacteristicModel) => item.id !== 0);
      this.prepareFilteredCarac();
    }
  }

  // Construire les caractéristiques affichées (éventuellement filtrées)
  private prepareFilteredCarac(): void {
    // On récupère les caractéristiques qui correspondent au filtre
    const filteredCharacteristics = this.characteristics.filter((child: CharacteristicModel) => {
      return child.name.toUpperCase().includes((this.caracFilter?.toUpperCase() ?? ""));
    });

    // On récupère les caractétistiques types qui correspondent
    const caracTypeIds = filteredCharacteristics.map(({ characteristic_type_id }) => characteristic_type_id);
    const filteredCharacteristicsTypes = this.characteristics_types.filter((item: CharacteristicTypeModel) => {
      return caracTypeIds.includes(item.id);
    });

    // On récupère l'arborescence complète
    filteredCharacteristics.forEach((item: CharacteristicModel) => {
      if (item.parent_id != null && filteredCharacteristics.find((parent: CharacteristicModel) => parent.id === item.parent_id) == null) {
        const missingParent = this.characteristics.filter((parent: CharacteristicModel) => {
          return parent.id === item.parent_id;
        });
        filteredCharacteristics.push(...missingParent);
      }
    });

    // Calculer la profondeur de chaque élément
    filteredCharacteristics.forEach((item) => {
      item.depth = this.getDepth(item, filteredCharacteristics);
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
      parent.characteristics = this.sortItems(parent.characteristics);
    });
    this.filteredCharacteristicType = filteredCharacteristicsTypes;
  }

  // Préparer le style des lignes parent du tableau
  public getTableParentRowClass(row: object, index: number): string {
    let style = "";
    if (row instanceof CharacteristicTypeModel) style += getCaracteristicTypeColor(row.id);
    return style;
  }

  // Gestion de la ligne sélectionnée (pour les lignes enfant)
  public onChildRowClicked(item: any, event: any): void {
    this.selectedItem = item;
  }

  // Gestion du style sélection des colonnes
  public onRowClickNative(event: any):void {
    if (event.target.nodeName.toLowerCase() !== "td" && event.target.nodeName.toLowerCase() !== "tr") return;
    (this.$refs.carac_table as any).$el.querySelectorAll("tr").forEach((row: HTMLElement) => {
      row.classList.remove("is-selected");
    });
    if (event.target.nodeName.toLowerCase() === "td") event.target.parentElement.classList.add("is-selected");
    else event.target.classList.add("is-selected");
  }

  // Ajout d'une nouvelle caractéristique
  public onNewCarac(caracteristicType: CharacteristicTypeModel): void {
    // Enlever les précédents nouveaux items non poussés
    this.characteristics = this.characteristics.filter((item: CharacteristicModel) => item.id !== 0);

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
    this.characteristics.push(newItem);

    this.prepareFilteredCarac();
    // // Reset les éventuels filtres
    // if ((this.caracFilter?.length ?? 0) > 0) this.caracFilter = null;

    // Expand la caractéristique type parent
    const caracType = this.filteredCharacteristicType.filter((item: CharacteristicTypeModel) => {
      return item.id === newItem.characteristic_type_id;
    });
    (this.$refs.carac_table as any).openDetailRow(caracType[0]);

    // Après l'ajout dans le dom, afficher et cliquer sur le nouvel élément
    this.$nextTick(() => {
      const newTableRow = (this.$refs["child_row_" + newItem.id.toString()] as any);
      newTableRow[0].scrollIntoView({ behavior: "smooth" });
      newTableRow[0].click();
      newTableRow[0].classList.add("animate__animated", "animate__flash");
    });
  }

  // A l'ouverture du dropdown, reset les filtres éventuels
  public onDropdownToggled(active: boolean): void {
    if (active && ((this.caracFilter?.length ?? 0) > 0)) this.caracFilter = null;
  }

  // Démarrer le déplacement d'une ligne enfant
  public dragstart(row: CharacteristicModel, index: number, e: DragEvent):void {
    // Avant un drag, reset les filtres éventuels
    if (((this.caracFilter?.length ?? 0) > 0)) {
      this.caracFilter = null;
      e.preventDefault();
      return;
    }

    // Impossible de drag une carac non commitée (nouvel item)
    if (row.id === 0) {
      e.preventDefault();
      return;
    }

    // Enlever les précédentes marques de sélection
    (this.$refs.carac_table as any).$el.querySelectorAll("tr").forEach((row: HTMLElement) => {
      row.classList.remove("is-selected");
    });
    this.selectedItem = null;

    // Récupérer en mémoire l'élément qu'on déplace
    this.draggedRow = { target: e.target, object: row, index: index, childs: this.getAllChildren(this.characteristics, row.id).map(item => item.id) };

    // Mise en évidence de l'élément qu'on déplace
    this.draggedRow.target.classList.add("is-selected");
  }

  // Comportement lors du déplacement d'une ligne
  public dragover(row: CharacteristicModel, index: number, e: DragEvent):void {
    e.preventDefault();
    if (e.target == null || e.dataTransfer == null) return;
    if ((this.droppedOnRow?.index ?? -1) === index && (this.droppedOnRow?.dropAsChild ?? false) === e.shiftKey) return;

    // On ne peut pas bouger une carac en dehors de son parent ni bouger un parent dans un enfant
    if (row.characteristic_type_id !== this.draggedRow.object.characteristic_type_id ||
      this.draggedRow.childs.includes(row.id)
    ) {
      this.droppedOnRow = null;
      e.dataTransfer.dropEffect = "none";
    } else {
      this.droppedOnRow = { target: e.target, object: row, index: index, dropAsChild: e.shiftKey };
      e.dataTransfer.dropEffect = "move";
    }
  }

  // Après un glisser déposer d'un élément
  public drop(row: CharacteristicModel, index: number, e: DragEvent):void {
    // Vérifications de base
    if (this.droppedOnRow == null || // Impossible si pas de cible
      row.id === 0 || // Impossible de drop une carac non commitée (nouvel item)
      this.draggedRow.index === this.droppedOnRow.index // Pas de mouvement
    ) {
      e.preventDefault();

      // Reset
      this.draggedRow = null;
      this.droppedOnRow = null;
      return;
    }

    // Demander une confirmation après drop pour valider le changement d'ordre
    let parentObject: CharacteristicModel | null = null;
    let newPos = this.droppedOnRow.object.order;
    if (this.droppedOnRow.dropAsChild) {
      parentObject = this.droppedOnRow.object;
      newPos = 0;
    } else if (this.droppedOnRow.object.parent_id != null) {
      parentObject = this.characteristics.filter(item => item.id === this.droppedOnRow.object.parent_id)[0];
    }

    let message = "Confirmer le déplacement de \"" + this.draggedRow.object.name + "\" (position " + (this.draggedRow.object.order + 1).toString() + ") vers la position " + (newPos + 1).toString();
    if (parentObject != null) message += " (sous élement de \"" + parentObject.name + "\") ";
    message += "?";
    const confirmSnackbar = this.$buefy.snackbar.open({
      indefinite: true,
      message: message,
      cancelText: "Annuler",
      actionText: "Confirmer",
      type: "is-warning"
    });

    // Récupérer l'événement de fermeture de base en mémoire
    const baseClose = confirmSnackbar.close;

    // Binder l'événement de close custom (avec annulation)
    confirmSnackbar.close = () => {
      // Reset
      this.draggedRow = null;
      this.droppedOnRow = null;
      baseClose();
    };

    // Binder l'événement d'action
    confirmSnackbar.onAction = () => {
      // Récupérer le parent
      const parent = this.filteredCharacteristicType.filter((parent: CharacteristicTypeModel) => {
        return parent.characteristic_type_id === this.draggedRow.object.characteristic_type_id;
      });

      // Récupére l'élément qu'on drag
      const draggedItem = parent[0].characteristics.splice(this.draggedRow.index, 1)[0];

      // Gestion du drop en tant que child
      draggedItem.parent_id = (parentObject != null ? parentObject.id : null);

      // Calculer sa nouvelle profondeur
      draggedItem.depth = this.getDepth(draggedItem, parent[0].characteristics);

      // Insérer l'élément déplacé à sa nouvelle position
      parent[0].characteristics.splice((this.droppedOnRow.dropAsChild ? this.droppedOnRow.index + 1 : this.droppedOnRow.index), 0, draggedItem);

      // Mettre à jour l'ordre dans le tableau
      this.reOrder(parent[0].characteristics, parent[0].characteristics.filter(t => t.parent_id == null));

      // S'il faut  déplacer les enfants, on regénère la totalité du tree
      if (this.draggedRow.childs.length > 0) this.prepareFilteredCarac();

      // Mettre à jour l'élément en base
      this.updateItem();
    };
  }

  // public test():void {
  //   const t = this.characteristics.filter((item: CharacteristicModel) => {
  //     return item.parent_id !== null;
  //   });
  //   console.log(t);
  // }

  // Trier récursivement les items
  private sortItems(items: CharacteristicModel[]) : CharacteristicModel[] {
    // Trier les items racines
    const rootItems = items
      .filter(item => item.parent_id === null)
      .sort((a, b) => a.order - b.order);

    const sortedList = [];
    // Pour chaque root item ajouter ses enfants en dessous
    for (const rootItem of rootItems) {
      sortedList.push(rootItem);
      this.addChildren(items, sortedList, rootItem.id);
    }

    return sortedList;
  }

  // Obtenir les enfants d'un item donné, dans le bon ordre
  private getChildren(items: CharacteristicModel[], parentId: number | null): CharacteristicModel[] {
    if (parentId == null) return [];
    return items
      .filter(item => item.parent_id === parentId)
      .sort((a, b) => a.order - b.order);
  }

  // Pour ajouter les enfants triés à la liste de façon récursive
  private addChildren(items: CharacteristicModel[], sortedList: CharacteristicModel[], parentId: number): void {
    const children = this.getChildren(items, parentId);
    for (const child of children) {
      sortedList.push(child);
      this.addChildren(items, sortedList, child.id); // Ajouter les enfants de l'enfant trié
    }
  }

  // Obtenir les enfants et sous enfants d'un item donné de façon récursive
  private getAllChildren(items: CharacteristicModel[], parentId: number | null): CharacteristicModel[] {
    let result: CharacteristicModel[] = [];
    if (parentId == null) return result;

    const children = items.filter(item => item.parent_id === parentId);
    result = children;
    for (const child of children) {
      result.push(...this.getAllChildren(this.characteristics, child.id));
    }
    return result;
  }

  //  Ré-ordonner un arbre de façon récursive
  private reOrder(refArray: CharacteristicModel[], items: CharacteristicModel[]): void {
    if (items == null || items.length === 0) return;
    items.forEach((child: CharacteristicModel, index: number) => {
      child.order = index;
      this.reOrder(refArray, refArray.filter(t => t.parent_id === child.id));
    });
  }

  // Récupérer la profondeur d'un élément
  private getDepth(item: CharacteristicModel, items: CharacteristicModel[]): number {
    let depth: number = 0;
    let currentItem: CharacteristicModel | null | undefined = item;
    while (currentItem != null && currentItem.parent_id !== null) {
      depth++;
      currentItem = items.find(item => item.id === currentItem?.parent_id);
    }
    return depth;
  }
  // #endregion
}
</script>

<style lang="scss">
@import "~/assets/scss/custom.scss";

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
  -webkit-box-shadow: inset 8px 0px 0px 0px $primary !important;
  box-shadow: inset 8px 0px 0px 0px $primary !important;
  font-weight: bold !important;
}

table tr.highlighted {
  //background-color: red !important; /* Changer la couleur de fond */
  /* Autres styles pour indiquer la ligne cible */
  //-webkit-box-shadow: inset 0px 35px 0px -30px  $primary  !important;
  //box-shadow: inset 0px 35px 0px -30px  $primary  !important;
  -webkit-box-shadow: 0px -5px 0px 0px  $primary  !important;
  box-shadow: 0px -5px 0px 0px  $primary  !important;
}

table tr.highlighted-child {
  -webkit-box-shadow: 70px -5px 0px 0px  $primary, 0px -5px 0px 0px  $primary-light !important;
  box-shadow: 70px -5px 0px 0px  $primary, 0px -5px 0px 0px  $primary-light !important;
}

table{
  // border-collapse: collapse !important;
  border: 1px solid $primary !important;
  border-radius: 4px;
}

table tr:not(.is-selected, .is-subheading):hover {
  /*background-color: $primary-light !important;
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
