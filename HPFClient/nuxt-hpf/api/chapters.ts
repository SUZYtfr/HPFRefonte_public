import $UseFetchWrapper from "~/utils/api";
import { ChapterModel } from "~/models/fanfictions";

export const getChapters = (id: number): Promise<any> => $UseFetchWrapper.get<ChapterModel>("/fictions/chapters/" + id.toString() + "/", null, ChapterModel);
export const postChapters = (chapter: ChapterModel): Promise<any> => $UseFetchWrapper.post<ChapterModel>("/fictions/chapters/", chapter, ChapterModel);
export const putChapters = (id: number, chapter: ChapterModel): Promise<any> => $UseFetchWrapper.put<ChapterModel>("/fictions/chapters/" + id.toString() + "/", chapter, ChapterModel);
export const deleteChapters = (id: number): Promise<any> => $UseFetchWrapper.delete<ChapterModel>("/fictions/chapters/" + id.toString() + "/", ChapterModel);
