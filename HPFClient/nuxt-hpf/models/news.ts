import { Type } from "class-transformer";
import { CommentData, NewsData } from "~/types/news";
import { AuthorData } from "~/types/users";
import { ImageHPFData } from "~/types/images";

// #region Comment
export class CommentModel extends CommentData {
  @Type(() => AuthorData)
  public author: AuthorData | null = null;
  public content_images: ImageHPFData[] | null = null;
}
// #endregion

// #region News
export class NewsModel extends NewsData {
  @Type(() => AuthorData)
  public authors: AuthorData[] | null = null;

  @Type(() => CommentModel)
  public comments: CommentModel[] | null = null;

  public comment_count: number = 0;
}
// #endregion
