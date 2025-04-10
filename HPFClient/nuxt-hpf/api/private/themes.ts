import $AxiosWrapper from "~/utils/api";
import { ThemeModel } from "~/models/themes";
import { IBasicQuery } from "@/types/basics";
import { UseFetchOptions } from "nuxt/app";
import { Paginated } from "@/types/basics";

export const searchThemes = (filters: IBasicQuery | null, options?: UseFetchOptions<Paginated<ThemeModel[]>>) => $AxiosWrapper.get<Paginated<ThemeModel[]>>("/private/users/themes/", filters, ThemeModel, options);
export const postTheme = (theme: ThemeModel, options?: UseFetchOptions<ThemeModel>) => $AxiosWrapper.post<ThemeModel>("/private/users/themes/", theme, ThemeModel, options);
export const putTheme = (id: number, theme: ThemeModel, options?: UseFetchOptions<ThemeModel>) => $AxiosWrapper.put<ThemeModel>(`/private/users/themes/${id.toString()}/`, theme, ThemeModel, options);
export const deleteTheme = (id: number, options?: UseFetchOptions<ThemeModel>) => $AxiosWrapper.delete<ThemeModel>(`/private/users/themes/${id.toString()}/`, ThemeModel, options);
