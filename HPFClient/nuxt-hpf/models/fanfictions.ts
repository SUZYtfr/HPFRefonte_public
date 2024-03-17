
import { Type, Exclude } from "class-transformer";
import { getModule } from "vuex-module-decorators";
import { CharacteristicModel } from "./characteristics";
import { BasicClass } from "~/types/basics";
import { FanfictionData, ReviewData, SerieData, ChapterData } from "~/types/fanfictions";
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

  public chapter_count: number | null = null;
  public word_count: number | null = null;
  public first_chapter: { id: number, title: string, order: number } | null = null;
}

export class TableOfContent extends BasicClass<TableOfContent> {
  @Exclude()
  public get fanfiction_id(): number {
    return this.id;
  }

  public title: string | null = null;
  public storynote: string | null = null;

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

  public text: string | null = null;

  @Type(() => ImageHPFData)
  public text_images: ImageHPFData[] | null = null;

  public trigger_warnings: number[] = [];

  @Exclude()
  public _trigger_warnings_loaded: { id: number, caption: string }[] | null = null;

  @Exclude()
  public get trigger_warnings_loaded(): { id: number, caption: string }[] | null {
    if (this._trigger_warnings_loaded == null && process.client === true) {
      const ConfigModule = getModule(Config, window.$nuxt.$store);
      if (
        ConfigModule.characteristicTypes.length === 0 ||
        ConfigModule.characteristics.length === 0
      ) {
        LoadConfigAsync(ConfigModule);
      }
      return ConfigModule.characteristics.filter(t => t.characteristic_type_id === 4 && this.trigger_warnings.includes(t.characteristic_id)).map((x: CharacteristicData) => ({ id: x.characteristic_id, caption: x.name }));
    }
    return this._trigger_warnings_loaded;
  }
}

async function LoadConfigAsync(ConfigModule: Config): Promise<void> {
  await ConfigModule.LoadConfig();
}

export class ChapterModelLight extends BasicClass<ChapterModelLight> {
  @Exclude()
  public get chapter_id(): number {
    return this.id;
  }

  public title: string | null = null;
  public order: number = 0;
  public trigger_warnings: number[] = [];

  @Exclude()
  public _trigger_warnings_loaded: { id: number, caption: string }[] | null = null;

  @Exclude()
  public get trigger_warnings_loaded(): { id: number, caption: string }[] {
    if (this._trigger_warnings_loaded == null && process.client === true) {
      const ConfigModule = getModule(Config, window.$nuxt.$store);
      if (
        ConfigModule.characteristicTypes.length === 0 ||
        ConfigModule.characteristics.length === 0
      ) {
        LoadConfigAsync(ConfigModule);
      }
      return ConfigModule.characteristics.filter(t => t.characteristic_type_id === 4 && this.trigger_warnings.includes(t.characteristic_id)).map((x: CharacteristicData) => ({ id: x.characteristic_id, caption: x.name }));
    }
    return this._trigger_warnings_loaded != null ? this._trigger_warnings_loaded : [];
  }

  @Exclude()
  public get titleAsSlug(): string {
    return this.title?.toLowerCase().replace(/ /g, "-") ?? this.chapter_id.toString();
  }
}
// #endregion
