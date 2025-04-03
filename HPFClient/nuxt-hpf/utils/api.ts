import { ClassConstructor } from "class-transformer";
import type { UseFetchOptions } from "nuxt/app";
import useCustomFetch from "~/composables/useCustomFetch";
import type { Flatten, Depaginate } from "~/types/basics";

export class FetchController {
    public async get<T>(url: string, params: any, model?: ClassConstructor<Flatten<Depaginate<T>>>, options?: UseFetchOptions<T>) {
        try {
            return useCustomFetch<T>(
                url,
                {
                    method: "get",
                    params: params,
                    ...options
                },
                model
            )
            } catch (error) {
                console.log(error);
                throw error;
            }
        }

    public async delete<T>(url: string, model?: ClassConstructor<Flatten<Depaginate<T>>>, options?: UseFetchOptions<T>): Promise<any> {
        try {
            return useCustomFetch(
                url,
                {
                    method: "delete",
                    ...options
                }
            );
        } catch (error) {
            console.log(error)
            throw error;
        }
    }

    public async post<T>(url: string, payload: any, model?: ClassConstructor<Flatten<Depaginate<T>>>, options?: UseFetchOptions<T>): Promise<any> {
        try {
            return useCustomFetch(
                url,
                {
                    method: "post",
                    body: payload,
                    ...options
                }
            );
        } catch (error) {
            console.log(error)
            throw error;
        }
    }

    public async put<T>(url: string, payload: any, model?: ClassConstructor<Flatten<Depaginate<T>>>, options?: UseFetchOptions<T>) {
        try {
          return useCustomFetch<T>(
            url,
            {
                method: "put",
                body: payload,
                ...options
            },
            model
            );
        } catch (error) {
            console.log(error)
            throw error;
        }
    }
}

const $fetchController = new FetchController();
export default $fetchController;
