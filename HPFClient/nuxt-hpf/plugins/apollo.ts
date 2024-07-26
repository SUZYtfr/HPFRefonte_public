import type { Plugin } from "@nuxt/types";
import { initializeApollo } from "~/utils/apolloApi";

const accessor: Plugin = (context) => {
    let client = context.app.apolloProvider.defaultClient;
    initializeApollo(client);
};

export default accessor;
