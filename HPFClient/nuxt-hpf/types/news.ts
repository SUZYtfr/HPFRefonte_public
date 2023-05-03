
import { Exclude, Transform } from "class-transformer";
import { BasicClass, IBasicQuery } from "./basics";

// #region News
enum NewsStatus {
  Pending = 1,
  Posted = 2,
  ToPost = 3,
}

export class NewsData extends BasicClass<NewsData> {
  @Exclude()
  public get news_id(): number {
    return this.id;
  }

  public title: string = "";
  public content: string = "";
  public status: NewsStatus = NewsStatus.Pending;

  @Transform(({ value }) => new Date(value), { toClassOnly: true })
  @Transform(({ value }) => (value?.toISOString() ?? ""), { toPlainOnly: true })
  public post_date: Date | null = null;
}

export interface INewsFilters extends IBasicQuery {
  searchTerm: string,
  searchAuthor: string,
  searchAuthorId: number,
  status: boolean | null,
  fromDate: Date | null,
  toDate: Date | null,
}
// #endregion

// #region Comment
export class CommentData extends BasicClass<CommentData> {
  @Exclude()
  public get comment_id(): number {
    return this.id;
  }

  public news_id: number = 0;
  public user_id: number = 0;
  public content: string = "";

  @Transform(({ value }) => new Date(value), { toClassOnly: true })
  @Transform(({ value }) => (value?.toISOString() ?? ""), { toPlainOnly: true })
  public post_date: Date | null = null;
}
// #endregion
