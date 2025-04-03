<template>
  <div class="container is-fluid">
    <div class="columns">
      <div class="column is-auto">
        <div style="/*height: 100%;*/">
          <b-table
            :data="paginatedUsers?.results ?? []"
            :paginated="true"
            :backend-pagination="true"
            :backend-sorting="true"
            :total="totalUsers"
            :per-page="userFilters.pageSize"
            :current-page="userFilters.page"
            :pagination-simple="false"
            :loading="listStatus === 'pending'"
            :striped="true"
            :hoverable="true"
            sort-icon="chevron-up"
            default-sort="user.first_name"
            aria-next-label="Page suivante"
            aria-previous-label="Page précédente"
            aria-page-label="Page"
            aria-current-label="Page actuelle"
            :debounce-search="1000"
            :selected="selectedUser"
            @click="(user: UserModel) => selectedUser = user"
            @pageChange="(page: number) => userFilters.page = page"
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
                  v-model="userFilters.id"
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
                  v-model="userFilters.username"
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
            <b-table-column field="status" label="Statut" width="150" sortable>
              <template #subheading>
                <b-select
                  v-model="userFilters.status"
                  placeholder="Statut"
                  icon="sort"
                  size="is-small"
                  type="search"
                >
                  <option value="">
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
                {{ statusToString(props.row.status) }}
              </template>
            </b-table-column>

            <!-- Statut d'adhérent-->
            <b-table-column field="is_premium" label="Adhérent" width="50" centered>
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
            <div class="columns is-vcentered mb-0">
              <div class="column is-narrow">
                <figure class="image is-64x64">
                  <img
                    :src="selectedUser.profile?.profile_picture ?? 'https://bulma.io/assets/images/placeholders/64x64.png'"
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
                    <option :value="1">
                      Non validé
                    </option>
                    <option :value="2">
                      Validé
                    </option>
                    <option :value="3">
                      Modérateur
                    </option>
                    <option :value="4">
                      Administrateur
                    </option>
                    <option :value="5">
                      Banni
                    </option>
                  </b-select>
                </b-field>
              </div>
            </div>

            <b-field
              v-if="selectedUser.status == UserStatus.Banned"
              label="Raison bannissement"
              label-position="on-border"
              custom-class="has-text-primary"
            >
              <b-input
                v-model="selectedUser.ban_reason"
                type="textarea"
                placeholder="Raison du bannissement"
                required
                maxlength="200"
              />
            </b-field>

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
            <div class="is-flex is-flex-direction-row is-align-items-center is-align-content-space-between">
              <b-button
                :expanded="true"
                label="Anonymiser ce compte"
                type="is-danger"
                @click="anonymiseUser2()"
              />
              <b-tooltip
                position="is-left"
                type="is-primary"
                append-to-body
                multilined
              >
                <b-icon
                  pack="fas"
                  class="is-clickable"
                  type="is-primary"
                  icon="question-circle"
                />
                <template #content>
                  <p>
                    Anonymiser l'utilisateur, ses fictions, séries, reviews, commmentaires.
                  </p>
                  <p>
                    <strong class="has-text-white">Action irréversible.</strong>
                  </p>
                </template>
              </b-tooltip>
            </div>
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

<script setup lang="ts">
import { UserModel } from "@/models/users";
import { IUserFilters, UserStatus } from "@/types/users";
import { searchUsers, putUser, anonymiseUser, sendPasswordResetEmail } from "@/api/private/users";
import { SortByEnum } from "~/types/basics";
import { Field, SnackbarProgrammatic as Snackbar } from "buefy";

function statusToString(statusNumber: UserStatus) {
  let result = "";
  switch (statusNumber) {
    case UserStatus.Unvalidated: result = "Non validé"; break;
    case UserStatus.Validated: result = "Validé"; break;
    case UserStatus.Moderator: result = "Modérateur"; break;
    case UserStatus.Administrator: result = "Administrateur"; break;
    case UserStatus.Banned: result = "Banni"; break;
  }
  return result;
}

// TODO Gérer le multi-sort (frontend + backend)
// utiliser b-table@sort
const userFilters = reactive<IUserFilters>({
  username: null,
  email: null,
  id: null,
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
});

const { data: paginatedUsers, status: listStatus, execute } = await searchUsers(userFilters);
watch(paginatedUsers, () => {
  userFilters.page = paginatedUsers.value?.current ?? 1
});
const totalUsers = computed(() => paginatedUsers.value?.count ?? 0)

