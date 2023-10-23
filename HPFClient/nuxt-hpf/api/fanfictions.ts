import $UseFetchWrapper from "~/utils/api";
import { IBasicQuery } from "@/types/basics";
import { FanfictionModel, TableOfContent } from "~/models/fanfictions";
import { FanfictionData } from "@/types/fanfictions";

export const searchFanfictions = (filters: IBasicQuery | null): Promise<any> => $UseFetchWrapper.get<FanfictionModel>("/fictions/fictions/", filters, FanfictionModel);
export const getFanfictions = (id: number): Promise<any> => $UseFetchWrapper.get<FanfictionModel>("/fictions/fictions/" + id.toString() + "/", null, FanfictionModel);
export const getTableOfContent = (id: number): Promise<any> => $UseFetchWrapper.get<TableOfContent>("/fictions/fictions/" + id.toString() + "/table-of-contents/", null, TableOfContent);
export const postFanfictions = (fanfiction: FanfictionData): Promise<any> => $UseFetchWrapper.post<FanfictionModel>("/fictions/fictions/", fanfiction, FanfictionModel);
export const putFanfictions = (id: number, fanfiction: FanfictionData): Promise<any> => $UseFetchWrapper.put<FanfictionModel>("/fictions/fictions/" + id.toString() + "/", fanfiction, FanfictionModel);
export const deleteFanfictions = (id: number): Promise<any> => $UseFetchWrapper.delete<FanfictionModel>("/fictions/fictions/" + id.toString() + "/", FanfictionModel);
