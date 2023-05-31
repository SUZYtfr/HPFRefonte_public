import type { NuxtAxiosInstance } from "@nuxtjs/axios";
import type { ClassConstructor } from "class-transformer";
import { plainToInstance } from "class-transformer";
import qs from "qs";

let $axios: NuxtAxiosInstance;

export function initializeAxios(axiosInstance: NuxtAxiosInstance): void {
  $axios = axiosInstance;
  $axios.create({
    baseURL: process.env.VUE_APP_BASE_API,
    timeout: 5000,
    withCredentials: (process.env.NODE_ENV === "production")
  });

  $axios.defaults.paramsSerializer = params => qs.stringify(params, { arrayFormat: "repeat", skipNulls: true });
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
          data.results = this.parseData2(type, data.results);
        } else {
          // Contenu unique
          data = this.parseData2(type, data);
        }
        return data;
      } catch (error) {
        console.log(error);
        throw error;
      }
    } else {
      // if there is no type, return axios default behavior
      return $axios.get(url);
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
    if (type) {
      try {
        const { data } = await $axios.delete(url);
        const items = data.items;
        // if (process.client) data.items = this.parseData(type, items, useConstructor);
        data.items = this.parseData2(type, items);
        return data;
      } catch (error) {
        return error;
      }
      // return new Promise(async (resolve, reject) => {
      //   try {
      //     const { data } = await $axios.delete(url);
      //     const items = data.items;
      //     if (process.client) data.items = this.parseData(type, items, useConstructor)
      //     return resolve(data);
      //   } catch (error) {
      //     return reject(error);
      //   }
      // });
    } else {
      // if there is no type, return axios default behavior
      return $axios.delete(url);
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
        // if (process.client) data.items = this.parseData(type, items, useConstructor);
        data.items = this.parseData2(type, items);
        return data;
      } catch (error) {
        return error;
      }
      // return new Promise(async (resolve, reject) => {
      //   try {
      //     const { data } = await $axios.post(url, payload);
      //     const items = data.items;
      //     if (process.client) data.items = this.parseData(type, items, useConstructor)
      //     return resolve(data);
      //   } catch (error) {
      //     return reject(error);
      //   }
      // });
    } else {
      // if there is no type, return axios default behavior
      return $axios.post(url, payload);
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
        const { data } = await $axios.put(url, payload);
        const items = data.items;
        // if (process.client) data.items = this.parseData(type, items, useConstructor);
        data.items = this.parseData2(type, items);
        return data;
      } catch (error) {
        return error;
      }
      // return new Promise(async (resolve, reject) => {
      //   try {
      //     const { data } = await $axios.put(url, payload);
      //     const items = data.items;
      //     if (process.client) data.items = this.parseData(type, items, useConstructor)
      //     return resolve(data);
      //   } catch (error) {
      //     return reject(error);
      //   }
      // });
    } else {
      // if there is no type, return axios default behavior
      return $axios.put(url, payload);
    }
  }

  /**
   * Creates response object
   * @param type Typescript class type to be returned
   * @param data Response data
   * @param useConstructor boolean (default false). Indicates if we want to use class constructor (true) or use default constructor (false)
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
