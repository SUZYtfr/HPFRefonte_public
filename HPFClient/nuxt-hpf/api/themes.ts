import $AxiosWrapper from "~/utils/api";
import { ThemeModel } from "~/models/themes";
import { IBasicQuery } from "@/types/basics";

export const searchThemes = (filters: IBasicQuery | null): Promise<any> => $AxiosWrapper.get<ThemeModel>("/themes/", filters, ThemeModel);
export const postTheme = (theme: ThemeModel): Promise<any> => $AxiosWrapper.post<ThemeModel>("/themes/", theme, ThemeModel);
export const putTheme = (id: number, theme: ThemeModel): Promise<any> => $AxiosWrapper.put<ThemeModel>("/themes/" + id.toString() + "/", theme, ThemeModel);
