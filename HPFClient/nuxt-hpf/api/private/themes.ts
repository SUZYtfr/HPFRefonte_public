import $AxiosWrapper from "~/utils/api";
import { ThemeModel } from "~/models/themes";
import { IBasicQuery } from "@/types/basics";

export const searchThemes = (filters: IBasicQuery | null) => $AxiosWrapper.get<ThemeModel[]>("/users/themes/", filters, ThemeModel);
export const postTheme = (theme: ThemeModel) => $AxiosWrapper.post<ThemeModel>("/private/users/themes/", theme, ThemeModel);
export const putTheme = (id: number, theme: ThemeModel) => $AxiosWrapper.put<ThemeModel>(`/private/users/themes/${id.toString()}/`, theme, ThemeModel);
export const deleteTheme = (id: number) => $AxiosWrapper.delete<ThemeModel>(`/private/users/themes/${id.toString()}/`, ThemeModel);
