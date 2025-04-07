import $AxiosWrapper from "~/utils/api";
import { ThemeModel } from "~/models/themes";
import { IBasicQuery } from "@/types/basics";
import { Paginated } from "@/types/basics";

export const searchThemes = (filters: IBasicQuery | null) => $AxiosWrapper.get<Paginated<ThemeModel[]>>("/users/themes/", filters, ThemeModel);
