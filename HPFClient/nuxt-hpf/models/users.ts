import { Type } from "class-transformer";
import { UserData, UserLinkData, UserStatus, UserProfileData, UserPreferencesData } from "@/types/users";

interface UserStats {
  fiction_count: number,
  chapter_count: number,
  word_count: number,
  collection_count: number,
  challenges: number,
  review_count: number
  favorites_fanfictions: number
  favorites_series: number
  favorites_author: number
}

// Model d'un utilisateur
// Avec stats, information de profil, préférences et liens
export class UserModel extends UserData {
  public stats: UserStats | null = null;

  @Type(() => UserProfileData)
  public profile: UserProfileData | null = null;

  @Type(() => UserPreferencesData)
  public preferences: UserPreferencesData | null = null;

  @Type(() => UserLinkData)
  public links: UserLinkData[] | null = null;
}

export class Account {
  public user_id: number | null = null;
  public username: string | null = null;
  public avatar: string | null = null;
  public roles: UserStatus[] = [];
}
