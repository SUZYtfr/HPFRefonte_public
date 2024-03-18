import $AxiosWrapper from "~/utils/api";
import { ReviewModel } from "~/models/fanfictions";
import { ReviewData, IReviewFilters } from "@/types/fanfictions";
import { IBasicQuery } from "~/types/basics";

// Routes des reviews de chapitres
export const searchChapterReviews = (chapter_id: number, filters: IBasicQuery | null): Promise<any> => $AxiosWrapper.get<ReviewModel>("/fictions/chapters/" + chapter_id + "/reviews/", filters, ReviewModel);
export const getChapterReview = (id: number): Promise<any> => $AxiosWrapper.get<ReviewModel>("/reviews/chapter-reviews/" + id.toString() + "/", null, ReviewModel);
export const postChapterReview = (chapter_id: number, review: ReviewData): Promise<any> => $AxiosWrapper.post<ReviewModel>("/fictions/chapters/" + chapter_id + "/reviews/", review, ReviewModel);
export const putChapterReview = (id: number, review: ReviewData): Promise<any> => $AxiosWrapper.put<ReviewModel>("/reviews/chapter-reviews/" + id.toString() + "/", review, ReviewModel);
export const getChapterReviewReplies = (id: number): Promise<any> => $AxiosWrapper.get<ReviewModel>("/reviews/chapter-reviews/" + id.toString() + "/replies/", null, ReviewModel);
export const postChapterReviewReply = (review_id: number, review: ReviewData): Promise<any> => $AxiosWrapper.post<ReviewModel>("/reviews/chapter-reviews/" + review_id + "/replies/", review, ReviewModel);

// Routes des reviews de fictions
export const searchFictionReviews = (fiction_id: number, filters: IBasicQuery | null): Promise<any> => $AxiosWrapper.get<ReviewModel>("/fictions/fictions/" + fiction_id + "/reviews/", filters, ReviewModel);
export const getFictionReview = (id: number): Promise<any> => $AxiosWrapper.get<ReviewModel>("/reviews/fictions-reviews/" + id.toString() + "/", null, ReviewModel);
export const postFictionReview = (fiction_id: number, review: ReviewData): Promise<any> => $AxiosWrapper.post<ReviewModel>("/fictions/fictions/" + fiction_id + "/reviews/", review, ReviewModel);
export const putFictionReview = (id: number, review: ReviewData): Promise<any> => $AxiosWrapper.put<ReviewModel>("/reviews/fictions-reviews/" + id.toString() + "/", review, ReviewModel);
export const getFictionReviewReplies = (id: number): Promise<any> => $AxiosWrapper.get<ReviewModel>("/reviews/fictions-reviews/" + id.toString() + "/replies/", null, ReviewModel);
export const postFictionReviewReply = (review_id: number, review: ReviewData): Promise<any> => $AxiosWrapper.post<ReviewModel>("/reviews/fictions-reviews/" + review_id + "/replies/", review, ReviewModel);

// Routes des reviews de séries
export const searchCollectionReviews = (collection_id: number, filters: IBasicQuery | null): Promise<any> => $AxiosWrapper.get<ReviewModel>("/fictions/collections/" + collection_id + "/reviews/", filters, ReviewModel);
export const getCollectionReview = (id: number): Promise<any> => $AxiosWrapper.get<ReviewModel>("/reviews/collections-reviews/" + id.toString() + "/", null, ReviewModel);
export const postCollectionReview = (collection_id: number, review: ReviewData): Promise<any> => $AxiosWrapper.post<ReviewModel>("/fictions/collections/" + collection_id + "/reviews/", review, ReviewModel);
export const putCollectionReview = (id: number, review: ReviewData): Promise<any> => $AxiosWrapper.put<ReviewModel>("/reviews/collections-reviews/" + id.toString() + "/", review, ReviewModel);
export const getCollectionReviewReplies = (id: number): Promise<any> => $AxiosWrapper.get<ReviewModel>("/reviews/collections-reviews/" + id.toString() + "/replies/", null, ReviewModel);
export const postCollectionReviewReply = (review_id: number, review: ReviewData): Promise<any> => $AxiosWrapper.post<ReviewModel>("/reviews/collections-reviews/" + review_id + "/replies/", review, ReviewModel);

// Route unique de suppression de review
export const deleteReview = (id: number): Promise<any> => $AxiosWrapper.delete<ReviewModel>("/reviews/" + id.toString() + "/", ReviewModel);

// Routes globales utilisant les filters pour choisir l'entité
export const searchReviews = (filters: IReviewFilters | null): Promise<any> => $AxiosWrapper.get<ReviewModel>("/reviews/reviews/", filters, ReviewModel);
export const getReviews = (id: number): Promise<any> => $AxiosWrapper.get<ReviewModel>("/reviews/reviews/" + id.toString() + "/", null, ReviewModel);
export const postReviews = (review: ReviewData): Promise<any> => $AxiosWrapper.post<ReviewModel>("/reviews/reviews/", review, ReviewModel);
export const putReviews = (id: number, review: ReviewData): Promise<any> => $AxiosWrapper.put<ReviewModel>("/reviews/reviews/" + id.toString() + "/", review, ReviewModel);
export const deleteReviews = (id: number): Promise<any> => $AxiosWrapper.delete<ReviewModel>("/reviews/reviews/" + id.toString() + "/", ReviewModel);
export const getReviewReplies = (id: number): Promise<any> => $AxiosWrapper.get<ReviewModel>("/reviews/reviews/" + id.toString() + "/replies/", null, ReviewModel);
export const postReviewReply = (id: number): Promise<any> => $AxiosWrapper.post<ReviewModel>("/reviews/reviews/" + id.toString() + "/replies/", null, ReviewModel);
export const getReviewReplyContext = (id: number): Promise<any> => $AxiosWrapper.get<ReviewModel>("/reviews/reviews/" + id.toString() + "/context/", null, ReviewModel);

// Accés aux reviews du compte authentifié / page de gestion de reviews
export const getPublishedReviews = (filters: IReviewFilters | null): Promise<any> => $AxiosWrapper.get<ReviewModel>("/account/published-reviews/", filters, ReviewModel);
export const getReceivedReviews = (filters: IReviewFilters | null): Promise<any> => $AxiosWrapper.get<ReviewModel>("/account/received-reviews/", filters, ReviewModel);
export const getDraftReviews = (filters: IReviewFilters | null): Promise<any> => $AxiosWrapper.get<ReviewModel>("/account/draft-reviews/", filters, ReviewModel);
export const getUnansweredReviews = (filters: IReviewFilters | null): Promise<any> => $AxiosWrapper.get<ReviewModel>("/account/unanswered-reviews/", filters, ReviewModel);
