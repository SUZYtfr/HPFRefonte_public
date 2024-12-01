import $AxiosWrapper from "~/utils/api";
import { IBasicQuery } from "@/types/basics";
import { NewsModel } from "~/models/news";
import { NewsData } from "@/types/news";

export const searchNews = (filters: IBasicQuery | null | undefined): Promise<any> => $AxiosWrapper.get<NewsModel>(`/private/news/`, filters, NewsModel);
export const getNews = (id: number): Promise<any> => $AxiosWrapper.get<NewsModel>(`/private/news/${id.toString()}/`, null, NewsModel);
export const postNews = (news: NewsData): Promise<any> => $AxiosWrapper.post<NewsModel>(`/private/news/`, news, NewsModel);
export const putNews = (id: number, news: NewsData): Promise<any> => $AxiosWrapper.put<NewsModel>(`/private/news/${id.toString()}/`, news, NewsModel);
export const deleteNews = (id: number): Promise<any> => $AxiosWrapper.delete<NewsModel>(`/private/news/${id.toString()}/`, NewsModel);
