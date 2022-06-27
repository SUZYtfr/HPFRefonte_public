import { AuthorData } from "./users";

export interface CommentData {
    comment_id: number,
    post_date: Date,
    content: string,
    authors: AuthorData[],
  }