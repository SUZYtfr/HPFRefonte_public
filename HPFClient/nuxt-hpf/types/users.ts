import { Exclude, Transform } from "class-transformer";
import { BasicClass } from "./basics";

enum UserStatus {
  Unvalidated = 1,
  Validated = 2,
  Moderator = 3,
  Administrator = 4,
  Banned = 4,
}

export class UserData extends BasicClass<UserData> {
  @Exclude()
  public get user_id(): number {
    return this.id;
  }

  public status: UserStatus = UserStatus.Unvalidated;
  public nickname: string = "";
  public realname: string = "";
  public email: string = "";

  @Transform(({ value }) => new Date(value), { toClassOnly: true })
  @Transform(({ value }) => (value?.toISOString() ?? ""), { toPlainOnly: true })
  public birthdate: Date = new Date();

  public sex: number | null = null;
  public bio: string | null = null;
  public is_premium: boolean = false;
  public is_beta: boolean = false;

  @Transform(({ value }) => new Date(value), { toClassOnly: true })
  @Transform(({ value }) => (value?.toISOString() ?? ""), { toPlainOnly: true })
  public last_login_date: Date | null = null;

  public user_pref_font: string | null = null;
  public user_pref_font_size: number | null = null;
  public user_pref_line_spacing: number | null = null;
  public user_pref_dark_mode: boolean | null = null;
  public user_pref_skin: string = "default";
  public user_pref_show_reaction: boolean = true;
  public age_consent: boolean = false;
}

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

export interface UserRegisterData {
  email: string,
  password: string,
  username: string,
  realname: string | null,
  bio: string | null,
  website: string | null,
  avatar: string | ArrayBuffer | null,
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

  public nickname: string | null = null;
  public avatar: string | null = null;
}
