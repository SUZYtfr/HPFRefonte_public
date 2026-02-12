import { Transform, Exclude } from "class-transformer";
import { BasicClass } from "./basics";

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
    return Number(this.id);
  }

  public title: string = "";
  public summary: string | null = null;
  public image: string | null = null;
  public average: number | null = null;
  public storynote: string | null = null;

  @Transform(({ value }) => new Date(value), { toClassOnly: true })
  @Transform(
    ({ value }) => {
      return value instanceof Date ? value.toISOString() : value;
    },
    { toPlainOnly: true },
  )
  public lastUpdateDate: Date = new Date();

  public readCount: number | null = null;
  public wordCount: number | null = null;
  public reviewCount: number | null = null;
  public collectionCount: number | null = null;
  public status: FanfictionStatus = FanfictionStatus.OnGoing;
  public featured: boolean = false;
  public validationStatus: ValidationStatus = ValidationStatus.Unvalidated;
  public watched: boolean = false;

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

  constructor(init?: Partial<FanfictionData>) {
    super();
    Object.assign(this, init);
  }
}

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
    return Number(this.id);
  }

  public itemId: number = 0;
  public reviewItemTypeId: ReviewItemTypeEnum = ReviewItemTypeEnum.Chapter;
  public userId: number | null = null;
  public groupId: number | null = null;
  public grading: number | null = null;
  public text: string = "";
  public parentId: number | null = null;
  public isDraft: boolean = false;
  public isArchived: boolean = false;

  @Transform(({ value }) => new Date(value), { toClassOnly: true })
  @Transform(
    ({ value }) => {
      return value instanceof Date ? value.toISOString() : value;
    },
    { toPlainOnly: true },
  )
  public postDate: Date | null = null;
}

// #region  Serie
enum SerieStatusEnum {
  Closed = 1,
  Moderated = 2,
  Opened = 3,
}

export class SerieData extends BasicClass<SerieData> {
  @Exclude()
  public get serieId(): number {
    return Number(this.id);
  }

  public title: string = "";
  public summary: string | null = null;
  public parentId: number | null = null;
  public status: SerieStatusEnum = SerieStatusEnum.Closed;
}
// #endregion

export enum ChapterValidationStatusEnum {
  Draft = 1,
  BetaPending = 2,
  BetaCompleted = 3,
  AwaitingValidation = 4,
  AwaitingModification = 5,
  Modified = 6,
  Published = 7,
  AwaitingDiscussion = 8,
}

export class ChapterData extends BasicClass<ChapterData> {
  @Exclude()
  public get chapterId(): number {
    return Number(this.id);
  }

  public title: string = "";
  public fiction: number | null = null;

  public creationUser: number | null = null;
  @Transform(({ value }) => new Date(value), { toClassOnly: true })
  @Transform(
    ({ value }) => {
      return value instanceof Date ? value.toISOString() : value;
    },
    { toPlainOnly: true },
  )
  public submissionDate: Date | null = null;

  public modificationUser: number | null = null;

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

export class VersionData extends BasicClass<VersionData> {
  @Exclude()
  public get versionId(): number {
    return Number(this.id);
  }

  // Chapitre Id auquel est liée la version
  public chapterId: number | null = null;

  // Auteur Id de cette version
  public authorId: number | null = null;

  // Date de dernière modification de cette version
  @Transform(({ value }) => new Date(value), { toClassOnly: true })
  @Transform(
    ({ value }) => {
      return value instanceof Date ? value.toISOString() : value;
    },
    { toPlainOnly: true },
  )
  public versionDate: Date | null = null;

  // Nombre de mots dans cette version
  public words: number = 0;

  // Texte de cette version
  public text: string | null = null;

  // Commentaire public de la modération (visible par l'auteur)
  public publicComment: string | null = null;

  // Commentaire privé de la modération (visible par la modération uniquement)
  public privateComment: string | null = null;

  // Motif(s) d'invalidation
  public invalidationReasonIds: number[] | null = null;

  // Date d'invalidation de cette version
  @Transform(({ value }) => new Date(value), { toClassOnly: true })
  @Transform(
    ({ value }) => {
      return value instanceof Date ? value.toISOString() : value;
    },
    { toPlainOnly: true },
  )
  public invalidationDate: Date | null = null;

  // Utilisateur qui a invalidé cette version
  public invalidationUserId: number | null = null;
}

// Formulaire de validation d'un chapitre
export interface ChapterValidationData {
  // Commentaire public de la modération (visible par l'auteur)
  publicComment: string | null;
  // Commentaire privé de la modération (visible par la modération uniquement)
  privateComment: string | null;
  // Motif(s) d'invalidation
  invalidationReasonIds: number[];
}
// #endregion


export interface FandomData {
  id: string;
  name: string;
  slug: string;
}
