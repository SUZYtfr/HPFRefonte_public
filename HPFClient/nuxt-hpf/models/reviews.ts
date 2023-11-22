import { Type } from "class-transformer";
import { ReviewData } from "~/types/reviews";
import { ChapterModelLight, FanfictionModelLight, SerieModel } from "./fanfictions";

export class ReviewModel extends ReviewData {
  @Type(() => ChapterModelLight)
  public chapter: ChapterModelLight | null = null;

  @Type(() => FanfictionModelLight)
  public fiction: FanfictionModelLight | null = null;

  @Type(() => SerieModel)
  public collection: SerieModel | null = null;

  @Type(() => ReviewModel)
  public replies: ReviewModel[] | null = null;
}