// selected.sync n'est pas compatible avec Vue 3
// https://github.com/buefy/buefy/issues/3099
// à la place, simple v-model + onClick
const selectedUser = ref<UserModel | null>(null);

const loading = ref<boolean>(false);

let timerId: number = 0;

const formIsValid = computed<boolean>(() => {
  if (selectedUser.value == null) return false;

  return (((selectedUser.value.username?.length ?? 0) > 0) &&
  ((selectedUser.value.email?.length ?? 0) > 0) &&
  ((selectedUser.value.status === UserStatus.Banned && selectedUser.value.ban_reason.length > 0) || selectedUser.value.status !== UserStatus.Banned));
})

watch(userFilters, () => {
  clearTimeout(timerId);
  timerId = window.setTimeout(execute, 500);
}, {
  deep: true,
});

// Envoyer une demande de renouvellement de mot de passe
async function sendResetPassword(): Promise<void> {
  try {
    loading.value = true;
    if(selectedUser.value) {
      await sendPasswordResetEmail(selectedUser.value.user_id, {
        onResponse: () => {
          OpenToast(
            "Un mail de renouvellement de mot de passe a été envoyé",
            "is-primary",
            5000,
            false,
            true,
            "is-bottom"
          );
        },
        onResponseError: () => {
          OpenToast("Erreur", "is-danger", 5000, false, true, "is-bottom");
        },
      });
    }
    else { throw "Erreur"; }
  } catch (exception) {
  } finally {
    loading.value = false;
  }
}

// Anonymiser cet utilisateur
async function anonymiseUser2(): Promise<void> {
  // Confirmer l'action
  new Snackbar().open({
    indefinite: true,
    message: "Confirmer l'anonymisation ? (action irréversible)",
    cancelText: "Annuler",
    actionText: "Confirmer",
    type: "is-warning",
    onAction: async () => {
      try {
        loading.value = true;
        if(selectedUser.value) {
          await anonymiseUser(selectedUser.value.user_id, {
            onResponse: () => {
              OpenToast(
                "L'utilisateur a bien été anonymisé", "is-primary", 5000, false, true, "is-bottom");
            },
            onResponseError: () => {
              OpenToast("Erreur", "is-danger", 5000, false, true, "is-bottom");
            }
          });
        }
        else { throw "Erreur"; }
      } catch (exception) {
      } finally {
        loading.value = false;
      }
    }
  });
}

// Mettre à jour l'utilisateur - la nouvelle méthode
// FIXME Ceci ne fonctionne pas ! selectedUser.value.id doit être défini au moment de l'appel à putUser (pas execute)
// Sinon il faudrait cette syntaxe : useFetch(() => { $fetch })
// TODO réécrire le FetchController pour utiliser cette syntaxer (optionnelle ?)
// TODO passer les toasts (succès / échec) comme paramtères
// const { status: userUpdateStatus, execute: doUpdateUser } = await putUser(selectedUser.value?.id, selectedUser.value, { immediate: false });
// const loading = computed(() => {
//   userUpdateStatus.value === 'pending'  // TODO ou les autres
// });

// Mettre à jour l'utilisateur - l'ancienne méthode
async function updateUser(): Promise<void> {
  try {
    loading.value = true;
    if(selectedUser.value) {
      await putUser(selectedUser.value?.id, selectedUser.value,
        {
          onResponse: () => {
            OpenToast("Utilisateur mis à jour", "is-primary", 5000, false, true, "is-bottom");
          },
          onResponseError: () => {
            OpenToast("Erreur", "is-danger", 5000, false, true, "is-bottom");
          }
        }
      );
    }
    else { throw "Erreur"; }
  } catch (exception) {
    // Les toasts (réussite / échec) sont envoyés comme paramètres au client
    // Quels sont les scénarios où une erreur atteint cet endroit et que faire ?
  } finally {
    loading.value = false;
  }
}

// Supprimer l'avatar de l'utilisateur
function deletePicture(): void {
  if (selectedUser.value?.profile != null) selectedUser.value.profile.profile_picture = "";
}
</script>

<style lang="scss">
@use "~/assets/scss/custom.scss";
.trash-image-position {
  position: absolute;
  margin-left: 17px;
  margin-right: auto;
  margin-top: -16px;
}
</style>
