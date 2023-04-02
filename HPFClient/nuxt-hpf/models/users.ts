import { Type } from "class-transformer";
import { UserData, UserLinkData } from "@/types/users";

interface UserStats {
  fanfictions: number,
  chapters: number,
  words: number,
  series: number,
  challenges: number,
  reviews: number
  favorites_fanfictions: number
  favorites_series: number
  favorites_author: number
}

export class UserModel extends UserData {
  public storiesCount: number = 0;
  public avatar: string | null = null;
  public stats: UserStats | null = null;

  @Type(() => UserLinkData)
  public links: UserLinkData[] | null = null;
}
