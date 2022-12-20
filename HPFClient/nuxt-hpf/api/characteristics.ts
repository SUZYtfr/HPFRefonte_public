import { $axios } from '~/utils/api'
import { PaginatedResponse } from "@/types/basics"
import { CharacteristicQueryParams, ICharacteristic, ICharacteristicType } from "@/types/characteristics"
import qs from 'qs'

export const getCharacteristics = (filters : CharacteristicQueryParams) =>
    $axios.request({
        url: '/features/features/',
        method: 'get',
        params: filters,
        paramsSerializer: params => {
            return qs.stringify(params)
          }
    })

export const getCharacteristicTypes = () =>
    $axios.request({
        url: '/features/categories/',
        method: 'get',
    })