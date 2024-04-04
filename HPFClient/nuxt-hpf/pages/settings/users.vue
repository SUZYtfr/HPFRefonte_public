<template>
  <div class="container is-fluid">
    <div class="columns">
      <div class="column is-auto">
        <div>
          <b-table
            :data="users"
            :paginated="true"
            :per-page="userFilters.pageSize"
            :current-page.sync="userFilters.page"
            :pagination-simple="false"
            :loading="listLoading"
            :striped="true"
            :hoverable="true"
            sort-icon="chevron-up"
            default-sort="user.first_name"
            aria-next-label="Page suivante"
            aria-previous-label="Page précédente"
            aria-page-label="Page"
            aria-current-label="Page actuelle"
            :debounce-search="1000"
            :selected.sync="selectedUser"
          >
            <!-- UserId -->
            <b-table-column
              field="id"
              label="UserId"
              width="80"
              sortable
              numeric
            >
              <template #subheading>
                <b-input
                  v-model="userFilters.authorId"
                  size="is-small"
                  type="search"
                />
              </template>
              <template #default="props">
                {{ props.row.id }}
              </template>
            </b-table-column>

            <!-- Username -->
            <b-table-column field="username" label="Pseudo" sortable>
              <template #subheading>
                <b-input
                  v-model="userFilters.name"
                  placeholder="Pseudo"
                  size="is-small"
                  type="search"
                  expanded
                />
              </template>
              <template #default="props">
                {{ props.row.username }}
              </template>
            </b-table-column>

            <!-- Email -->
            <b-table-column field="email" label="Email" sortable>
              <template #subheading>
                <b-input
                  v-model="userFilters.email"
                  placeholder="Email"
                  size="is-small"
                  type="search"
                  expanded
                />
              </template>
              <template #default="props">
                {{ props.row.email }}
              </template>
            </b-table-column>

            <!-- Statut du compte -->
            <b-table-column field="status" label="Statut" width="10" sortable>
              <template #subheading>
                <b-select
                  v-model="userFilters.status"
                  placeholder="Statut"
                  icon="sort"
                  size="is-small"
                  type="search"
                >
                  <option value="null">
                    Tous
                  </option>
                  <option value="1">
                    Non validé
                  </option>
                  <option value="2">
                    Validé
                  </option>
                  <option value="3">
                    Modérateur
                  </option>
                  <option value="4">
                    Administrateur
                  </option>
                  <option value="5">
                    Banni
                  </option>
                </b-select>
              </template>
              <template #default="props">
                {{ props.row.status | statusToString }}
              </template>
            </b-table-column>

            <!-- Statut d'adhérent-->
            <b-table-column field="is_premium" label="Adhérent" width="10" sortable centered>
              <template #subheading>
                <b-checkbox
                  v-model="userFilters.premium"
                  type="search"
                  class="mt-1"
                />
              </template>
              <template #default="props">
                <b-checkbox
                  :value="props.row.is_premium"
                  type="is-success"
                  :disabled="true"
                />
              </template>
            </b-table-column>

            <!-- Date d'inscription -->
            <b-table-column field="creation_date" label="Inscription" width="120" sortable centered>
              <template #subheading>
                <b-datepicker
                  v-model="userFilters.creation_date"
                  locale="fr-FR"
                  placeholder="Date d'inscription"
                  append-to-body
                  icon="calendar-alt"
                  :first-day-of-week="1"
                  :icon-right="userFilters.creation_date ? 'times-circle' : ''"
                  :icon-right-clickable="true"
                  size="is-small"
                  @icon-right-click="userFilters.creation_date = null"
                />
              </template>
              <template #default="props">
                {{ props.row.creation_date?.toLocaleDateString() ?? "31/12/1970" }}
              </template>
            </b-table-column>

            <!-- Nombre de publications-->
            <b-table-column field="stats.fiction_count" label="Publications" sortable>
              <template #default="props">
                {{ props.row.stats?.fiction_count }}
              </template>
            </b-table-column>

            <!-- Equipes -->
            <!-- <b-table-column field="team" label="Equipe" sortable>
              <template #subheading>
                <b-dropdown
                  ref="dropdownTeamFilter"
                  v-model="userFilters.team"
                  multiple
                  aria-role="list"
                >
                  <template #trigger>
                    <b-button
                      type="is-primary"
                      icon-right="menu-down"
                      size="is-small"
                    >
                      {{ "Equipes" + (((userFilters.team?.length ?? 0) > 0) ? (" (" + userFilters.team?.length +")") : "") }}
                    </b-button>
                  </template>

                  <b-dropdown-item custom value="1" aria-role="listitem">
                    <b-checkbox @input="$refs.dropdownTeamFilter.selectItem('1')">
                      <span>Sélections</span>
                    </b-checkbox>
                  </b-dropdown-item>
                </b-dropdown>
              </template>
              <template #default="props">
                {{ props.row.team }}
              </template>
            </b-table-column> -->

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
      <div v-if="selectedUser != null" class="column is-narrow">
        <div class="card">
          <header class="card-header sub-title">
            <p class="card-header-title is-centered">
              {{ selectedUser.username }}
            </p>
          </header>
          <div class="card-content px-3 py-3">
            <div class="columns is-vcentered">
              <div class="column is-narrow">
                <figure class="image is-64x64">
                  <img
                    :src="selectedUser.profile?.profile_picture ?? require('@/assets/img/placeholders/64x64.png')"
                  >
                </figure>
                <b-button
                  v-if="(selectedUser.profile?.profile_picture ?? false)"
                  type="is-primary"
                  size="is-small"
                  icon-pack="fas"
                  icon-left="trash-alt"
                  class="trash-image-position"
                  @click="deletePicture()"
                />
              </div>
              <div class="column is-auto">
                <b-field
                  label="Nom d'auteur"
                  label-position="on-border"
                  custom-class="has-text-primary"
                >
                  <b-input
                    v-model="selectedUser.username"
                    type="text"
                    placeholder="Pseudo"
                    required
                    pattern="^[A-Za-z0-9_\- ]{3,30}$"
                    validation-message="Veuillez saisir un nom d'utilisateur compris entre 3 et 30 caractères"
                    :expanded="true"
                  />
                </b-field>
                <b-field
                  label="Statut"
                  label-position="on-border"
                  custom-class="has-text-primary"
                >
                  <b-select
                    v-model="selectedUser.status"
                    placeholder="Statut"
                    icon="sort"
                    type="search"
                    :expanded="true"
                  >
                    <option value="1">
                      Non validé
                    </option>
                    <option value="2">
                      Validé
                    </option>
                    <option value="3">
                      Modérateur
                    </option>
                    <option value="4">
                      Administrateur
                    </option>
                    <option value="5">
                      Banni
                    </option>
                  </b-select>
                </b-field>
              </div>
            </div>

            <div class="is-flex is-flex-direction-row is-align-items-center mb-3">
              <b-field>
                <b-checkbox :value="selectedUser.is_premium">
                  Adhérent
                </b-checkbox>
              </b-field>
              <!-- <b-field>
                <b-dropdown
                  ref="dropdownSelectedUserTeamFilter"
                  v-model="userFilters.team"
                  multiple
                  aria-role="list"
                >
                  <template #trigger>
                    <b-button
                      type="is-primary"
                      icon-right="menu-down"
                      size="is-small"
                    >
                      {{ "Equipes" + (((selectedUser.team?.length ?? 0) > 0) ? (" (" + selectedUser.team?.length +")") : "") }}
                    </b-button>
                  </template>

                  <b-dropdown-item custom value="1" aria-role="listitem">
                    <b-checkbox @input="$refs.dropdownSelectedUserTeamFilter.selectItem('1')">
                      <span>Sélections</span>
                    </b-checkbox>
                  </b-dropdown-item>
                </b-dropdown>
              </b-field> -->
            </div>
            <b-field
              label="Adresse mail"
              label-position="on-border"
              custom-class="has-text-primary"
            >
              <b-input
                v-model="selectedUser.email"
                type="email"
                placeholder="Adresse mail"
                required
                validation-message="L'adresse mail est invalide"
                :expanded="true"
              />
            </b-field>
            <b-button
              :expanded="true"
              label="Envoyer un mail de réinitialisation de mot de passe"
              type="is-primary"
              class="mb-3"
              @click="sendResetPassword()"
            />
            <b-button
              :expanded="true"
              label="Anonymiser ce compte"
              type="is-danger"
              @click="anonymiseUser()"
            />
          </div>
          <footer class="modal-card-foot p-3">
            <b-button
              :disabled="!formIsValid"
              :expanded="true"
              label="Enregistrer"
              type="is-primary"
              :loading="loading"
              @click="updateUser()"
            />
          </footer>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Watch } from "nuxt-property-decorator";
