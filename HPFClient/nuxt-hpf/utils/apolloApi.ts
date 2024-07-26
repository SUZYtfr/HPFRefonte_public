import type { ApolloClient, InMemoryCache, QueryOptions } from '@apollo/client/core'
import type { ClassConstructor } from "class-transformer";
import { plainToInstance } from "class-transformer";
import type { DocumentNode } from "graphql/language/ast";


// const createApolloClient = () => {
//     new ApolloClient({
//         uri: process.env.SERVER_GRAPHQL_API,
//         cache: new InMemoryCache(),
//     });
// }

let $apollo: ApolloClient<any>;

export function initializeApollo(apolloInstance: any): void {
    $apollo = apolloInstance;
    // $apollo.create({
    //   baseURL: process.env.SERVER_BASE_API,
    //   timeout: 5000,
    //   withCredentials: (process.env.NODE_ENV === "production")
    // });
  
    // $apollo.defaults.paramsSerializer = params => qs.stringify(params, { arrayFormat: "repeat", skipNulls: true });
  
    // $apollo.interceptors.request.use((request) => {
    //   // console.log("Starting Request", JSON.stringify(request, null, 2));
    //   return request;
    // });
  
    // $apollo.interceptors.response.use((response) => {
    //   // console.log("Response:", JSON.stringify(response, null, 2));
    //   return response;
    // });
  }

export { $apollo };


export class ApolloWrapper {
    /**
     * Get axios instance if additional configuration is needed
     */
    get apolloInstance(): ApolloClient<InMemoryCache> { return $apollo; }

    public async query<T>(query: DocumentNode, params: any, type?: (new (arg: any) => T)/* , useConstructor?: boolean */): Promise<any> {
        
        const queryOptions: QueryOptions = {
            query: query,
        };
        if (type) {
            try {
                let { data } = await $apollo.query(queryOptions);
                console.log(data)
                const results = data[params].results;
                // Transformer en instance
                if (results != null) {
                    // Contenu paginé
                    data.count = data[params].count;
                    data.page = data[params].current;
                    data.results = this.parseData2(type, results);
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
            return $apollo.query(queryOptions);
        }
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

const $ApolloWrapper: ApolloWrapper = new ApolloWrapper();

export default $ApolloWrapper;
