import fetchController from "~/utils/api";
import { IBasicQuery } from "@/types/basics";
import { CommentModel, NewsModel } from "~/models/news";
import { CommentData, NewsData } from "@/types/news";
import type { Paginated } from "@/types/basics";


export const searchNews = (filters: IBasicQuery | null | undefined) => fetchController.get<Paginated<NewsModel[]>>(`/news/`, filters, NewsModel);
export const getNews = (id: number) => fetchController.get<NewsModel>(`/news/${id.toString()}/`, null, NewsModel);

export const postComment = (news_id: number, comment: CommentData) => fetchController.post<CommentModel>(`/news/${news_id.toString()}/comments/`, comment, CommentModel);
