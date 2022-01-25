import { $axios } from '~/utils/api'

export interface NewsData {
  news_id: number;
  post_date: number;
  title: string;
  content: string;
  authors: string;
  comments: string;
}

export const getNews = (params: any) =>
  $axios.request({
    url: '/news',
    method: 'get',
    params
  })
