import type { CookieRef } from "#app";
import type { GqlSdkFuncs } from "#gql";
import { jwtDecode, type JwtPayload } from "jwt-decode";

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

interface JWTExtraPayload {
  username: string;
  userId: number;
  isStaff: boolean;
  preferred5Fandoms: number[];
}

interface SignInCredentials {
  username: string;
  password: string;
}

type SessionData = Awaited<ReturnType<GqlSdkFuncs["getSession"]>>;

const loading = ref<boolean>(false);
// const accountData = ref<SessionData["account"] | null>(null);

interface UseCustomAuthReturn {
  token: CookieRef<string | null | undefined>;
  refresh: Ref<string | null>;
  isAuthenticated: ComputedRef<boolean>;
  isStaff: ComputedRef<boolean>;
  loading: Ref<boolean>;
  payloadData: ComputedRef<(JwtPayload & JWTExtraPayload) | null>;
  accountData: Ref<SessionData["account"] | null>;
  data: UseCustomAuthReturn["accountData"];
  signIn: (credentials: SignInCredentials) => Promise<void>;
  signOut: VoidFunction;
}

export function useCustomAuth(): UseCustomAuthReturn {
  const token = useCookie("gql:default");
  const refresh = ref<string | null>(null);
  const payloadData = computed<(JwtPayload & JWTExtraPayload) | null>(() => {
    if (token.value) {
      return jwtDecode<JwtPayload & JWTExtraPayload>(token.value || "", { header: false });
    } else return null;
  });
  const isAuthenticated = computed<boolean>(() => Boolean(token.value));
  const isStaff = computed<boolean>(() => payloadData.value?.isStaff || false);
  const profileCookie = useCookie<SessionData["account"]>("profile");
  const accountData = profileCookie;

  async function signIn(credentials: SignInCredentials): Promise<void> {
    loading.value = true;
    // accountData.value = null;
    useGqlToken(null);

    const { requestToken } = await GqlRequestToken(credentials);
    // TODO gérer les erreurs
    useGqlToken({
      token: requestToken.token,
      config: {
        type: "JWT",
        name: "Authorization",
      },
    });
    await nextTick(getAccountData);
    loading.value = false;
    return;
  }

  async function getAccountData(): Promise<void> {
    if (!isAuthenticated) return;
    const { account } = await GqlGetSession();
    // accountData.value = account;
    const profileCookie = useCookie("profile");
    profileCookie.value = JSON.stringify(account);
    return;
  }

  async function signOut(): Promise<void> {
    loading.value = true;
    useGqlToken(null);
    // accountData.value = null;
    loading.value = false;
    const profileCookie = useCookie("profile");
    profileCookie.value = undefined;
    return;
  }

  return {
    token,
    refresh,
    isAuthenticated,
    isStaff,
    loading,
    payloadData,
    accountData,
    data: accountData,
    signIn,
    signOut,
  };
}
