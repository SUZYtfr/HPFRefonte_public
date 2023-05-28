import { AxiosResponse } from "axios";
import { $axios } from "~/utils/api";
import { UserRegisterData } from "@/types/users";

export const getUserInfo = (data: any): Promise<AxiosResponse<any>> =>
  $axios.request({
    url: "/users/info",
    method: "post",
    data
  });

export const getUser = (user_id: string): Promise<AxiosResponse<any>> =>
  $axios.request({
    url: "/authors/" + user_id,
    method: "get"
  });

export const signup = (data: UserRegisterData): Promise<AxiosResponse<any>> =>
  $axios.request({
    url: "/signup",
    method: "post",
    data
  });
