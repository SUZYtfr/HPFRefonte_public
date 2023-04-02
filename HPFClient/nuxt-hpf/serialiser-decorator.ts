import Vue, { ComponentOptions } from "vue";
import { ClassConstructor, /* plainToClass, */plainToInstance } from "class-transformer";
import { createDecorator, VueDecorator } from "vue-class-component";

/** Deserialize an SSR data on client side with the given constructor
 * @param classType The class constructor to use for this property
 */
export const SerialiseClass = <T>(classType: ClassConstructor<T>): VueDecorator => createDecorator((options, key): void => {
  console.log("Serializer");
  console.log(key);
  if (process.server) {
    wrapFetch(options, key);
  } else {
    wrapBeforeCreate(options, key, classType);
  }
});

/** Enrich the asyncData hook with a registering function.
 * Ensure we still call the original hook if it exists.
 */
// function wrapAsyncData(options: ComponentOptions<Vue>, key: string): void {
//   const originalAsyncDataHook = options.asyncData;
//   options.asyncData = async function wrapperAsyncData(...args) {
//     const originalAsyncData = (await originalAsyncDataHook?.apply(this, args)) || {};

//     registerSerializableProp(originalAsyncData, key);

//     return originalAsyncData;
//   };
// }

/** Enrich the fetch hook with a registering function.
 * Ensure we still call the original hook if it exists.
 */
function wrapFetch(options: ComponentOptions<Vue>, key: string): void {
  console.log("wrapFetch");
  const originalwrapFetchHook = options.fetch;
  options.fetch = async function wrapperFetch(...args) {
    const originalAsyncData = (await originalwrapFetchHook?.apply(this, args));

    registerSerializableProp(originalAsyncData, key);
    return originalAsyncData;
  };
}

/** Add a config property to store the data that must be serialised */
function registerSerializableProp(asyncData: any, key: string): void {
  console.log("registerSerializableProp asyncData: " + asyncData);
  console.log("registerSerializableProp key: " + key);
  if (asyncData == null) {
    asyncData = {};
    asyncData.serializerConfig = [];
  }
  asyncData.serializerConfig = asyncData.serializerConfig || [];
  console.log("registerSerializableProp asyncData après: ");
  console.log(asyncData);
  asyncData.serializerConfig.push(key);
}

/** Enrich the beforeCreate hook with a deserialiser function.
 * Ensure we still call the original hook if it exists.
 */
function wrapBeforeCreate<T>(options: ComponentOptions<Vue>, key: string, classType: ClassConstructor<T>): void {
  console.log("wrapBeforeCreate");
  console.log(key);
  const originalBeforeCreateHook = options.beforeCreate;
  options.beforeCreate = function deserializerWrapper(...args) {
    deserializer.call(this, key, classType);
    originalBeforeCreateHook?.apply(this, args);
  };
}

/** Deserialise a POJO data to a class instance
 * @param key the property name
 * @param classType The class constructor used to create the instance
 */
function deserializer<T>(this: Vue, key: string, classType: ClassConstructor<T>): void {
  console.log("deserializer: " + key);
  console.log(this.$nuxt.context.nuxtState);
  // console.log(classType);
  // console.log(this.$nuxt);
  // console.log(this.$nuxt.context);
  // const { data } = this.$nuxt.context.nuxtState || {};
  const { fetch } = this.$nuxt.context.nuxtState || {};
  // console.log("data:");
  // console.log(data);
  // if (data) {
  //   const [asyncData] = data;
  //   console.log(asyncData[key]);
  //   if (asyncData && asyncData[key]) {
  //     asyncData[key] = plainToClass(classType, asyncData[key]);
  //   }
  // }
  // console.log("fetch:");
  // console.log(fetch);
  // console.log(Object.keys(fetch)[0]);
  // console.log(fetch[Object.keys(fetch)[0]]);
  // console.log(fetch["site-sidebar:0"]);
  // console.log(fetch["site-sidebar:0"][key]);
  if (fetch) {
    // const asyncFetch = fetch[Object.keys(fetch)[0]];
    // // console.log(key);
    // // console.log(asyncFetch[key]);
    // if (asyncFetch && asyncFetch[key]) {
    //   console.log("on passe par là");
    //   // asyncFetch[key] = plainToClass(classType, asyncFetch[key]);
    //   asyncFetch[key] = plainToInstance(classType, asyncFetch[key]);
    //   // console.log(key);
    //   console.log(asyncFetch[key]);
    // }

    // const asyncFetch = fetch[Object.keys(fetch)[0]];

    Object.keys(fetch).forEach((fetchkey) => {
      console.log("FetchKey: ");
      console.log(fetchkey);

      Object.keys(fetch[fetchkey]).forEach((localKey) => {
        if (localKey !== key) return;
        const asyncFetch = fetch[fetchkey];
        console.log("AsyncFetch: ");
        console.log(key);
        console.log("Plain:");
        console.log(asyncFetch[key]);
        asyncFetch[key] = plainToInstance(classType, asyncFetch[key]);
        console.log("Instance:");
        console.log(asyncFetch[key]);
      });
    });

    // console.log(asyncFetch);
    // Object.keys(asyncFetch).forEach((key) => {
    //   console.log("AsyncFetch: ");
    //   console.log(key);
    //   console.log(asyncFetch[key]);
    //   asyncFetch[key] = plainToInstance(classType, asyncFetch[key]);
    // });
  }
}
