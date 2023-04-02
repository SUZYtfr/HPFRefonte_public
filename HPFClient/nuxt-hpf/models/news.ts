import { Type } from "class-transformer";
import { CommentData, NewsData } from "~/types/news";
import { UserData } from "~/types/users";

// #region Comment
export class CommentModel extends CommentData {
  @Type(() => UserData)
  public authors: UserData[] | null = null;
}
// #endregion

// #region News
export class NewsModel extends NewsData {
  @Type(() => UserData)
  public authors: UserData[] | null = null;

  @Type(() => CommentModel)
  public comments: CommentModel[] | null = null;
}
// #endregion
