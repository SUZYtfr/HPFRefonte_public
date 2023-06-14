import { AxiosResponse } from "axios";
import $AxiosWrapper, { $axios } from "~/utils/api";
import { UserRegisterData } from "@/types/users";
import { UserModel } from "~/models/users";

export const getUserInfo = (data: any): Promise<AxiosResponse<any>> =>
  $axios.request({
    url: "/users/info/",
    method: "post",
    data
  });

export const getUser = (user_id: number): Promise<any> => $AxiosWrapper.get<UserModel>("/users/" + user_id.toString() + "/", null, UserModel);

export const signup = (data: UserRegisterData): Promise<AxiosResponse<any>> =>
  $axios.request({
    url: "/account/",
    method: "post",
    data
  });
