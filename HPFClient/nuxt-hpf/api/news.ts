/* eslint-disable @typescript-eslint/explicit-function-return-type */

import fetchController from "~/utils/api";
import type { IBasicQuery, Paginated } from "@/types/basics";
import { CommentModel, NewsModel } from "~/models/news";
import type { CommentData } from "@/types/news";
import type { UseFetchOptions } from "nuxt/app";

export const searchNews = (
  filters: IBasicQuery | null | undefined,
  options?: UseFetchOptions<Paginated<NewsModel[]>>,
) => fetchController.get<Paginated<NewsModel[]>>("/news/", filters, NewsModel, options);

export const getNews = (id: number, options?: UseFetchOptions<NewsModel>) =>
  fetchController.get<NewsModel>(`/news/${id.toString()}/`, null, NewsModel, options);

export const postComment = (news_id: number, comment: CommentData, options?: UseFetchOptions<CommentModel>) =>
  fetchController.post<CommentModel>(`/news/${news_id.toString()}/comments/`, comment, CommentModel, options);
