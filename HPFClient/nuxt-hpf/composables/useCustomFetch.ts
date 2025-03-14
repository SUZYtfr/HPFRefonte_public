import type { UseFetchOptions } from "nuxt/app";
import { ClassConstructor, plainToInstance } from "class-transformer";
import type { Flatten, Depaginate } from "~/types/basics"
import defu from "defu";

export default function useCustomFetch<T>(url: string, opts: UseFetchOptions<T> = {}, model?: ClassConstructor<Flatten<Depaginate<T>>>) {  
    const defaultOptions: UseFetchOptions<T> = {
        headers: {
            "Accept": "application/json",
            "Content-type": "application/json",
        },
        timeout: 5000,
        // params: (input) => {
        //     return qs.stringify(input, { arrayFormat: "repeat", skipNulls: true })
        // },
        transform: (input: any) => {  // Ça va être marrant à typer, input est de types *Data | *Data[] | Paginated<Data[]>, et pas *Model
            if (model) {
                if (input.results) {
                    return {
                        count: input.count,
                        current: input.current,
                        results: plainToInstance(model, input.results)
                    }
                }
                else {
                    return plainToInstance(model, input);
                } 
            }
            else {
                return input
            }
        },
        watch: false,
        baseURL: "http://localhost:8585/api",
        $fetch: useNuxtApp().$api as typeof $fetch
    };

    const defaultedOptions = defu(opts, defaultOptions);
    return useFetch(url, defaultedOptions)
};
