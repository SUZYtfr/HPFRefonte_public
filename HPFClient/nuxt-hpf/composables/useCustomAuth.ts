import type { SignInFunc, SignOutFunc, SignUpFunc } from '/home/pierre/projects/HPFRefonte/HPFClient/nuxt-hpf/node_modules/@sidebase/nuxt-auth/dist/runtime/composables/local/useAuth';
import type { CommonUseAuthReturn, GetSessionOptions, SecondarySignInOptions, SignOutOptions, SignUpOptions } from '/home/pierre/projects/HPFRefonte/HPFClient/nuxt-hpf/node_modules/@sidebase/nuxt-auth/dist/runtime/types';
import { useAuthState } from '/home/pierre/projects/HPFRefonte/HPFClient/nuxt-hpf/node_modules/@sidebase/nuxt-auth/dist/runtime/composables/local/useAuthState';
import type { RequestTokenMutation } from '#gql';

/*
La version 1.0.0 "stable" de @sidebase/nuxt-auth est sortie récemment.
La roadmap indique des améliorations à venir, notamment la mise en disposition de hooks 
sur la configuration consommant le provider local de JWT, qui permettrait de le faire 
fonctionner avec GraphQL.
En attendant, fait à la va-vite, ce composable permet de patcher pour bénéficier des 
fonctionnalités de sidebase/nuxt-auth (middleware de protection des pages) en intégrant 
les quelques outils de gestion de l'authentification qu'offre nuxt-graphql-client. 
Autre option, se passer entièrement de sidebase/nuxt-auth pour écrire ses propres 
composables et middlewares avec nuxt-graphql-client.
*/

type SessionData = {
    
}

interface Credentials extends Record<string, any> {
  username: string
  password: string
}

export function useCustomAuth() {
    const {
        data,
        status,
        lastRefreshedAt,
        loading,
        token,
        refreshToken,
        rawToken,
        rawRefreshToken,
        _internal
    } = useAuthState();

    async function signIn(
        credentials: Credentials,
        signInOptions?: SecondarySignInOptions,
    ): Promise<RequestTokenMutation> {
        useGqlToken(null);
        const response = await GqlRequestToken(credentials);
        const token = response.requestToken.token;
        rawToken.value = token;
        useGqlToken({
            token: token,
            config: {
                type: 'JWT',
                name: 'Authorization',
            }
        })
        await nextTick(getSession);
        return response;
    }

    async function signOut(signOutOptions?: SignOutOptions): Promise<void> {
        data.value = null
        rawToken.value = null
        rawRefreshToken.value = null
        useGqlToken(null);
        return
    }

    async function getSession(getSessionOptions?: GetSessionOptions): Promise<SessionData | null | void> {
        let tokenValue = token.value
        loading.value = true
        try {
            const result = await GqlGetSession();
            //@ts-ignore
            data.value = result.account
        }
        catch (err) {
            if (!data.value && err instanceof Error) {
                console.error(`Session: unable to extract session, ${err.message}`)
            }
            
            // Clear all data: Request failed so we must not be authenticated
            data.value = null
            rawToken.value = null
            useGqlToken(null);
        }
        loading.value = false
        lastRefreshedAt.value = new Date()
        return data.value
    }

    return {
        status,
        data: readonly(data),
        lastRefreshedAt: readonly(lastRefreshedAt),
        token: readonly(token),
        refreshToken: readonly(refreshToken),
        getSession,
        signIn,
        signOut,
        // signUp,
        // refresh
    }
}

