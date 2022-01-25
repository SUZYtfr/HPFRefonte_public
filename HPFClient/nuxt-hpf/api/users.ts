import { $axios } from '~/utils/api'
import { UserRegisterData, UserLoginData } from "@/types/users";


export const getUserInfo = (data: any) =>
    $axios.request({
        url: '/users/info',
        method: 'post',
        data
    })

export const getUser = (user_id: string) =>
    $axios.request({
        url: '/authors/' + user_id,
        method: 'get'
    })

export const login = (data: UserLoginData) =>
    $axios.request({
        url: '/login',
        method: 'post',
        data
    })

export const signup = (data: UserRegisterData) =>
    $axios.request({
        url: '/signup',
        method: 'post',
        data
    })

export const logout = () =>
    $axios.request({
        url: '/users/logout',
        method: 'post'
    })