import { SerialiseClass } from "@/serialiser-decorator";
import { UserModel } from "@/models/users";
import { IUserFilters, UserStatus } from "@/types/users";
import { searchUsers } from "@/api/users";
import { SortByEnum } from "~/types/basics";
import { VForm, OpenToast } from "@/utils/formHelper";

@Component({
  name: "SettingsUsers",
  fetchOnServer: true,
  fetchKey: "settings-users",
  filters: {
    statusToString: (number: UserStatus) => {
      let result = "";
      switch (number) {
        case UserStatus.Unvalidated: result = "Non validé"; break;
        case UserStatus.Validated: result = "Validé"; break;
        case UserStatus.Moderator: result = "Modérateur"; break;
        case UserStatus.Administrator: result = "Administrateur"; break;
        case UserStatus.Banned: result = "Banni"; break;
      }
      return result;
    }
  }
})
export default class extends Vue {
  // #region Data
  @SerialiseClass(UserModel)
  public users: UserModel[] = [];

  public listLoading: boolean = false;
  public totalUsers: number = 0;

  public userFilters: IUserFilters = {
    name: null,
    email: null,
    authorId: null,
    status: null,
    premium: null,
    team: null,
    published: null,
    creation_date: null,
    page: 1,
    pageSize: 20,
    totalPages: true,
    sortBy: SortByEnum.Descending,
    sortOn: ""
  };

