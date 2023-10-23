// import { AxiosResponse } from "axios";
// import { $axios } from "~/utils/api";
import { ContactFormData } from "@/types/other";
import $UseFetchWrapper from "~/utils/api";

export const contact = (data: ContactFormData): Promise<any> => $UseFetchWrapper.post<ContactFormData>("/contact/", data)
