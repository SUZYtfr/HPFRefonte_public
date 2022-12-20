import { $axios } from '~/utils/api'
import { UserData } from "@/types/users";

export const getUser = (user_id: string) =>
    $axios.request({
        url: '/users/' + user_id + '/',
        method: 'get'
    })
