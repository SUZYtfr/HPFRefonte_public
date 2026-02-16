import { Type, Exclude, Transform } from "class-transformer";
import { AuthorData } from "~/types/users";
import type { ImageHPFData } from "~/types/images";
import { BasicClass } from "~/types/basics";

// #region Comment
export class CommentModel extends BasicClass<CommentModel> {
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

  @Type(() => AuthorData)
  public author: AuthorData | null = null;

  public contentImages: ImageHPFData[] | null = null;

  constructor(init?: Partial<CommentModel>) {
    super();
    Object.assign(this, init);
  }
}
// #endregion

enum NewsStatus {
  Pending = 1,
  Posted = 2,
  ToPost = 3,
}

// #region News
export class NewsModel extends BasicClass<NewsModel> {
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

  @Type(() => AuthorData)
  public authors: AuthorData[] | null = null;

  @Type(() => CommentModel)
  public comments: CommentModel[] | null = null;

  public commentCount: number = 0;
}
// #endregion
