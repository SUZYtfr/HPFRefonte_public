// import { Exclude, Transform } from "class-transformer";
// import { BasicClass, IBasicQuery } from "./basics";

// export enum ReviewItemTypeEnum {
//   Fanfiction = "FictionReview",
//   Chapter = "ChapterReview",
//   Serie = "CollectionReview",
//   Reply = "BaseReview"
// }

// // NOTE - une classe pour tous les types de reviews ET réponse à review
// export class ReviewData extends BasicClass<ReviewData> {
//   @Exclude()
//   public get review_id(): number {
//     return this.id;
//   }

//   public id: number = 0;
//   public grading: number | null = null;
//   public text: string = "";
//   public is_draft: boolean = false;
//   public is_archived: boolean = false;

//   // Pour la création d'une review, indiquer son type et l'ID de l'élément en question
//   // Pour une réponse à review, indiquer seulement le type (la route définira l'élément parent)
//   public item_type: ReviewItemTypeEnum | null = null;
//   public chapter_id: number | null = null;
//   public fiction_id: number | null = null;
//   public collection_id: number | null = null;

//   @Transform(({ value }) => new Date(value), { toClassOnly: true })
//   @Transform(({ value }) => { return ((value instanceof Date) ? value.toISOString() : value); }, { toPlainOnly: true })
//   public publication_date: Date | null = null;
// }

// export interface IReviewFilters extends IBasicQuery {
//   searchTerm: string | null;
//   include_item_types: ReviewItemTypeEnum[] | null;
//   item_id: number | null;
// }
