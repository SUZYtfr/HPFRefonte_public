import $AxiosWrapper from "~/utils/api";
import { ThemeModel } from "~/models/themes";
import { IBasicQuery } from "@/types/basics";

export const searchThemes = (filters: IBasicQuery | null): Promise<any> => $AxiosWrapper.get<ThemeModel>("/users/themes/", filters, ThemeModel);
