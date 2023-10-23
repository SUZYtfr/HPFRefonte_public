import Vue from "vue";
import { CharacteristicData, CharacteristicTypeData } from "@/types/characteristics";
import { UserData, UserLinkData, AuthorData } from "@/types/users";
import { NewsData, CommentData } from "@/types/news";
import { FanfictionData, ReviewData, SerieData } from "@/types/fanfictions";

import { UserModel } from "@/models/users";
import { CharacteristicModel, CharacteristicTypeModel } from "@/models/characteristics";
import { NewsModel, CommentModel } from "@/models/news";
import { FanfictionModel, ReviewModel, SerieModel, ChapterModel } from "@/models/fanfictions";

import { FanfictionListType } from "@/types/other";

// // Types
// Vue.prototype.UserData = UserData;
// Vue.prototype.AuthorData = AuthorData;
// Vue.prototype.UserLinkData = UserLinkData;
// Vue.prototype.CharacteristicData = CharacteristicData;
// Vue.prototype.CharacteristicTypeData = CharacteristicTypeData;
// Vue.prototype.NewsData = NewsData;
// Vue.prototype.CommentData = CommentData;
// Vue.prototype.FanfictionData = FanfictionData;
// Vue.prototype.ReviewData = ReviewData;
// Vue.prototype.SerieData = SerieData;

// // Models
// Vue.prototype.UserModel = UserModel;
// Vue.prototype.CharacteristicModel = CharacteristicModel;
// Vue.prototype.CharacteristicTypeModel = CharacteristicTypeModel;
// Vue.prototype.CommentModel = CommentModel;
// Vue.prototype.NewsModel = NewsModel;
// Vue.prototype.FanfictionModel = FanfictionModel;
// Vue.prototype.ReviewModel = ReviewModel;
// Vue.prototype.SerieModel = SerieModel;
// Vue.prototype.ChapterModel = ChapterModel;

// // Enum
// Vue.prototype.FanfictionListType = FanfictionListType;

export default defineNuxtPlugin({
    async setup (nuxtApp) {
        // // Types
        // nuxtApp.vueApp.config.globalProperties.UserData = UserData
        // nuxtApp.vueApp.config.globalProperties.AuthorData = AuthorData
        // nuxtApp.vueApp.config.globalProperties.UserLinkData = UserLinkData
        // nuxtApp.vueApp.config.globalProperties.CharacteristicData = CharacteristicData
        // nuxtApp.vueApp.config.globalProperties.CharacteristicTypeData = CharacteristicTypeData
        // nuxtApp.vueApp.config.globalProperties.NewsData = NewsData
        // nuxtApp.vueApp.config.globalProperties.CommentData = CommentData
        // nuxtApp.vueApp.config.globalProperties.FanfictionData = FanfictionData
        // nuxtApp.vueApp.config.globalProperties.ReviewData = ReviewData
        // nuxtApp.vueApp.config.globalProperties.SerieData = SerieData

        // // Models
        // nuxtApp.vueApp.config.globalProperties.UserModel = UserModel
        // nuxtApp.vueApp.config.globalProperties.CharacteristicModel = CharacteristicModel
        // nuxtApp.vueApp.config.globalProperties.CharacteristicTypeModel = CharacteristicTypeModel
        // nuxtApp.vueApp.config.globalProperties.CommentModel = CommentModel
        // nuxtApp.vueApp.config.globalProperties.NewsModel = NewsModel
        // nuxtApp.vueApp.config.globalProperties.FanfictionModel = FanfictionModel
        // nuxtApp.vueApp.config.globalProperties.ReviewModel = ReviewModel
        // nuxtApp.vueApp.config.globalProperties.SerieModel = SerieModel
        // nuxtApp.vueApp.config.globalProperties.ChapterModel = ChapterModel

        // Enum
        nuxtApp.vueApp.config.globalProperties.FanfictionListType = FanfictionListType
    }
})
