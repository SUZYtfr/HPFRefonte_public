import $AxiosWrapper from "~/utils/api";
import { ChapterModel } from "~/models/fanfictions";

export const getChapters = (id: number): Promise<any> => $AxiosWrapper.get<ChapterModel>("/fictions/chapters/" + id.toString() + "/", null, ChapterModel);
export const postChapters = (chapter: ChapterModel): Promise<any> => $AxiosWrapper.post<ChapterModel>("/fictions/chapters/", chapter, ChapterModel);
export const putChapters = (id: number, chapter: ChapterModel): Promise<any> => $AxiosWrapper.put<ChapterModel>("/fictions/chapters/" + id.toString() + "/", chapter, ChapterModel);
export const deleteChapters = (id: number): Promise<any> => $AxiosWrapper.delete<ChapterModel>("/fictions/chapters/" + id.toString() + "/", ChapterModel);
