import { Type, Exclude } from "class-transformer";
import { BasicClass } from "~/types/basics";
import { FanfictionData, SerieData, ChapterData, ReviewData, VersionData } from "~/types/fanfictions";
import { AuthorData, UserData } from "~/types/users";
import { ImageHPFData } from "~/types/images";
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

  public chapterCount: number | null = null;
  public firstChapter: { id: number; title: string; order: number } | null = null;

  constructor(init?: Partial<FanfictionModel>) {
    super();
    Object.assign(this, init);
  }
}

export class FanfictionModelLight extends BasicClass<FanfictionModelLight> {
  @Exclude()
  public get fanfictionId(): number {
    return this.id;
  }

  public title: string | null = null;

  @Exclude()
  public get titleAsSlug(): string {
    return this.title?.toLowerCase().replace(/ /g, "-") ?? this.fanfictionId.toString();
  }
}

export class TableOfContent extends BasicClass<TableOfContent> {
  @Exclude()
  public get fanfictionId(): number {
    return this.id;
  }

  public title: string | null = null;
  public storynote: string | null = null;

  @Type(() => ChapterModelLight)
  public chapters: ChapterModelLight[] | null = null;

  @Exclude()
  public get titleAsSlug(): string {
    return this.title?.toLowerCase().replace(/ /g, "-") ?? this.fanfictionId.toString();
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

  public triggerWarnings: number[] = [];

  // TODO à transformer en type un peu plus light quand on saura exactement de quoi on a besoin
  @Type(() => FanfictionModel)
  public fictionMetadata: FanfictionModel | null = null;

  @Type(() => VersionModel)
  public currentVersion: VersionModel | null = null;

  @Exclude()
  public _triggerWarningsLoaded: { id: number; caption: string }[] | null = null;

  @Exclude()
  public get triggerWarningsLoaded(): { id: number; caption: string }[] | null {
    if (this._triggerWarningsLoaded == null && import.meta.client === true) {
      return (
        useConfigStore()
          .characteristics?.filter(
            (t: CharacteristicData) =>
              t.characteristicTypeId === 4 && this.triggerWarnings.includes(t.characteristicId),
          )
          .map((x: CharacteristicData) => ({ id: x.characteristicId, caption: x.name })) ?? []
      );
    }
    return this._triggerWarningsLoaded;
  }

  constructor(init?: Partial<ChapterModel>) {
    super();
    Object.assign(this, init);
  }
}

export class ChapterModelLight extends BasicClass<ChapterModelLight> {
  @Exclude()
  public get chapterId(): number {
    return this.id;
  }

  public title: string | null = null;
  public order: number = 0;
  public triggerWarnings: number[] = [];

  @Exclude()
  public _triggerWarningsLoaded: { id: number; caption: string }[] | null = null;

  @Exclude()
  public get triggerWarningsLoaded(): { id: number; caption: string }[] {
    if (this._triggerWarningsLoaded == null && import.meta.client === true) {
      return (
        useConfigStore()
          .characteristics?.filter(
            (t: CharacteristicData) =>
              t.characteristicTypeId === 4 && this.triggerWarnings.includes(t.characteristicId),
          )
          .map((x: CharacteristicData) => ({ id: x.characteristicId, caption: x.name })) ?? []
      );
    }
    return this._triggerWarningsLoaded != null ? this._triggerWarningsLoaded : [];
  }

  @Exclude()
  public get titleAsSlug(): string {
    return this.title?.toLowerCase().replace(/ /g, "-") ?? this.chapterId.toString();
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
