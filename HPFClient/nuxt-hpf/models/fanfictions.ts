
import { Type } from "class-transformer";
import { FanfictionData, ReviewData, SerieData } from "~/types/fanfictions";
import { AuthorData } from "~/types/users";
import { CharacteristicData } from "~/types/characteristics";

// #region Review
export class ReviewModel extends ReviewData {
  @Type(() => AuthorData)
  public authors: AuthorData[] | null = null;
}
// #endregion

// #region Serie
export class SerieModel extends SerieData {
  @Type(() => AuthorData)
  public authors: AuthorData[] | null = null;
}
// #endregion

// #region Fanfiction
export class FanfictionModel extends FanfictionData {
  @Type(() => AuthorData)
  public authors: AuthorData[] | null = null;

  @Type(() => ReviewModel)
  public reviews: ReviewModel[] | null = null;

  @Type(() => CharacteristicData)
  public characteristics: CharacteristicData[] | null = null;

  @Type(() => SerieModel)
  public series: SerieModel[] | null = null;

  public chapter_count: number | null = null;
  public word_count: number | null = null;
}
// #endregion
