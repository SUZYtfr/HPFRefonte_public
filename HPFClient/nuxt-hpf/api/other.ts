import { $axios } from '~/utils/api'
import { ContactFormData } from "@/types/other";


export const contact = (data: ContactFormData) =>
    $axios.request({
        url: '/contact',
        method: 'post',
        data
    })