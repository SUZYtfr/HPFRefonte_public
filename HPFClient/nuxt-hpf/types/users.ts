export interface UserData {
  user_id: number,
  creation_date: Date,
  status: number,
  nickname: string,
  realname: string,
  bio: string,
  is_premium: boolean,
  is_beta: boolean,
  avatar: string,
  stats: {
    fanfictions: number,
    chapters: number,
    words: number,
    series: number,
    challenges: number,
    reviews: number
    favorites_fanfictions: number
    favorites_series: number
    favorites_author: number
  },
  links: UserLinkData[],
}

export interface UserLinkData {
  link_type_id: number;
  display_name: string;
  link_url: string;
}

export interface UserRegisterData {
  email: string,
  password: string,
  username: string,
  realname: string | null,
  bio: string | null,
  website: string | null,
  avatar: string | ArrayBuffer| null,
}

export interface UserLoginData {
  username: string,
  password: string,
}