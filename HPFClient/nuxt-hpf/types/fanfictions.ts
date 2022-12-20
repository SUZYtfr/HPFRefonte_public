import { QueryParams, PaginatedResponse } from "@/types/basics"
import { ICharacteristic } from "@/types/characteristics"
import { AuthorData } from "@/types/users"
import { CommentData } from "@/types/comments"

export class FanfictionData {
  id: number | null = null;
  last_update_date: Date | null = null;
  creation_date: Date | null = null;
  title: string | null = null;
  summary: string | null = null;
  authors: AuthorData[] | null = null;
  creation_user: AuthorData | null = null;
  review_count: number | null = null;
  features: ICharacteristic[] | null = null;
  series: SerieData[] | null = null;
  mean: number | null = null;
  chapter_count: number | null = null;
  word_count: number | null = null;
  read_count: number | null = null;
  status: number | null = null;
  featured: boolean | null = null;
}

export interface FanfictionQueryParams extends QueryParams {
  title?: string;
  author?: string;
  searchAuthorId?: number;
  sortBy?: string;
  multipleAuthors?: boolean;
  status?: boolean;
  minWords?: number;
  maxWords?: number;
  includedTags?: number[];
  excludedTags?: number[];
  customTags?: number[];
  featured?: boolean;
  inclusive?: boolean;
  fromDate?: Date;
  toDate?: Date;
}

export interface FanfictionResponse extends PaginatedResponse {
  results: FanfictionData[];
}

interface SerieData {
  serie_id: number,
  title: string
}