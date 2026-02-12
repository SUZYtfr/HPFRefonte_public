import { Exclude, Transform } from "class-transformer";
import { BasicClass } from "./basics";

// #region News
enum NewsStatus {
  Pending = 1,
  Posted = 2,
  ToPost = 3,
}

export class NewsData extends BasicClass<NewsData> {
  @Exclude()
  public get newsId(): number {
    return Number(this.id);
  }

  public title: string = "";
  public content: string = "";
  public status: NewsStatus = NewsStatus.Pending;

  @Transform(
    ({ value }) => {
      return value != null ? new Date(value) : null;
    },
    { toClassOnly: true },
  )
  @Transform(
    ({ value }) => {
      return value instanceof Date ? value.toISOString() : value;
    },
    { toPlainOnly: true },
  )
  public postDate: Date | null = null;
}


// #region Comment
export class CommentData extends BasicClass<CommentData> {
  @Exclude()
  public get commentId(): number {
    return Number(this.id);
  }

  public newsId: number = 0;
  public userId: number = 0;
  public content: string = "";

  @Transform(
    ({ value }) => {
      return value != null ? new Date(value) : null;
    },
    { toClassOnly: true },
  )
  @Transform(
    ({ value }) => {
      return value instanceof Date ? value.toISOString() : value;
    },
    { toPlainOnly: true },
  )
  public postDate: Date | null = null;
}
// #endregion
