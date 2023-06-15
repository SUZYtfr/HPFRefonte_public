import { ContactFormData } from "@/types/other";
import $AxiosWrapper from "~/utils/api";

export const contact = (data: ContactFormData): Promise<any> => $AxiosWrapper.post("/contact/", data);
