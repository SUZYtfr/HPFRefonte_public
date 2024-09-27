
import { Type, Exclude } from "class-transformer";
import { getModule } from "vuex-module-decorators";
import { CharacteristicModel } from "./characteristics";
import { BasicClass } from "~/types/basics";
import { FanfictionData, SerieData, ChapterData, ReviewData } from "~/types/fanfictions";
import { AuthorData } from "~/types/users";
import { ImageHPFData } from "~/types/images";
import { CharacteristicData } from "~/types/characteristics";
import Config from "~/store/modules/Config";

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
  public wordCount: number | null = null;
  public firstChapter: { id: number, title: string, order: number } | null = null;
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

  @Exclude()
  public _triggerWarningsLoaded: { id: number, caption: string }[] | null = null;

  @Exclude()
  public get triggerWarnings_loaded(): { id: number, caption: string }[] | null {
    if (this._triggerWarningsLoaded == null && process.client === true) {
      const ConfigModule = getModule(Config, window.$nuxt.$store);
      if (
        ConfigModule.characteristicTypes.length === 0 ||
        ConfigModule.characteristics.length === 0
      ) {
        LoadConfigAsync(ConfigModule);
      }
      return ConfigModule.characteristics.filter(t => t.characteristicTypeId === 4 && this.triggerWarnings.includes(t.characteristicId)).map((x: CharacteristicData) => ({ id: x.characteristicId, caption: x.name }));
    }
    return this._triggerWarningsLoaded;
  }
}

async function LoadConfigAsync(ConfigModule: Config): Promise<void> {
  await ConfigModule.LoadConfig();
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
  public _triggerWarningsLoaded: { id: number, caption: string }[] | null = null;

  @Exclude()
  public get triggerWarnings_loaded(): { id: number, caption: string }[] {
    if (this._triggerWarningsLoaded == null && process.client === true) {
      const ConfigModule = getModule(Config, window.$nuxt.$store);
      if (
        ConfigModule.characteristicTypes.length === 0 ||
        ConfigModule.characteristics.length === 0
      ) {
        LoadConfigAsync(ConfigModule);
      }
      return ConfigModule.characteristics.filter(t => t.characteristicTypeId === 4 && this.triggerWarnings.includes(t.characteristicId)).map((x: CharacteristicData) => ({ id: x.characteristicId, caption: x.name }));
    }
    return this._triggerWarningsLoaded != null ? this._triggerWarningsLoaded : [];
  }

  @Exclude()
  public get titleAsSlug(): string {
    return this.title?.toLowerCase().replace(/ /g, "-") ?? this.chapterId.toString();
  }
}
// #endregion
