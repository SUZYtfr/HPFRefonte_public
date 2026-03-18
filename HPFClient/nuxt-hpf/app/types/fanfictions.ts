import { Transform, Exclude, Type } from "class-transformer";
import { BasicClass } from "./basics";
import slugify from "slugify";
import { FanfictionModel, ChapterModel, CollectionModel } from "~/models";
import { AuthorData } from "~/types/users";

// #region Fanfiction
export enum FanfictionStatus {
  ONGOING = "Mise à jour",
  PAUSED = "Arrêtée",
  ABANDONED = "Abandonnée",
  FINISHED = "Terminée",
}

export enum FanfictionRating {
  ALL = "tout public",
  P12 = "-12 ans",
  P16 = "-16 ans",
  P18 = "-18 ans",
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
  public status: FanfictionStatus = FanfictionStatus.ONGOING;
  public rating: FanfictionRating | null = null;
  public featured: boolean = false;
  public validationStatus: ValidationStatus = ValidationStatus.Unvalidated;
  public watched: boolean = false;

  @Exclude()
  public get titleAsSlug(): string {
    return slugify(this.title, { lower: true, locale: "fr", strict: true });
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
  Collection = 3,
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

export enum CollectionAccess {
  CLOSED = "Fermée",
  MODERATED = "Modérée",
  OPEN = "Ouverte",
}

export enum itemType {
  Chapter = "chapitre",
  Fiction = "fiction",
  Collection = "série",
}

export class CollectionData extends BasicClass<CollectionData> {
  @Exclude()
  public get collectionId(): number {
    return Number(this.id);
  }

  public title: string = "";
  public summary: string | null = null;
  public parentId: number | null = null;
  public reviewCount: number | null = null;
  public average: number | null = null;

  public access: CollectionAccess | null = null;
}

export class CollectionItemData extends BasicClass<CollectionItemData> {
  @Exclude()
  public get itemId(): string {
    return this.id;
  }

  // TODO construire différents types en utilisant __typename?
  public __typename: string | null = null;
  public get itemType(): itemType | null {
    switch (this.__typename) {
      case "CollectionCollectionItemType":
        return itemType.Collection;
      case "FictionCollectionItemType":
        return itemType.Fiction;
      case "ChapterCollectionItemType":
        return itemType.Chapter;
      default:
        return null;
    }
  }

  public order: number | null = null;
  public get position(): number | null {
    return this.order !== null ? this.order + 1 : null;
  }

  public isAccepted: boolean | null = null;

  @Type(() => AuthorData)
  public additionUser: AuthorData | null = null;

  @Transform(({ value }) => new Date(value), { toClassOnly: true })
  @Transform(
    ({ value }) => {
      return value instanceof Date ? value.toISOString() : value;
    },
    { toPlainOnly: true },
  )
  public additionDate: Date | null = null;

  @Type(() => FanfictionModel)
  public fiction: FanfictionModel | null = null;

  @Type(() => ChapterModel)
  public chapter: ChapterModel | null = null;

  @Type(() => CollectionModel)
  public collection: CollectionModel | null = null;

  public get title(): string | null {
    return (this.chapter || this.fiction || this.collection)?.title || null;
  }

  public get reviewCount(): number | null {
    return (this.chapter || this.fiction || this.collection)?.reviewCount || null;
  }

  public get average(): number | null {
    return (this.chapter || this.fiction || this.collection)?.average || null;
  }
}

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

  @Type(() => FanfictionModel)
  public fiction: FanfictionModel | null = null;

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

  public startNote: string = "";

  public endNote: string = "";
  public order: number | null = null;

  public validationStatus: ChapterValidationStatusEnum = ChapterValidationStatusEnum.Draft;
  public wordCount: number | null = null;
  public readCount: number | null = null;
  public reviewCount: number | null = null;
  public average: number | null = null;

  @Exclude()
  public get titleAsSlug(): string {
    return slugify(this.title, { lower: true, locale: "fr", strict: true });
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
