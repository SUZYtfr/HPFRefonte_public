import { Type } from "class-transformer";
import { CommentData, NewsData } from "@/types/news.ts";
import { AuthorData } from "@/types//users.ts";
import type { ImageHPFData } from "@/types/images.ts";

// #region Comment
export class CommentModel extends CommentData {
  @Type(() => AuthorData)
  public author: AuthorData | null = null;

  public contentImages: ImageHPFData[] | null = null;

  constructor(init?: Partial<CommentModel>) {
    super();
    Object.assign(this, init);
  }
}
// #endregion

// #region News
export class NewsModel extends NewsData {
  @Type(() => AuthorData)
  public authors: AuthorData[] | null = null;

  @Type(() => CommentModel)
  public comments: CommentModel[] | null = null;

  public commentCount: number = 0;

  constructor(init?: Partial<NewsModel>) {
    super();
    Object.assign(this, init);
  }
}
// #endregion
