import type { NuxtAxiosInstance } from "@nuxtjs/axios";
import type { ClassConstructor } from "class-transformer";
import { plainToInstance } from "class-transformer";
// import { Message, MessageBox } from 'element-ui'
import qs from "qs";

let $axios: NuxtAxiosInstance;

export function initializeAxios(axiosInstance: NuxtAxiosInstance): void {
  $axios = axiosInstance;
  $axios.create({
    baseURL: process.env.VUE_APP_BASE_API,
    timeout: 5000,
    withCredentials: false
  });

  $axios.defaults.paramsSerializer = params => qs.stringify(params, { arrayFormat: "repeat", skipNulls: true });

  // Request interceptors
  $axios.interceptors.request.use(
    (config) => {
      // Add X-Access-Token header to every request, you can add other custom headers here
      // if (UserModule.token) {
      //   config.headers["X-Access-Token"] = UserModule.token;
      // }
      // config.paramsSerializer = params => qs.stringify(params, { arrayFormat: "repeat", skipNulls: true });
      return config;
    },
    (error) => {
      Promise.reject(error);
    }
  );

  // Response interceptors
  $axios.interceptors.response.use(
    (response) => {
      // Some example codes here:
      // code == 20000: success
      // code == 50001: invalid access token
      // code == 50002: already login in other place
      // code == 50003: access token expired
      // code == 50004: invalid user (user not exist)
      // code == 50005: username or password is incorrect
      // You can change this part for your own usage.
      // const res = response.data
      // if (res.code !== 20000) {
      //   Message({
      //     message: res.message || 'Error',
      //     type: 'error',
      //     duration: 5 * 1000
      //   })
      //   if (res.code === 50008 || res.code === 50012 || res.code === 50014) {
      //     MessageBox.confirm(
      //       'You have been logged out, try to login again.',
      //       'Log out',
      //       {
      //         confirmButtonText: 'Relogin',
      //         cancelButtonText: 'Cancel',
      //         type: 'warning'
      //       }
      //     ).then(() => {
      //       UserModule.ResetToken()
      //       location.reload() // To prevent bugs from vue-router
      //     })
      //   }
      //   return Promise.reject(new Error(res.message || 'Error'))
      // } else {
      // return response.data
      return response.data;
      // }
    },
    (error) => {
      // Message({
      //     message: error.message,
      //     type: 'error',
      //     duration: 5 * 1000
      // })
      return Promise.reject(error);
    }
  );
}

export interface ResponseWrapper<T> {
  items: T;
  total: number;
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
        const { data } = await $axios.request({
          url: url,
          method: "get",
          params: params
        });
        const items = data.items;
        console.log("dans le get");
        console.log(items);
        // console.log(items[0]);
        // console.log(items[0] instanceof type);
        // if (process.client) data.items = this.parseData(type, items, useConstructor);
        // if (process.client)
        data.items = this.parseData2(type, items);
        // console.log(data);
        // console.log(data.items[0]);
        // console.log(data.items[0] instanceof type);
        return data;
      } catch (error) {
        console.log(error);
        throw error;
      }
      // return new Promise(async (resolve, reject) => {
      //   try {
      //     const { data } = await $axios.request({
      //       url: url,
      //       method: "get",
      //       params: params
      //     });
      //     const items = data.items;
      //     if (process.client) data.items = this.parseData(type, items, useConstructor)
      //     return resolve(data);
      //   } catch (error) {
      //     return reject(error);
      //   }
      // });
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
  // private parseData(type: any, data: any, useConstructor: boolean = false): (any[] | null) {
  //   console.log("on passe par ici");
  //   if (!data) {
  //     return null;
  //   }
  //   if (Array.isArray(data)) {
  //     const result = data.map(x => this.createObject(type, x, useConstructor));
  //     return result;
  //   } else {
  //     const result = this.createObject(type, data, useConstructor);
  //     return result;
  //   }
  // }

  private parseData2<T>(classType: ClassConstructor<T>, data: any): T {
    console.log("parseData2");
    return plainToInstance(classType, data);
  }
}

const $AxiosWrapper: AxiosWrapper = new AxiosWrapper();

export default $AxiosWrapper;
