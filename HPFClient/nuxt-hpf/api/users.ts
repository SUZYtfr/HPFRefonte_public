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

export const getUser = (id: number): Promise<any> => $AxiosWrapper.get<UserModel>(`/users/users/${id.toString()}/`, null, UserModel);
