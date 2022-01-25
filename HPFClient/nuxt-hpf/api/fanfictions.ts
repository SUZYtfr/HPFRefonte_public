import { $axios } from '~/utils/api'

export const getFanfictions = (params: any) =>
  $axios.request({
    url: '/fanfictions',
    method: 'get',
    params
  })
