import type { UseFetchOptions } from 'nuxt/app'
import type { ClassConstructor } from "class-transformer";
import { plainToInstance } from 'class-transformer'
import { defu } from 'defu'
import qs from "qs";

export function useCustomFetch<T, U> (url: string | (() => string), options: UseFetchOptions<T> = {}, type?: ClassConstructor<U>) {
  const config = useRuntimeConfig()
  const baseUrl = config.public.apiBase
  
  const defaults: UseFetchOptions<T> = {
    baseURL: baseUrl,
    server: true,
    headers: {
      "Accept": "application/json",
      "Content-type": "application/json",
    },
    timeout: 5000,
    params: (input) => {
      return qs.stringify(input, { arrayFormat: "repeat", skipNulls: true })
    },
    transform: (input) => {
      if (type != null) {
        if (input.results != null) {
          return plainToInstance(type, input.results)
        } else {
          return plainToInstance(type, input)
        }
      } else {
        return input
      }
    }
  }
  const defaultedOptions = defu(options, defaults)

  return useFetch(url, defaultedOptions)
}
