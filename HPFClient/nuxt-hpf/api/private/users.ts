import $AxiosWrapper from "~/utils/api";
import { IBasicQuery, Paginated } from "~/types/basics";
import { UserModel } from "~/models/users";
import { UseFetchOptions } from "nuxt/app";

export const searchUsers = (filters: IBasicQuery | null, options?: UseFetchOptions<Paginated<UserModel[]>>) => $AxiosWrapper.get<Paginated<UserModel[]>>(`/private/users/users/`, filters, UserModel, options);
export const putUser = (id: number, user: UserModel, options?: UseFetchOptions<UserModel>) => $AxiosWrapper.put<UserModel>(`/private/users/users/${id.toString()}/`, user, UserModel, options);
export const anonymiseUser = (id: number, options?: UseFetchOptions<UserModel>): Promise<any> => $AxiosWrapper.put(`/private/users/users/${id.toString()}/anonymise/`, null, UserModel, options);
export const sendPasswordResetEmail = (id: number, options?: UseFetchOptions<UserModel>): Promise<any> => $AxiosWrapper.put(`/private/users/users/${id.toString()}/send-password-reset-email/`, null, UserModel, options);
