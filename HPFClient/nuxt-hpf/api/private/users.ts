import $AxiosWrapper from "~/utils/api";
import { IBasicQuery } from "~/types/basics";
import { UserModel } from "~/models/users";

export const searchUsers = (filters: IBasicQuery | null): Promise<any> => $AxiosWrapper.get<UserModel>(`/private/users/`, filters, UserModel);
export const putUser = (id: number, user: UserModel): Promise<any> => $AxiosWrapper.put<UserModel>(`/private/users/${id.toString()}/`, user, UserModel);
export const anonymiseUser = (id: number): Promise<any> => $AxiosWrapper.put(`/private/users/${id.toString()}/anonymise/`, null);
export const sendPasswordResetEmail = (id: number): Promise<any> => $AxiosWrapper.put(`/private/users/${id.toString()}/send-password-reset-email/`, null);
