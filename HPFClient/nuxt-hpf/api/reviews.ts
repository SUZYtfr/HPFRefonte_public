import $AxiosWrapper from "~/utils/api";
import { ReviewModel } from "~/models/fanfictions";
import { ReviewData, IReviewFilters } from "@/types/fanfictions";
import { IBasicQuery } from "~/types/basics";

// Routes des reviews de chapitres
export const searchChapterReviews = (chapterId: number, filters: IBasicQuery | null): Promise<any> => $AxiosWrapper.get<ReviewModel>("/fictions/chapters/" + chapterId + "/reviews/", filters, ReviewModel);
export const getChapterReview = (id: number): Promise<any> => $AxiosWrapper.get<ReviewModel>("/reviews/chapter-reviews/" + id.toString() + "/", null, ReviewModel);
export const postChapterReview = (chapterId: number, review: ReviewData): Promise<any> => $AxiosWrapper.post<ReviewModel>("/fictions/chapters/" + chapterId + "/reviews/", review, ReviewModel);
export const putChapterReview = (id: number, review: ReviewData): Promise<any> => $AxiosWrapper.put<ReviewModel>("/reviews/chapter-reviews/" + id.toString() + "/", review, ReviewModel);
export const getChapterReviewReplies = (id: number): Promise<any> => $AxiosWrapper.get<ReviewModel>("/reviews/chapter-reviews/" + id.toString() + "/replies/", null, ReviewModel);
export const postChapterReviewReply = (reviewId: number, review: ReviewData): Promise<any> => $AxiosWrapper.post<ReviewModel>("/reviews/chapter-reviews/" + reviewId + "/replies/", review, ReviewModel);

// Routes des reviews de fictions
export const searchFictionReviews = (fictionId: number, filters: IBasicQuery | null): Promise<any> => $AxiosWrapper.get<ReviewModel>("/fictions/fictions/" + fictionId + "/reviews/", filters, ReviewModel);
export const getFictionReview = (id: number): Promise<any> => $AxiosWrapper.get<ReviewModel>("/reviews/fictions-reviews/" + id.toString() + "/", null, ReviewModel);
export const postFictionReview = (fictionId: number, review: ReviewData): Promise<any> => $AxiosWrapper.post<ReviewModel>("/fictions/fictions/" + fictionId + "/reviews/", review, ReviewModel);
export const putFictionReview = (id: number, review: ReviewData): Promise<any> => $AxiosWrapper.put<ReviewModel>("/reviews/fictions-reviews/" + id.toString() + "/", review, ReviewModel);
export const getFictionReviewReplies = (id: number): Promise<any> => $AxiosWrapper.get<ReviewModel>("/reviews/fictions-reviews/" + id.toString() + "/replies/", null, ReviewModel);
export const postFictionReviewReply = (reviewId: number, review: ReviewData): Promise<any> => $AxiosWrapper.post<ReviewModel>("/reviews/fictions-reviews/" + reviewId + "/replies/", review, ReviewModel);

// Routes des reviews de séries
export const searchCollectionReviews = (collectionId: number, filters: IBasicQuery | null): Promise<any> => $AxiosWrapper.get<ReviewModel>("/fictions/collections/" + collectionId + "/reviews/", filters, ReviewModel);
export const getCollectionReview = (id: number): Promise<any> => $AxiosWrapper.get<ReviewModel>("/reviews/collections-reviews/" + id.toString() + "/", null, ReviewModel);
export const postCollectionReview = (collectionId: number, review: ReviewData): Promise<any> => $AxiosWrapper.post<ReviewModel>("/fictions/collections/" + collectionId + "/reviews/", review, ReviewModel);
export const putCollectionReview = (id: number, review: ReviewData): Promise<any> => $AxiosWrapper.put<ReviewModel>("/reviews/collections-reviews/" + id.toString() + "/", review, ReviewModel);
export const getCollectionReviewReplies = (id: number): Promise<any> => $AxiosWrapper.get<ReviewModel>("/reviews/collections-reviews/" + id.toString() + "/replies/", null, ReviewModel);
export const postCollectionReviewReply = (reviewId: number, review: ReviewData): Promise<any> => $AxiosWrapper.post<ReviewModel>("/reviews/collections-reviews/" + reviewId + "/replies/", review, ReviewModel);

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
