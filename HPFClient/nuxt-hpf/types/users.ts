import { Exclude, Transform } from "class-transformer";
import { BasicClass, IBasicQuery } from "./basics";

export enum UserStatus {
  Unvalidated = 1,
  Validated = 2,
  Moderator = 3,
  Administrator = 4,
  Banned = 5,
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
  public ban_reason: string = "";
  public username: string = "";
  public email: string = "";

  public is_premium: boolean = false;
  public is_beta: boolean = false;
  public team: number[] | null = null;

  @Transform(({ value }) => new Date(value), { toClassOnly: true })
  @Transform(({ value }) => { return ((value instanceof Date) ? value.toISOString() : value); }, { toPlainOnly: true })
  public creation_date: Date | null = null;

  @Transform(({ value }) => new Date(value), { toClassOnly: true })
  @Transform(({ value }) => { return ((value instanceof Date) ? value.toISOString() : value); }, { toPlainOnly: true })
  public first_seen: Date | null = null;

  @Transform(({ value }) => new Date(value), { toClassOnly: true })
  @Transform(({ value }) => { return ((value instanceof Date) ? value.toISOString() : value); }, { toPlainOnly: true })
  public last_login: Date | null = null;
}

// Filtres utilisateurs
export interface IUserFilters extends IBasicQuery {
  username: string | null,
  email: string | null,
  id: number | null,
  status: UserStatus | null,
  premium: boolean | null,
  published: boolean | null,
  team: number[] | null,
  creation_date: Date | null,
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
  
  @Transform(({ value }) => new Date(value), { toClassOnly: true })
  @Transform(({ value }) => { return ((value instanceof Date) ? value.toISOString() : value); }, { toPlainOnly: true })
  public theme_overriden_at: Date | null = null;
  public theme: number | null = null;

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

  constructor(init?: Partial<AuthorData>) {
    super();
    Object.assign(this, init);
  }
}
