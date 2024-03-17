import { Transform, Exclude } from "class-transformer";
import { BasicClass, IBasicQuery } from "./basics";

// #region Fanfiction
export enum FanfictionStatus {
  OnGoing = 1,
  Paused = 2,
  Abandoned = 3,
  Finished = 4,
}

export enum ValidationStatus {
  Unvalidated = 0,
  AwaitingCorrection = 2,
  Validated = 3,
}

export class FanfictionData extends BasicClass<FanfictionData> {
  @Exclude()
  public get fanfiction_id(): number {
    return this.id;
  }

  public title: string = "";
  public summary: string | null = null;
  public image: string | null = null;
  public average: number | null = null;
  public storynote: string | null = null;

  @Transform(({ value }) => new Date(value), { toClassOnly: true })
  @Transform(({ value }) => { return ((value instanceof Date) ? value.toISOString() : value); }, { toPlainOnly: true })
  public last_update_date: Date = new Date();

  public read_count: number | null = null;
  public word_count: number | null = null;
  public review_count: number | null = null;
  public collection_count: number | null = null;
  public status: FanfictionStatus = FanfictionStatus.OnGoing;
  public featured: boolean = false;
  public validation_status: ValidationStatus = ValidationStatus.Unvalidated;

  @Exclude()
  public get statusAsText(): string {
    let result: string = "";
    switch (this.status) {
      case 1:
        result = "Mise à jour";
        break;
      case 2:
        result = "Arrêtée";
        break;
      case 3:
        result = "Abandonnée";
        break;
      case 4:
        result = "Terminée";
        break;
    }
    return result;
  }

  @Exclude()
  public get titleAsSlug(): string {
    return this.title.toLowerCase().replace(/ /g, "-");
  }
}

export interface IFanfictionFilters extends IBasicQuery {
  searchTerm: string | null,
  searchAuthor: string | null,
  searchAuthorId: number | null,
  multipleAuthors: boolean | null,
  status: FanfictionStatus | null,
  wordCount_min: number | null,
  wordCount_max: number | null,
  includedTags: number[],
  excludedTags: number[],
  customTags: number[],
  featured: boolean | null,
  inclusive: boolean,
  fromDate: Date | null,
  toDate: Date | null,
}
// #endregion

// #region Reviews
export enum ReviewItemTypeEnum {
  Fanfiction = 1,
  Chapter = 2,
  Serie = 3,
  Author = 4,
}

export class ReviewData extends BasicClass<ReviewData> {
  @Exclude()
  public get review_id(): number {
    return this.id;
  }

  public item_id: number = 0;
  public review_item_type_id: ReviewItemTypeEnum = ReviewItemTypeEnum.Chapter;
  public user_id: number | null = null;
  public group_id: number | null = null;
  public grading: number | null = null;
  public text: string = "";
  public parent_id: number | null = null;
  public is_draft: boolean = false;

  @Transform(({ value }) => new Date(value), { toClassOnly: true })
  @Transform(({ value }) => { return ((value instanceof Date) ? value.toISOString() : value); }, { toPlainOnly: true })
  public post_date: Date | null = null;
}

// Est-ce que finalement ça sert à quelque chose ?
export interface IReviewFilters extends IBasicQuery {
  review_item_type_id: ReviewItemTypeEnum,
  item_id: number,
}
// #endregion

// #region  Serie
enum SerieStatusEnum {
  Closed = 1,
  Moderated = 2,
  Opened = 3,
}

export class SerieData extends BasicClass<SerieData> {
  @Exclude()
  public get serie_id(): number {
    return this.id;
  }

  public title: string = "";
  public summary: string | null = null;
  public parent_id: number | null = null;
  public status: SerieStatusEnum = SerieStatusEnum.Closed;
}
// #endregion

// #region  Chapter
enum ChapterValidationStatusEnum {
  Draft = 1,
  BetaPending = 2,
  BetaCompleted = 3,
  AwaitingValidation = 4,
  AwaitingModification = 5,
  Modified = 6,
  Published = 7,
}

export class ChapterData extends BasicClass<ChapterData> {
  @Exclude()
  public get chapter_id(): number {
    return this.id;
  }

  public title: string = "";
  public fiction: number | null = null;

  public creation_user: number | null = null;
  @Transform(({ value }) => new Date(value), { toClassOnly: true })
  @Transform(({ value }) => { return ((value instanceof Date) ? value.toISOString() : value); }, { toPlainOnly: true })
  public creation_date: Date = new Date();

  public modification_user: number | null = null;
  @Transform(({ value }) => new Date(value), { toClassOnly: true })
  @Transform(({ value }) => { return ((value instanceof Date) ? value.toISOString() : value); }, { toPlainOnly: true })
  public modification_date: Date = new Date();

  public startnote: string = "";
  public endnote: string = "";
  public order: number | null = null;

  public validation_status: ChapterValidationStatusEnum = ChapterValidationStatusEnum.Draft;
  public word_count: number | null = null;
  public read_count: number | null = null;
  public review_count: number | null = null;
  public average: number | null = null;

  @Exclude()
  public get titleAsSlug(): string {
    return this.title.toLowerCase().replace(/ /g, "-");
  }
}
// #endregion
