import { Exclude, Transform } from "class-transformer";
import { BasicClass, type IBasicQuery } from "./basics";
import { ExplicitContentEnum } from "./images";

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
  public get userId(): number {
    return this.id;
  }

  public status: UserStatus = UserStatus.Unvalidated;
  public banReason: string = "";
  public username: string = "";
  public email: string = "";

  public isPremium: boolean = false;
  public isBeta: boolean = false;
  public team: number[] | null = null;

  @Transform(
    ({ value }) => {
      return value != null ? new Date(value) : null;
    },
    { toClassOnly: true },
  )
  @Transform(
    ({ value }) => {
      return value instanceof Date ? value.toISOString() : value;
    },
    { toPlainOnly: true },
  )
  public firstSeen: Date | null = null;

  @Transform(
    ({ value }) => {
      return value != null ? new Date(value) : null;
    },
    { toClassOnly: true },
  )
  @Transform(
    ({ value }) => {
      return value instanceof Date ? value.toISOString() : value;
    },
    { toPlainOnly: true },
  )
  public lastLogin: Date | null = null;

  constructor(init?: Partial<UserData>) {
    super();
    Object.assign(this, init);
  }
}

// Filtres utilisateurs
export interface IUserFilters extends IBasicQuery {
  username: string | null;
  email: string | null;
  id: number | null;
  status: UserStatus | null;
  premium: boolean | null;
  published: boolean | null;
  team: number[] | null;
  creationDate: Date | null;
}

// Table UserProfile
// Informations secondaire (de profil) d'un utilisateur
export class UserProfileData extends BasicClass<UserProfileData> {
  @Exclude()
  public get userProfileId(): number {
    return this.id;
  }

  public realname: string = "";

  @Transform(
    ({ value }) => {
      return value != null ? new Date(value) : null;
    },
    { toClassOnly: true },
  )
  @Transform(
    ({ value }) => {
      return value instanceof Date ? value.toISOString() : value;
    },
    { toPlainOnly: true },
  )
  public birthdate: Date = new Date();

  public website: string | null = null;
  public gender: UserGender | null = null;
  public bio: string | null = null;
  public profilePicture: string | ArrayBuffer | null = null;
}

// Table UserPreferences
// Informations secondaire (des préférences) d'un utilisateur
export class UserPreferencesData extends BasicClass<UserPreferencesData> {
  @Exclude()
  public get userPreferenceId(): number {
    return this.id;
  }

  @Transform(
    ({ value }) => {
      return value != null ? new Date(value) : null;
    },
    { toClassOnly: true },
  )
  @Transform(
    ({ value }) => {
      return value instanceof Date ? value.toISOString() : value;
    },
    { toPlainOnly: true },
  )
  public themeOverridenAt: Date | null = null;

  public theme: number | null = null;

  public ageConsent: boolean = false;
  public font: string | null = null;
  public fontSize: number | null = null;
  public lineSpacing: number | null = null;
  public darkMode: boolean | null = null;
  public skin: string = "default";
  public showReaction: boolean = true;
  public explicitContent: ExplicitContentEnum = ExplicitContentEnum.Safe;
}

// Table UserLink
// Liens de l'utilisateur
export class UserLinkData extends BasicClass<UserLinkData> {
  @Exclude()
  public get userLinkId(): number {
    return this.id;
  }

  public userId: number = 0;
  public linkTypeId: number = 0;
  public displayName: string = "";
  public linkUrl: string = "";
  public visible: boolean = true;
}

export interface UserRegisterProfileData {
  realname: string | null;
  bio: string | null;
  website: string | null;
  profilePicture: string | ArrayBuffer | null;
}

export interface UserRegisterData {
  email: string;
  password: string;
  username: string;
  profile: UserRegisterProfileData;
}

export interface UserLoginData {
  username: string;
  password: string;
}

export class AuthorData extends BasicClass<AuthorData> {
  @Exclude()
  public get userId(): number {
    return this.id;
  }

  public username: string | null = null;
  public avatar: string | null = null;
  public watched: boolean = false;

  constructor(init?: Partial<AuthorData>) {
    super();
    Object.assign(this, init);
  }
}
