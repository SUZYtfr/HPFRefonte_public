import { AuthorData } from "./users";
import { CommentData } from "./comments";

export class NewsData {
    news_id: number | null = null;
    title: string | null = null;
    content: string | null = null;
    status: number | null = null;
    post_date: Date | null = null;
    authors: AuthorData[] | null = null;
    comments: CommentData[] | null = null;
  }

  export interface NewsFiltersData {
    searchTerm: string,
    searchAuthor: string,
    searchAuthorId: number,
    sortBy: string,
    status: boolean | null,
    fromDate: Date | null,
    toDate: Date | null,
    currentPage: number,
    perPage: number,
  }