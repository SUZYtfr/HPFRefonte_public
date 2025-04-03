/* eslint-disable @typescript-eslint/no-explicit-any */
/* eslint-disable @typescript-eslint/explicit-function-return-type */

import { useFetch, useNuxtApp, type UseFetchOptions } from "nuxt/app";
import { type ClassConstructor, plainToInstance } from "class-transformer";
import type { Flatten, Depaginate } from "~/types/basics.ts";
import defu from "defu";
import { SnackbarProgrammatic as Snackbar } from "buefy";

export default function useCustomFetch<T>(
  url: string,
  opts: UseFetchOptions<T> = {},
  model?: ClassConstructor<Flatten<Depaginate<T>>>,
) {
  const config = useRuntimeConfig();
  const defaultOptions: UseFetchOptions<T> = {
    headers: {
      Accept: "application/json",
      "Content-type": "application/json",
    },
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    onRequest: ({ request, options }) => {
      const { token } = useAuth();
      if (token.value) options.headers.set("Authorization", token.value);
    },
    onResponseError: ({ response }) => {
      if (import.meta.client) {
        new Snackbar().open({
          duration: 5000,
          message: "Une erreur s'est produite lors de la récupération des données",
          type: "is-danger",
          position: "is-bottom-right",
          actionText: undefined,
          pauseOnHover: true,
          queue: true,
        });
      }
      console.log(`${response.status} ${response.statusText}`);
    },
    timeout: 5000,
    // params: (input) => {
    //     return qs.stringify(input, { arrayFormat: "repeat", skipNulls: true })
    // },
    transform: (input: any) => {
      // Ça va être marrant à typer, input est de types *Data | *Data[] | Paginated<Data[]>, et pas *Model
      if (model) {
        if (input.results) {
          return {
            count: input.count,
            current: input.current,
            results: plainToInstance(model, input.results),
          };
        } else {
          return plainToInstance(model, input);
        }
      } else {
        return input;
      }
    },
    watch: false,
    baseURL: import.meta.client ? config.public.baseApi : config.baseApi,
    $fetch: useNuxtApp().$api as typeof $fetch,
  };
  const defaultedOptions = defu(opts, defaultOptions);
  return useFetch(url, defaultedOptions);
}
