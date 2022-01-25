import { ICharacteristic } from "./characteristics";

export class FanfictionData {
  fanfiction_id: number | null = null;
  last_update_date: number | null = null;
  creation_date: number | null = null;
  title: string | null = null;
  summary: string | null = null;
  authors: AuthorData[] | null = null;
  comments: CommentData[] | null = null;
  characteristics: ICharacteristic[] | null = null;
  series: SerieData[] | null = null;
  rating: number | null = null;
  chapter_count: number | null = null;
  word_count: number | null = null;
  read_count: number | null = null;
  status: number | null = null;
  featured: boolean | null = null;
}

export interface FanfictionFiltersData {
  searchTerm: string,
  searchAuthor: string,
  searchAuthorId: number,
  sortBy: string,
  multipleAuthors: boolean | null,
  status: boolean | null,
  words: number[],
  includedTags: number[],
  excludedTags: number[],
  customTags: number[],
  featured: boolean | null,
  inclusive: boolean,
  fromDate: Date | null,
  toDate: Date | null,
}

interface AuthorData {
  author_id: number,
  nickname: string
}

interface CommentData {
  comment_id: number,
  post_date: Date,
  content: string,
  authors: AuthorData[],
}

interface SerieData {
  serie_id: number,
  title: string
}