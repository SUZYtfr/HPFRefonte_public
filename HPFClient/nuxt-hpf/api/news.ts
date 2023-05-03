import $AxiosWrapper from "~/utils/api";
import { IBasicQuery } from "@/types/basics";
import { CommentModel, NewsModel } from "~/models/news";
import { CommentData, NewsData } from "@/types/news";

export const searchNews = (filters: IBasicQuery | null): Promise<any> => $AxiosWrapper.get<NewsModel>("/news", filters, NewsModel);
export const getNews = (id: number): Promise<any> => $AxiosWrapper.get<NewsModel>("/news/" + id.toString(), null, NewsModel);
export const postNews = (news: NewsData): Promise<any> => $AxiosWrapper.post<NewsModel>("/news", news, NewsModel);
export const putNews = (id: number, news: NewsData): Promise<any> => $AxiosWrapper.put<NewsModel>("/news/" + id.toString(), news, NewsModel);
export const deleteNews = (id: number): Promise<any> => $AxiosWrapper.delete<NewsModel>("/news/" + id.toString(), NewsModel);

export const postComment = (news_id: number, comment: CommentData): Promise<any> => $AxiosWrapper.post<CommentModel>("/news/" + news_id.toString() + "/comments", comment, CommentModel);
