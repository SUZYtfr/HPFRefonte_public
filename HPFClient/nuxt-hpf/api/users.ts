import { AxiosResponse } from "axios";
import $AxiosWrapper, { $axios } from "~/utils/api";
import { UserRegisterData } from "@/types/users";
import { UserModel } from "~/models/users";
import { IBasicQuery } from "@/types/basics";

export const getUserInfo = (data: any): Promise<AxiosResponse<any>> =>
  $axios.request({
    url: "/users/info/",
    method: "post",
    data
  });

export const signup = (data: UserRegisterData): Promise<AxiosResponse<any>> =>
  $axios.request({
    url: "/account/",
    method: "post",
    data
  });

export const searchUsers = (filters: IBasicQuery | null): Promise<any> => $AxiosWrapper.get<UserModel>("/users/", filters, UserModel);
export const getUser = (id: number): Promise<any> => $AxiosWrapper.get<UserModel>("/users/" + id.toString() + "/", null, UserModel);
export const putUser = (id: number, user: UserModel): Promise<any> => $AxiosWrapper.put<UserModel>("/users/" + id.toString() + "/", user, UserModel);
export const anonymiseUser = (id: number): Promise<any> => $AxiosWrapper.put("/users/" + id.toString() + "/anonymise/", null);
export const sendPasswordResetEmail = (id: number): Promise<any> => $AxiosWrapper.put("/users/" + id.toString() + "/send-password-reset-email/", null);
