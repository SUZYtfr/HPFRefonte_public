import { $axios } from '~/utils/api'
import { FanfictionData, FanfictionQueryParams } from "@/types/fanfictions"

export const getFanfictions = (params: FanfictionQueryParams) =>
  $axios.request({
    url: '/fictions/fictions/',
    method: 'get',
    params
  })