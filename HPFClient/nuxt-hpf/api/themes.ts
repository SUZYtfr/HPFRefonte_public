/* eslint-disable @typescript-eslint/explicit-function-return-type */

import fetchController from "~/utils/api";
import type { IBasicQuery, Paginated } from "@/types/basics";
import { ThemeModel } from "~/models/themes";
import type { UseFetchOptions } from "nuxt/app";

export const getPublicThemes = (
  filters: IBasicQuery | null | undefined,
  options?: UseFetchOptions<Paginated<ThemeModel[]>>,
) => fetchController.get<Paginated<ThemeModel[]>>("/users/themes/", filters, ThemeModel, options);

export const getPrivateThemes = (filters: IBasicQuery | null, options?: UseFetchOptions<Paginated<ThemeModel[]>>) =>
  fetchController.get<Paginated<ThemeModel[]>>("/private/users/themes/", filters, ThemeModel, options);

export const postTheme = (theme: ThemeModel, options?: UseFetchOptions<ThemeModel>) =>
  fetchController.post<ThemeModel>("/private/users/themes/", theme, ThemeModel, options);

export const putTheme = (id: number, theme: ThemeModel, options?: UseFetchOptions<ThemeModel>) =>
  fetchController.put<ThemeModel>("/private/users/themes/" + id.toString() + "/", theme, ThemeModel, options);

export const deleteTheme = (id: number, options?: UseFetchOptions<ThemeModel>) =>
  fetchController.delete<ThemeModel>("/private/users/themes/" + id.toString() + "/", ThemeModel, options);
