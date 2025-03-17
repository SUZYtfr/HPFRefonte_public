import { plainToInstance, instanceToPlain } from "class-transformer"
import * as models from "~/models";

export default definePayloadPlugin((nuxtApp) => {
  Object.entries(models).forEach(([modelName, modelClass]) => {
    definePayloadReducer(modelName, data => data && data instanceof modelClass && instanceToPlain(data));
    definePayloadReviver(modelName, data => plainToInstance(modelClass as any, data));
  });
});
