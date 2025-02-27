import type { NuxtAxiosInstance } from "@nuxtjs/axios";
import type { ClassConstructor } from "class-transformer";
import { plainToInstance } from "class-transformer";
import { AxiosError } from "axios";
import qs from "qs";

let $axios: NuxtAxiosInstance;

export function initializeAxios(axiosInstance: NuxtAxiosInstance): void {
  $axios = axiosInstance;
  $axios.create({
    baseURL: process.env.SERVER_BASE_API,
    timeout: 5000,
    withCredentials: (process.env.NODE_ENV === "production")
  });
  // Header spécifique à ngrok à commenter quand on est sur python anywhere
  // $axios.defaults.headers.common["ngrok-skip-browser-warning"] = "1";
  $axios.defaults.paramsSerializer = params => qs.stringify(params, { arrayFormat: "repeat", skipNulls: true });

  $axios.interceptors.request.use((request) => {
    // console.log("Starting Request", JSON.stringify(request, null, 2));
    return request;
  });

  $axios.interceptors.response.use((response) => {
    // console.log("Response:", JSON.stringify(response, null, 2));
    return response;
  });
}

// Est-ce qu'on a vraiment besoin de ça ?
export interface ListResponseWrapper<T> {
  items: T[];
  count: number;
  next: string | null;
  previous: string | null;
  current: number;
}

export { $axios };

export class AxiosWrapper {
  /**
   * Get axios instance if additional configuration is needed
   */
  get axiosInstance(): NuxtAxiosInstance { return $axios; }

  /**
   * HTTP GET request
   * Returns Promise
   * @param url String representation of url
   * @param type Typescript class type. Optional.
   * @param useConstructor boolean (default false). Indicates if we want to use class constructor (true) or use default constructor (false). Optional.
   * @param config AxiosRequestConfig. Additional axios configuration. Optional.
   */
  public async get<T>(url: string, params: any, type?: (new (arg: any) => T)/* , useConstructor?: boolean */): Promise<any> {
    if (type) {
      try {
        let { data } = await $axios.request({
          url: url,
          method: "get",
          params: params
        });
        // Transformer en instance
        if (data.results != null) {
          // Contenu paginé
          if (data.results.length > 0) {
            data.results = this.parseData2(type, data.results);
          }
        } else if (data != null) {
          // Contenu unique
          data = this.parseData2(type, data);
        }
        return data;
      } catch (error) {
        throw new Error((error as AxiosError).response?.data ?? (error as Error).message);
      }
    } else {
      // if there is no type, return axios default behavior
      try {
        return $axios.get(url);
      } catch (error) {
        throw new Error((error as AxiosError).response?.data ?? (error as Error).message);
      }
    }
  }

  /**
   * HTTP DELETE request
   * Returns Promise
   * @param url String representation of url
   * @param type Typescript class type.Optional.
   * @param useConstructor boolean (default false). Indicates if we want to use class constructor (true) or use default constructor (false).Optional.
   * @param config AxiosRequestConfig | undefined. Additional axios configuration.Optional.
   */
  public async delete<T>(url: string, type?: (new (arg: any) => T)/* , useConstructor?: boolean */): Promise<any> {
    try {
      return await $axios.delete(url);
    } catch (error) {
      throw new Error((error as AxiosError).response?.data ?? (error as Error).message);
    }
  }

  /**
   * HTTP POST request
   * Returns Promise
   * @param url String representation of url
   * @param type Typescript class type.Optional.
   * @param useConstructor boolean (default false). Indicates if we want to use class constructor (true) or use default constructor (false).Optional.
   * @param config AxiosRequestConfig | undefined. Additional axios configuration.Optional.
   */
  public async post<T>(url: string, payload: any, type?: (new (arg: any) => T)/* , useConstructor?: boolean */): Promise<any> {
    if (type) {
      try {
        const { data } = await $axios.post(url, payload);
        const items = data.items;
        data.items = this.parseData2(type, items);
        return data;
      } catch (error) {
        throw new Error((error as AxiosError).response?.data ?? (error as Error).message);
      }
    } else {
      // if there is no type, return axios default behavior
      try {
        return $axios.post(url, payload);
      } catch (error) {
        throw new Error((error as AxiosError).response?.data ?? (error as Error).message);
      }
    }
  }

  /**
   * HTTP PUT request
   * Returns Promise
   * @param url String representation of url
   * @param type Typescript class type.Optional.
   * @param useConstructor boolean (default false). Indicates if we want to use class constructor (true) or use default constructor (false).Optional.
   * @param config AxiosRequestConfig | undefined. Additional axios configuration.Optional.
   */
  public async put<T>(url: string, payload: any, type?: (new (arg: any) => T)/* , useConstructor?: boolean */): Promise<any> {
    if (type) {
      try {
        let { data } = await $axios.put(url, payload);
        data = this.parseData2(type, data);
        return data;
      } catch (error) {
        throw new Error((error as AxiosError).response?.data ?? (error as Error).message);
      }
    } else {
      // if there is no type, return axios default behavior
      try {
        return $axios.put(url, payload);
      } catch (error) {
        throw new Error((error as AxiosError).response?.data ?? (error as Error).message);
      }
    }
  }

  /**
   * Creates response object
   * @param type Typescript class type to be returned
   * @param data Response data
   * @param useConstructor boolean (default false). Indicates if we want to use class constructor (true) or use default constructor (false)
   * NON UTILISE, A ENLEVER UN JOUR
   */
  private createObject(Type: any, data: any, useConstructor: boolean = false): any {
    let result: any;

    if (useConstructor) {
      result = new Type(data);
    } else {
      result = new Type();
      for (const key in data) {
        if (Object.prototype.hasOwnProperty.call(result, key)) {
          result[key] = data[key];
        }
      }
    }
    return result;
  }

  /**
   * Parse response data, before creating response object
   * @param type Typescript class type to be returned
   * @param data Response data
   * @param useConstructor boolean (default false). Indicates if we want to use class constructor (true) or use default constructor (false)
   */
  private parseData2<T>(classType: ClassConstructor<T>, data: any): T {
    return plainToInstance(classType, data);
  }
}

const $AxiosWrapper: AxiosWrapper = new AxiosWrapper();

export default $AxiosWrapper;
