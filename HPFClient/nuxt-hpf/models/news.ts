import { Type } from "class-transformer";
import { CommentData, NewsData } from "~/types/news";
import { AuthorData } from "~/types/users";

// #region Comment
export class CommentModel extends CommentData {
  @Type(() => AuthorData)
  public author: AuthorData | null = null;
}
// #endregion

// #region News
export class NewsModel extends NewsData {
  @Type(() => AuthorData)
  public authors: AuthorData[] | null = null;

  @Type(() => CommentModel)
  public comments: CommentModel[] | null = null;
}
// #endregion
