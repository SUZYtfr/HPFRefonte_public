import { plainToInstance, instanceToPlain } from "class-transformer";
import * as models from "~/models";

export default definePayloadPlugin(() => {
  Object.entries(models).forEach(([modelName, modelClass]) => {
    if (typeof modelClass !== "function") return;
    definePayloadReducer(modelName, (data) => data && data instanceof modelClass && instanceToPlain(data));
    /* eslint-disable @typescript-eslint/no-explicit-any */
    definePayloadReviver(modelName, (data) => plainToInstance(modelClass as new (...args: any[]) => any, data));
  });
});
