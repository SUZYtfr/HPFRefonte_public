import { AuthorData } from "./users";
import { CommentData } from "./comments";
import { QueryParams, PaginatedResponse } from "@/types/basics"

export interface TeamData {
  id: number;
  name: string;
}

export interface NewsData {
  id: number;
  title: string;
  content: string;
  status: number;
  post_date: Date;
  authors?: AuthorData[];
  teams?: TeamData[];
  comments?: CommentData[];
  category: string;
}

export interface NewsQueryParams extends QueryParams {
  searchTerm?: string;
  searchAuthor?: string;
  searchAuthorId?: number;
  sortBy?: string;
  status?: boolean;
  fromDate?: Date;
  toDate?: Date;
}

export interface NewsResponse extends PaginatedResponse {
  results: NewsData[];
}
