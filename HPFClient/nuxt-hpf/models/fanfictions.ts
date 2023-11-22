
import { Type, Exclude } from "class-transformer";
import { BasicClass } from "~/types/basics";
import { FanfictionData, SerieData, ChapterData } from "~/types/fanfictions";
import { AuthorData } from "~/types/users";
import { CharacteristicData } from "~/types/characteristics";
import { ReviewModel } from "./reviews";

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

export class FanfictionModelLight extends BasicClass<FanfictionModelLight> {
  @Exclude()
  public get fanfiction_id(): number {
    return this.id;
  }

  public title: string | null = null;

  @Exclude()
  public get titleAsSlug(): string {
    return this.title?.toLowerCase().replace(/ /g, "-") ?? this.fanfiction_id.toString();
  }
}

export class TableOfContent extends BasicClass<TableOfContent> {
  @Exclude()
  public get fanfiction_id(): number {
    return this.id;
  }

  public title: string | null = null;

  @Type(() => ChapterModelLight)
  public chapters: ChapterModelLight[] | null = null;

  @Exclude()
  public get titleAsSlug(): string {
    return this.title?.toLowerCase().replace(/ /g, "-") ?? this.fanfiction_id.toString();
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
}

export class ChapterModelLight extends BasicClass<ChapterModelLight> {
  @Exclude()
  public get chapter_id(): number {
    return this.id;
  }

  public title: string | null = null;
  public order: number = 0;

  @Exclude()
  public get titleAsSlug(): string {
    return this.title?.toLowerCase().replace(/ /g, "-") ?? this.chapter_id.toString();
  }
}
// #endregion
