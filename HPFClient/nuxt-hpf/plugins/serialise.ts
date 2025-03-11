import { plainToInstance, instanceToPlain } from "class-transformer"
import { NewsModel } from "~/models/news";
import { FanfictionModel, TableOfContent } from "~/models/fanfictions";
import { CharacteristicModel, CharacteristicTypeModel } from "~/models/characteristics";
import { ReviewModel } from "~/models/fanfictions";
// import * from "~/models/index.ts";

// const classNameToClass = new Map([
//   [NewsModel.name, NewsModel]
// ])


export default definePayloadPlugin((nuxtApp) => {
  definePayloadReducer('NewsModel', data => data && data instanceof NewsModel && instanceToPlain(data))
  definePayloadReviver('NewsModel', data => plainToInstance(NewsModel, data))
  definePayloadReducer('FanfictionModel', data => data && data instanceof FanfictionModel && instanceToPlain(data))
  definePayloadReviver('FanfictionModel', data => plainToInstance(FanfictionModel, data))
  definePayloadReducer('TableOfContent', data => data && data instanceof TableOfContent && instanceToPlain(data))
  definePayloadReviver('TableOfContent', data => plainToInstance(TableOfContent, data))
  definePayloadReducer('CharacteristicModel', data => data && data instanceof CharacteristicModel && instanceToPlain(data))
  definePayloadReviver('CharacteristicModel', data => plainToInstance(CharacteristicModel, data))
  definePayloadReducer('CharacteristicTypeModel', data => data && data instanceof CharacteristicTypeModel && instanceToPlain(data))
  definePayloadReviver('CharacteristicTypeModel', data => plainToInstance(CharacteristicTypeModel, data))
  definePayloadReducer('ReviewModel', data => data && data instanceof ReviewModel && instanceToPlain(data))
  definePayloadReviver('ReviewModel', data => plainToInstance(ReviewModel, data))
})