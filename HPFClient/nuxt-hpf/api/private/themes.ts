import $AxiosWrapper from "~/utils/api";
import { ThemeModel } from "~/models/themes";
import { IBasicQuery } from "@/types/basics";

export const searchThemes = (filters: IBasicQuery | null): Promise<any> => $AxiosWrapper.get<ThemeModel>("/users/themes/", filters, ThemeModel);
export const postTheme = (theme: ThemeModel): Promise<any> => $AxiosWrapper.post<ThemeModel>("/users/themes/", theme, ThemeModel);
export const putTheme = (id: number, theme: ThemeModel): Promise<any> => $AxiosWrapper.put<ThemeModel>(`/users/themes/${id.toString()}/`, theme, ThemeModel);
export const deleteTheme = (id: number): Promise<any> => $AxiosWrapper.delete<ThemeModel>(`/users/themes/${id.toString()}/`, ThemeModel);
