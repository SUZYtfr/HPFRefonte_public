import $AxiosWrapper from "~/utils/api";
import { IBasicQuery } from "@/types/basics";
import { FanfictionModel } from "~/models/fanfictions";
import { FanfictionData } from "@/types/fanfictions";

export const searchFanfictions = (filters: IBasicQuery | null): Promise<any> => $AxiosWrapper.get<FanfictionModel>("/fanfictions", filters, FanfictionModel);
export const getFanfictions = (id: number): Promise<any> => $AxiosWrapper.get<FanfictionModel>("/fanfictions/" + id.toString(), FanfictionModel);
export const postFanfictions = (fanfiction: FanfictionData): Promise<any> => $AxiosWrapper.post<FanfictionModel>("/fanfictions", fanfiction, FanfictionModel);
export const putFanfictions = (id: number, fanfiction: FanfictionData): Promise<any> => $AxiosWrapper.put<FanfictionModel>("/fanfictions/" + id.toString(), fanfiction, FanfictionModel);
export const deleteFanfictions = (id: number): Promise<any> => $AxiosWrapper.delete<FanfictionModel>("/fanfictions/" + id.toString(), FanfictionModel);
