import { $axios } from '~/utils/api'

export const getCharacteristics = () =>
    $axios.request({
        url: '/characteristics',
        method: 'get',
    })

export const getCharacteristicsTypes = () =>
    $axios.request({
        url: '/characteristics_types',
        method: 'get',
    })