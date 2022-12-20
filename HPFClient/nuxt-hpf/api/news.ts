import { $axios } from '~/utils/api'
import { QueryParams, PaginatedResponse } from "@/types/basics"
import { NewsData } from '~/types/news'

export const getNews = (params: QueryParams) =>
  $axios.request({
    url: '/news/',
    method: 'get',
    params
  })


export const getNew = (newsId: string) =>
  $axios.request({
    url: '/news/' + newsId + "/",
    method: 'get'
  })
