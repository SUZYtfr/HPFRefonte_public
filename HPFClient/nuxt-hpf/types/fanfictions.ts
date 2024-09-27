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
  public get fanfictionId(): number {
    return this.id;
  }

  public title: string = "";
  public summary: string | null = null;
  public image: string | null = null;
  public average: number | null = null;
  public storynote: string | null = null;

  @Transform(({ value }) => new Date(value), { toClassOnly: true })
  @Transform(({ value }) => { return ((value instanceof Date) ? value.toISOString() : value); }, { toPlainOnly: true })
  public lastUpdateDate: Date = new Date();

  public readCount: number | null = null;
  public wordCount: number | null = null;
  public reviewCount: number | null = null;
  public collectionCount: number | null = null;
  public status: FanfictionStatus = FanfictionStatus.OnGoing;
  public featured: boolean = false;
  public validationStatus: ValidationStatus = ValidationStatus.Unvalidated;

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
  public get reviewId(): number {
    return this.id;
  }

  public itemId: number = 0;
  public review_itemType_id: ReviewItemTypeEnum = ReviewItemTypeEnum.Chapter;
  public userId: number | null = null;
  public group_id: number | null = null;
  public grading: number | null = null;
  public text: string = "";
  public parentId: number | null = null;
  public is_draft: boolean = false;
  public is_archived: boolean = false;

  @Transform(({ value }) => new Date(value), { toClassOnly: true })
  @Transform(({ value }) => { return ((value instanceof Date) ? value.toISOString() : value); }, { toPlainOnly: true })
  public postDate: Date | null = null;
}

// Est-ce que finalement ça sert à quelque chose ?
export interface IReviewFilters extends IBasicQuery {
  searchTerm: string | null;
  includeItemTypes: ReviewItemTypeEnum[] | null;
  itemId: number | null;
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
  public get serieId(): number {
    return this.id;
  }

  public title: string = "";
  public summary: string | null = null;
  public parentId: number | null = null;
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
  public get chapterId(): number {
    return this.id;
  }

  public title: string = "";
  public fiction: number | null = null;

  public creationUser: number | null = null;
  @Transform(({ value }) => new Date(value), { toClassOnly: true })
  @Transform(({ value }) => { return ((value instanceof Date) ? value.toISOString() : value); }, { toPlainOnly: true })
  public creationDate: Date = new Date();

  public modification_user: number | null = null;
  @Transform(({ value }) => new Date(value), { toClassOnly: true })
  @Transform(({ value }) => { return ((value instanceof Date) ? value.toISOString() : value); }, { toPlainOnly: true })
  public modificationDate: Date = new Date();

  public startnote: string = "";
  public endnote: string = "";
  public order: number | null = null;

  public validationStatus: ChapterValidationStatusEnum = ChapterValidationStatusEnum.Draft;
  public wordCount: number | null = null;
  public readCount: number | null = null;
  public reviewCount: number | null = null;
  public average: number | null = null;

  @Exclude()
  public get titleAsSlug(): string {
    return this.title.toLowerCase().replace(/ /g, "-");
  }
}
// #endregion
