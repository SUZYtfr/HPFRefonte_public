import $AxiosWrapper from "~/utils/api";
import { IBasicQuery } from "@/types/basics";
import { CommentModel, NewsModel } from "~/models/news";
import { CommentData, NewsData } from "@/types/news";

// export const searchNews = (filters: IBasicQuery | null | undefined): Promise<any> => $AxiosWrapper.get<NewsModel>("/news/", filters, NewsModel);
export const getNews = (id: number): Promise<any> => $AxiosWrapper.get<NewsModel>("/news/" + id.toString() + "/", null, NewsModel);
export const postNews = (news: NewsData): Promise<any> => $AxiosWrapper.post<NewsModel>("/news/", news, NewsModel);
export const putNews = (id: number, news: NewsData): Promise<any> => $AxiosWrapper.put<NewsModel>("/news/" + id.toString() + "/", news, NewsModel);
export const deleteNews = (id: number): Promise<any> => $AxiosWrapper.delete<NewsModel>("/news/" + id.toString() + "/", NewsModel);

// export const postComment = (newsId: number, comment: CommentData): Promise<any> => $AxiosWrapper.post<CommentModel>("/news/" + newsId.toString() + "/comments/", comment, CommentModel);

import $ApolloWrapper from "~/utils/apolloApi";
import paginatedNewsQuery from "./queries/paginatedNewsQuery.gql";
import postCommentMutation from "./queries/postCommentMutation.gql";

export const searchNews = (filters: IBasicQuery | null | undefined): Promise<any> => $ApolloWrapper.query<NewsModel>(paginatedNewsQuery, filters, "paginatedNewsArticles", NewsModel);
export const postComment = (newsId: number, comment: CommentData): Promise<any> => $ApolloWrapper.mutation<CommentModel>(postCommentMutation, comment, "comment", CommentModel);