  public selectedUser: UserModel | null = null;

  public loading: boolean = false;

  private timerId: number = 0;
  // #endregion

  // #region Computed
  get formIsValid(): boolean {
    return (((this.selectedUser?.username?.length ?? 0) > 0) &&
    ((this.selectedUser?.email?.length ?? 0) > 0));
  }

  get form(): VForm {
    return this.$refs.signupForm as VForm;
  }
  // #endregion

  // #region Watchers
  @Watch("userFilters", { deep: true })
  public onFiltersChanged(): void {
    clearTimeout(this.timerId);
    this.timerId = window.setTimeout(this.$fetch, 500);
  }
  // #endregion

  // #region Hooks
  private async fetch(): Promise<void> {
    this.listLoading = true;
    // Récupération des users
    await this.getUsers();
    this.listLoading = false;
  }
  // #endregion

  // #region Methods
  private async getUsers(): Promise<void> {
    try {
      const response = (await searchUsers(this.userFilters));
      this.users = response.results;
      // console.log(this.users);
      // console.log("User: " + (this.users[0] instanceof UserModel));
      this.userFilters.page = response.current;
      this.totalUsers = response.count;
    } catch (error) {
      if (process.client) {
        this.$buefy.snackbar.open({
          duration: 5000,
          message: "Une erreur s'est produite lors de la récupération des utilisateurs",
          type: "is-danger",
          position: "is-bottom-right",
          actionText: null,
          pauseOnHover: true,
          queue: true
        });
      } else {
        console.log(error);
      }
    }
  }

  // Envoyer une demande de renouvellement de mot de passe
  public async sendResetPassword(): Promise<void> {
    try {
      this.loading = true;
      // const data = await signup(this.signupForm);
      OpenToast(
        "Un mail de renouvellement de mot de passe a été envoyé",
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

  // Anonymiser cet utilisateur
  public async anonymiseUser(): Promise<void> {
    // Confirmer l'action
    this.$buefy.snackbar.open({
      indefinite: true,
      message: "Confirmer l'anonymisation ? (action irréversible)",
      cancelText: "Annuler",
      actionText: "Confirmer",
      type: "is-warning",
      onAction: () => {
        try {
          this.loading = true;
          // const data = await signup(this.signupForm);
          OpenToast(
            "L'utilisateur a bien été anonymisé",
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
  }

  // Mettre à jour l'utilisateur
  public async updateUser(): Promise<void> {
    try {
      this.loading = true;
      // const data = await signup(this.signupForm);
      OpenToast(
        "Utilisateur mis à jour",
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

  // Supprimer l'avatar de l'utilisateur
  public deletePicture(): void {
    if (this.selectedUser?.profile != null) this.selectedUser.profile.profile_picture = "";
  }
  // #endregion
}
</script>

<style lang="scss">
@import "~/assets/scss/custom.scss";
.trash-image-position {
  position: absolute;
  margin-left: 17px;
  margin-right: auto;
  margin-top: -16px;
}
</style>
