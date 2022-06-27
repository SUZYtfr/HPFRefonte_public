import { ICharacteristic } from "./characteristics";
import { AuthorData } from "./users";
import { CommentData } from "./comments";

export class FanfictionData {
  fanfiction_id: number | null = null;
  last_update_date: Date | null = null;
  creation_date: Date | null = null;
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
  minWords: number | null,
  maxWords: number | null,
  includedTags: number[],
  excludedTags: number[],
  customTags: number[],
  featured: boolean | null,
  inclusive: boolean,
  fromDate: Date | null,
  toDate: Date | null,
  currentPage: number,
  perPage: number,
}

interface SerieData {
  serie_id: number,
  title: string
}