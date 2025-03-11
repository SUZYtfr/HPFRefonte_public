import fetchController from "~/utils/api";
import { IBasicQuery } from "@/types/basics";
import { FanfictionModel, TableOfContent } from "~/models/fanfictions";
import { FanfictionData } from "@/types/fanfictions";
import type { Paginated } from "@/types/basics";


export const searchFanfictions = (filters: IBasicQuery | null | undefined) => fetchController.get<Paginated<FanfictionModel[]>>("/fictions/fictions/", filters, FanfictionModel);
export const getFanfiction = (id: number) => fetchController.get<FanfictionModel>("/fictions/fictions/" + id.toString() + "/", null, FanfictionModel);
export const getTableOfContent = (id: number) => fetchController.get<TableOfContent>("/fictions/fictions/" + id.toString() + "/table-of-contents/", null, TableOfContent);
export const postFanfictions = (fanfiction: FanfictionData) => fetchController.post<FanfictionModel>("/fictions/fictions/", fanfiction, FanfictionModel);
export const putFanfictions = (id: number, fanfiction: FanfictionData) => fetchController.put<FanfictionModel>("/fictions/fictions/" + id.toString() + "/", fanfiction, FanfictionModel);
export const deleteFanfictions = (id: number) => fetchController.delete<FanfictionModel>("/fictions/fictions/" + id.toString() + "/", FanfictionModel);
