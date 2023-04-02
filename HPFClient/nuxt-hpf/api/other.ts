import { AxiosResponse } from "axios";
import { $axios } from "~/utils/api";
import { ContactFormData } from "@/types/other";

export const contact = (data: ContactFormData): Promise<AxiosResponse<any>> =>
  $axios.request({
    url: "/contact",
    method: "post",
    data
  });
