import { NuxtAxiosInstance } from '@nuxtjs/axios'
//import { Message, MessageBox } from 'element-ui'
import { UserModule } from '@/utils/store-accessor'
import qs from 'qs'

let $axios: NuxtAxiosInstance

export function initializeAxios(axiosInstance: NuxtAxiosInstance) {
    $axios = axiosInstance
    $axios.create({
        baseURL: "http://127.0.0.1:8000/api/",
        timeout: 5000,
        withCredentials: false,
    })
    
    // Request interceptors
//     $axios.interceptors.request.use(
//         (config) => {
//             // Add X-Access-Token header to every request, you can add other custom headers here
//             if (UserModule.token) {
//                 config.headers['X-Access-Token'] = UserModule.token
//             }
//             return config
//         },
//         (error) => {
//             Promise.reject(error)
//         }
//     )

    // Response interceptors
    $axios.interceptors.response.use(
        (response) => {
            // Some example codes here:
            // code == 20000: success
            // code == 50001: invalid access token
            // code == 50002: already login in other place
            // code == 50003: access token expired
            // code == 50004: invalid user (user not exist)
            // code == 50005: username or password is incorrect
            // You can change this part for your own usage.
            //const res = response.data
            // if (res.code !== 20000) {
            //   Message({
            //     message: res.message || 'Error',
            //     type: 'error',
            //     duration: 5 * 1000
            //   })
            //   if (res.code === 50008 || res.code === 50012 || res.code === 50014) {
            //     MessageBox.confirm(
            //       'You have been logged out, try to login again.',
            //       'Log out',
            //       {
            //         confirmButtonText: 'Relogin',
            //         cancelButtonText: 'Cancel',
            //         type: 'warning'
            //       }
            //     ).then(() => {
            //       UserModule.ResetToken()
            //       location.reload() // To prevent bugs from vue-router
            //     })
            //   }
            //   return Promise.reject(new Error(res.message || 'Error'))
            // } else {
            //return response.data
            return response
            //}
        },
        (error) => {
            // Message({
            //     message: error.message,
            //     type: 'error',
            //     duration: 5 * 1000
            // })
            return Promise.reject(error)
        }
    )

    $axios.defaults.paramsSerializer = function (params: any) {
        return qs.stringify(params, {arrayFormat: 'repeat'})
    }
}

export { $axios }
