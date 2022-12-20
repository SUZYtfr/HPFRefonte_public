import { $axios } from '~/utils/api'
import { UserRegisterData, UserLoginData } from "@/types/account"

export const signup = (data: UserRegisterData) =>
    $axios.request({
        url: '/account/',
        method: 'post',
        data
    })

export const login = (data: UserLoginData) =>
    $axios.request({
        url: '/account/token/',
        method: 'post',
        data
    })

export const logout = () =>
    $axios.request({
        url: '/account/logout',
        method: 'post'
    })

export const getUserInfo = () =>
    $axios.request({
        url: '/account/',
        method: 'get'
    })
