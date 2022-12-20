import { UserData, UserProfileData } from '@/types/users'

export interface UserPreferenceData {
  age_consent: boolean;
  font: string;
  font_size: number;
  line_spacing: number;
  dark_mode: boolean;
  skin: string;
  show_reaction: boolean;
  member_review_policy: number;
  anonymous_review_policy: number;
}

export interface AccountData extends UserData {
  user_preferences: UserPreferenceData;
}

export interface UserLoginData {
  nickname: string,
  password: string,
}

export interface TokenResponse {
    "access": string;
    "refresh": string;
}

export interface UserRegisterData {
  email: string,
  password: string,
  nickname: string,
  profile: UserProfileData,
}
