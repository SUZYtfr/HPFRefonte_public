import type { UserType } from "#gql";


/*
La version 1.0.0 "stable" de @sidebase/nuxt-auth est sortie récemment.
La roadmap indique des améliorations à venir, notamment la mise en disposition de hooks 
sur la configuration consommant le provider local de JWT, qui permettrait de le faire 
fonctionner avec GraphQL.
En attendant, fait à la va-vite, ce composable permet de répliquer grossièrement l'API et 
les fonctionnalités de sidebase/nuxt-auth (middleware de protection des pages) en intégrant 
les quelques outils de gestion de l'authentification qu'offre nuxt-graphql-client. 
Autre option, se passer entièrement de sidebase/nuxt-auth pour écrire ses propres 
composables et middlewares avec nuxt-graphql-client.
*/


const token = ref<String>('');
const refresh = ref<String>('');
const isAuthenticated = computed<Boolean>(() => token.value.length > 0);
const loading = ref<Boolean>(false);
const data = ref<UserType | null>(null);  // TODO
const isStaff = computed<Boolean>(() => data.value?.isStaff || false);  // TODO token claims ou accountData.isStaff?

export function useCustomAuth() {
    async function signIn(credentials: { username: string, password: string }) {
        useGqlToken(null);
        token.value = '';
        data.value = null;

        loading.value = true;
        const { requestToken } = await GqlRequestToken(credentials);
        // TODO gérer les erreurs
        token.value = requestToken.token;
        useGqlToken({
            token: requestToken.token,
            config: {
                type: 'JWT',
                name: 'Authorization',
            }
        })
        await nextTick(getAccountData);
        loading.value = false;
        // TODO return value?
    }

    async function getAccountData() {
        if(!isAuthenticated) {
            throw 'Pas authentifié'
        }
        const { account } = await GqlGetSession();
        //@ts-ignore
        data.value = account;
        return account;
    }

    async function signOut() {
        useGqlToken(null);
        token.value = '';
        data.value = null;
    }

    return {
        token,
        refresh,
        isAuthenticated,
        data,
        isStaff,
        loading,
        signIn,
        signOut,
        getAccountData,
    }
}
