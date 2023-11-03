import type { ClassConstructor } from "class-transformer";
import { plainToInstance } from "class-transformer";

// Est-ce qu'on a vraiment besoin de ça ?
export interface ListResponseWrapper<T> {
  items: T[];
  count: number;
  next: string | null;
  previous: string | null;
  current: number;
}

export interface UseFetchWrapperResponse<T> {
  data: Ref<T>
  pending: Ref<boolean>
  execute: Promise<void>
  refresh: Promise<void>
  error: Ref<any>
  status: Ref<string>
}

export class UseFetchWrapper {
  /**
   * HTTP GET request
   * Returns Promise
   * @param url String representation of url
   * @param type Typescript class type. Optional.
   * @param useConstructor boolean (default false). Indicates if we want to use class constructor (true) or use default constructor (false). Optional.
   * @param config AxiosRequestConfig. Additional axios configuration. Optional.
   */
  public async get<T>(url: string, params: any, type?: (new (arg: any) => T), options?: any/* , useConstructor?: boolean */): Promise<any> {
    try {
      return useCustomFetch(
        url,
        {
          method: "get",
          params: params,
          ...options
        },
        type
      )
    } catch (error) {
      console.log(error);
      throw error;
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
  public async delete<T>(url: string, type?: (new (arg: any) => T), options?: any/* , useConstructor?: boolean */): Promise<any> {
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

  /**
   * HTTP POST request
   * Returns Promise
   * @param url String representation of url
   * @param type Typescript class type.Optional.
   * @param useConstructor boolean (default false). Indicates if we want to use class constructor (true) or use default constructor (false).Optional.
   * @param config AxiosRequestConfig | undefined. Additional axios configuration.Optional.
   */
  public async post<T>(url: string, payload: any, type?: (new (arg: any) => T), options?: any/* , useConstructor?: boolean */): Promise<any> {
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

  /**
   * HTTP PUT request
   * Returns Promise
   * @param url String representation of url
   * @param type Typescript class type.Optional.
   * @param useConstructor boolean (default false). Indicates if we want to use class constructor (true) or use default constructor (false).Optional.
   * @param config AxiosRequestConfig | undefined. Additional axios configuration.Optional.
   */
  public async put<T>(url: string, payload: any, type?: (new (arg: any) => T), options?: any/* , useConstructor?: boolean */): Promise<any> {
    try {
      return useCustomFetch(
        url,
        {
          method: "put",
          body: payload,
          ...options
        }
      );
    } catch (error) {
      console.log(error)
      throw error;
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

const $UseFetchWrapper: UseFetchWrapper = new UseFetchWrapper()

export default $UseFetchWrapper;
