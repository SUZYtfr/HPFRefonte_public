import $AxiosWrapper from "~/utils/api";
import { ReviewModel } from "~/models/reviews";
import { IReviewFilters, ReviewData } from "~/types/reviews";

export const searchReviews = (filters: IReviewFilters | null): Promise<any> => $AxiosWrapper.get<ReviewModel>("/reviews/reviews/", filters, ReviewModel);
export const getReviews = (id: number): Promise<any> => $AxiosWrapper.get<ReviewModel>("/reviews/reviews/" + id.toString() + "/", null, ReviewModel);
export const postReviews = (review: ReviewData): Promise<any> => $AxiosWrapper.post<ReviewModel>("/reviews/reviews/", review, ReviewModel);
export const putReviews = (id: number, review: ReviewData): Promise<any> => $AxiosWrapper.put<ReviewModel>("/reviews/reviews/" + id.toString() + "/", review, ReviewModel);
export const deleteReviews = (id: number): Promise<any> => $AxiosWrapper.delete<ReviewModel>("/reviews/reviews/" + id.toString() + "/", ReviewModel);
export const getReviewReplies = (id: number): Promise<any> => $AxiosWrapper.get<ReviewModel>("/reviews/reviews/" + id.toString() + "/replies/", null, ReviewModel);
export const postReviewReply = (id: number): Promise<any> => $AxiosWrapper.post<ReviewModel>("/reviews/reviews/" + id.toString() + "/replies/", null, ReviewModel);
export const getReviewReplyContext = (id: number): Promise<any> => $AxiosWrapper.get<ReviewModel>("/reviews/reviews/" + id.toString() + "/context/", null, ReviewModel);

// accès aux reviews du compte authentifié / page de gestion de reviews
export const getPublishedReviews = (filters: IReviewFilters | null): Promise<any> => $AxiosWrapper.get<ReviewModel>("/account/published-reviews/", filters, ReviewModel);
export const getReceivedReviews = (filters: IReviewFilters | null): Promise<any> => $AxiosWrapper.get<ReviewModel>("/account/received-reviews/", filters, ReviewModel);
export const getDraftReviews = (filters: IReviewFilters | null): Promise<any> => $AxiosWrapper.get<ReviewModel>("/account/draft-reviews/", filters, ReviewModel);
export const getUnansweredReviews = (filters: IReviewFilters | null): Promise<any> => $AxiosWrapper.get<ReviewModel>("/account/unanswered-reviews/", filters, ReviewModel);
