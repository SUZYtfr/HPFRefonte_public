import { Exclude, Transform } from "class-transformer";
import { BasicClass } from "./basics";

export enum UserStatus {
  Unvalidated = 1,
  Validated = 2,
  Moderator = 3,
  Administrator = 4,
  Banned = 4,
}

export enum UserGender {
  Undefined = 0,
  Female = 1,
  Male = 2,
  Other = 3,
}

// Table User
// Informations essentielles d'un utilisateur
export class UserData extends BasicClass<UserData> {
  @Exclude()
  public get user_id(): number {
    return this.id;
  }

  public status: UserStatus = UserStatus.Unvalidated;
  public username: string = "";
  public email: string = "";

  public is_premium: boolean = false;
  public is_beta: boolean = false;

  @Transform(({ value }) => new Date(value), { toClassOnly: true })
  @Transform(({ value }) => { return ((value instanceof Date) ? value.toISOString() : value); }, { toPlainOnly: true })
  public first_seen: Date | null = null;

  @Transform(({ value }) => new Date(value), { toClassOnly: true })
  @Transform(({ value }) => { return ((value instanceof Date) ? value.toISOString() : value); }, { toPlainOnly: true })
  public last_login: Date | null = null;
}

// Table UserProfile
// Informations secondaire (de profil) d'un utilisateur
export class UserProfileData extends BasicClass<UserProfileData> {
  @Exclude()
  public get user_profile_id(): number {
    return this.id;
  }

  public realname: string = "";

  @Transform(({ value }) => new Date(value), { toClassOnly: true })
  @Transform(({ value }) => { return ((value instanceof Date) ? value.toISOString() : value); }, { toPlainOnly: true })
  public birthdate: Date = new Date();

  public website: string | null = null;
  public gender: UserGender | null = null;
  public bio: string | null = null;
  public profile_picture: string | ArrayBuffer | null = null;
}

// Table UserPreferences
// Informations secondaire (des préférences) d'un utilisateur
export class UserPreferencesData extends BasicClass<UserPreferencesData> {
  @Exclude()
  public get user_preference_id(): number {
    return this.id;
  }

  public age_consent: boolean = false;
  public font: string | null = null;
  public font_size: number | null = null;
  public line_spacing: number | null = null;
  public dark_mode: boolean | null = null;
  public skin: string = "default";
  public show_reaction: boolean = true;
}

// Table UserLink
// Liens de l'utilisateur
export class UserLinkData extends BasicClass<UserLinkData> {
  @Exclude()
  public get user_link_id(): number {
    return this.id;
  }

  public user_id: number = 0;
  public link_type_id: number = 0;
  public display_name: string = "";
  public link_url: string = "";
  public visible: boolean = true;
}

export interface UserRegisterProfileData {
  realname: string | null,
  bio: string | null,
  website: string | null,
  profile_picture: string | ArrayBuffer | null,
}

export interface UserRegisterData {
  email: string,
  password: string,
  username: string,
  profile: UserRegisterProfileData,
}

export interface UserLoginData {
  username: string,
  password: string,
}

export class AuthorData extends BasicClass<AuthorData> {
  @Exclude()
  public get user_id(): number {
    return this.id;
  }

  public username: string | null = null;
  public avatar: string | null = null;
}
