/* eslint-disable @typescript-eslint/no-explicit-any */
// https://nuxt-graphql-client.web.app/getting-started/composables#usegqlerror

export default defineNuxtPlugin(() => {
  useGqlError((err: any) => {
    /*     
    // Only log during development
    if (process.env.NODE_ENV !== "production") {
      for (const gqlError of err.gqlErrors) {
        console.error("[nuxt-graphql-client] [GraphQL error]", {
          client: err.client,
          statusCode: err.statusCode,
          operationType: err.operationType,
          operationName: err.operationName,
          gqlError
        });
      }
    }

    // Handle different error cases
    const tokenExpired = err.gqlErrors.some(e => e.message.includes("id-token-expired"));
    const tokenRevoked = err.gqlErrors.some(e => e.message.includes("id-token-revoked"));
    const unauthorized = err.gqlErrors.some(e => e.message.includes("invalid-claims") || e.message.includes("insufficient-permission"));
    */

    // TODO si jeton invalide
    // TODO proposer la reconnexion
    // TODO retenter l'action
    if (process.env.NODE_ENV === "development") {
      console.log(err.gqlErrors);
    }
    // useGqlToken(null, { "refreshData": true});
    useGqlToken(null);
    return navigateTo("/");
  });
});
