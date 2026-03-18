import { Type, Exclude, Transform, plainToInstance } from "class-transformer";
import { BasicClass } from "~/types/basics";
import {
  CollectionData,
  CollectionItemData,
  ChapterData,
  ReviewData,
  VersionData,
  FanfictionStatus,
  type FanfictionRating,
  type FandomData,
} from "~/types/fanfictions";
import { AuthorData, UserData } from "~/types/users";
import { ImageHPFData } from "~/types/images";
import { TriggerWarningData } from "~/types/characteristics";
import slugify from "slugify";
import { CharacteristicModel } from "~/models/characteristics";

export enum ValidationStatus {
  Unvalidated = 0,
  AwaitingCorrection = 2,
  Validated = 3,
}

// #region Review
export class ReviewModel extends ReviewData {
  @Type(() => AuthorData)
  public authors: AuthorData[] | null = null;
}
// #endregion

// #region Serie
export class CollectionModel extends CollectionData {
  @Type(() => AuthorData)
  public authors: AuthorData[] | null = null;

  @Type(() => CollectionItemData)
  public items: CollectionItemData[] | null = null;

  public itemCount: number | null = null;

  public fandoms: FandomData[] | null = null;

  @Type(() => CharacteristicModel)
  public characteristics: CharacteristicModel[] | null = null;

  constructor(init?: Partial<CollectionModel>) {
    super();
    Object.assign(this, init);
  }
}
// #endregion

// #region Fanfiction
export class FanfictionModel extends BasicClass<FanfictionModel> {
  @Exclude()
  public get fanfictionId(): number {
    return Number(this.id);
  }

  public title: string = "";
  public summary: string | null = null;
  public image: string | null = null;
  public average: number | null = null;
  public storynote: string | null = null;

  @Transform(({ value }) => (value ? new Date(value) : value), { toClassOnly: true })
  @Transform(
    ({ value }) => {
      return value instanceof Date ? value.toISOString() : value;
    },
    { toPlainOnly: true },
  )
  public lastUpdateDate: Date | null = null;

  public readCount: number | null = null;
  public wordCount: number | null = null;
  public reviewCount: number | null = null;
  public collectionCount: number | null = null;
  public status: FanfictionStatus = FanfictionStatus.ONGOING;
  public rating: FanfictionRating | null = null;

  public featured: boolean = false;
  public validationStatus: ValidationStatus = ValidationStatus.Unvalidated;
  public watched: boolean = false;

  @Exclude()
  public get titleAsSlug(): string {
    return slugify(this.title, { lower: true, locale: "fr", strict: true });
  }

  @Type(() => AuthorData)
  public authors: AuthorData[] | null = null;

  @Type(() => ReviewModel)
  public reviews: ReviewModel[] | null = null;

  @Type(() => CharacteristicModel)
  public characteristics: CharacteristicModel[] | null = null;

  @Type(() => TriggerWarningData)
  public triggerWarnings: TriggerWarningData[] | null = null;

  @Type(() => CollectionModel)
  public collections: CollectionModel[] | null = null;

  @Type(() => ChapterModel)
  @Transform(({ value }) => plainToInstance(ChapterModel, value?.results || value), { toClassOnly: true })
  public chapters: ChapterModel[] | null = null;

  public chapterCount: number | null = null;
  public firstChapter: { id: number; title: string; order: number } | null = null;

  public fandoms: FandomData[] | null = null;

  constructor(init?: Partial<FanfictionModel>) {
    super();
    Object.assign(this, init);
  }
}

export class FanfictionModelLight extends BasicClass<FanfictionModelLight> {
  @Exclude()
  public get fanfictionId(): number {
    return Number(this.id);
  }

  public title: string | null = null;

  @Exclude()
  public get titleAsSlug(): string {
    return slugify(this.title || this.fanfictionId.toString(), { lower: true, locale: "fr", strict: true });
  }
}

export class TableOfContent extends BasicClass<TableOfContent> {
  @Exclude()
  public get fanfictionId(): number {
    return Number(this.id);
  }

  public title: string | null = null;
  public storynote: string | null = null;

  @Type(() => ChapterModelLight)
  @Transform(({ value }) => plainToInstance(ChapterModelLight, value?.results || value), { toClassOnly: true })
  public chapters: ChapterModelLight[] | null = null;

  @Exclude()
  public get titleAsSlug(): string {
    return slugify(this.title || this.fanfictionId.toString(), { lower: true, locale: "fr", strict: true });
  }
}

export class FanfictionEntityConfig {
  public inList: boolean = true;

  public constructor(init?: Partial<FanfictionEntityConfig>) {
    Object.assign(this, init);
  }
}
// #endregion

// #region Chapter
export class ChapterModel extends ChapterData {
  @Type(() => AuthorData)
  public authors: AuthorData[] | null = null;

  @Type(() => ReviewModel)
  public reviews: ReviewModel[] | null = null;

  public text: string | null = null;

  @Type(() => ImageHPFData)
  public textImages: ImageHPFData[] | null = null;

  @Type(() => TriggerWarningData)
  public triggerWarnings: TriggerWarningData[] | null = null;

  @Transform(({ value }) => (value ? new Date(value) : value), { toClassOnly: true })
  @Transform(
    ({ value }) => {
      return value instanceof Date ? value.toISOString() : value;
    },
    { toPlainOnly: true },
  )
  public publicationDate: Date | null = null;

  // TODO à transformer en type un peu plus light quand on saura exactement de quoi on a besoin
  @Type(() => FanfictionModel)
  public fictionMetadata: FanfictionModel | null = null;

  @Type(() => VersionModel)
  public currentVersion: VersionModel | null = null;

  constructor(init?: Partial<ChapterModel>) {
    super();
    Object.assign(this, init);
  }
}

export class ChapterModelLight extends BasicClass<ChapterModelLight> {
  @Exclude()
  public get chapterId(): number {
    return Number(this.id);
  }

  public title: string | null = null;
  public order: number = 0;

  @Type(() => TriggerWarningData)
  public triggerWarnings: TriggerWarningData[] | null = null;

  @Exclude()
  public get titleAsSlug(): string {
    return slugify(this.title || this.chapterId.toString(), { lower: true, locale: "fr", strict: true });
  }
}

// Filtres des chapitres dans le batch
export interface BatchChapterFilters {
  searchTerm: string | null;
  awaitingDiscussionOnly: boolean;
  watchedAuthors: boolean;
}

// Model des Version incluant les auteurs en clair
export class VersionModel extends VersionData {
  @Type(() => AuthorData)
  public authors: AuthorData[] | null = null;

  // TODO un autre type plus light ?
  @Type(() => UserData)
  public invalidationUser: UserData | null = null;

  constructor(init?: Partial<VersionModel>) {
    super();
    Object.assign(this, init);
  }
}
// #endregion
