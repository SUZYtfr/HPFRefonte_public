import { $axios } from '~/utils/api'
import { ICharacteristicFilters } from "@/types/characteristics";
import qs from 'qs';

export const getCharacteristics = (filters : ICharacteristicFilters | null) =>
    $axios.request({
        url: '/characteristics',
        method: 'get',
        params: filters,
        paramsSerializer: params => {
            return qs.stringify(params)
          }
    })

export const getCharacteristicsTypes = () =>
    $axios.request({
        url: '/characteristics_types',
        method: 'get',
    })