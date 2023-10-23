// https://nuxt.com/blog/v3-4#payload-enhancements
// https://github.com/nuxt/nuxt/issues/21832#issuecomment-1694257192
import { plainToClass, instanceToPlain } from "class-transformer"
import { FanfictionModel } from "~/models/fanfictions"
import { NewsModel } from "~/models/news"
import { UserModel } from "~/models/users"

export default definePayloadPlugin((nuxtApp) => {
    definePayloadReducer('FanfictionModel', data => data && data instanceof FanfictionModel && instanceToPlain(data))
    definePayloadReviver('FanfictionModel', data => plainToClass(FanfictionModel, data))

    definePayloadReducer('NewsModel', data => data && data instanceof NewsModel && instanceToPlain(data))
    definePayloadReviver('NewsModel', data => plainToClass(NewsModel, data))

    definePayloadReducer('UserModel', data => data && data instanceof UserModel && instanceToPlain(data))
    definePayloadReviver('UserModel', data => plainToClass(UserModel, data))
})