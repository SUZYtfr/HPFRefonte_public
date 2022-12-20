export interface UserData {
  id: number;
  first_seen: Date;
  last_login: Date;
  username: string;
  email: string;
  is_beta: boolean;
  is_premium: boolean;
  stats: {
    fiction_count: number;
    chapter_count: number;
    review_count: number;
    collection_count: number;
    perso_review_count: number;
    challenge_count: number;
    read_count: number;
    word_count: number;
    comment_count: number;
    reviewreply_count: number;
    favorite_fanfictions: [];
    favorite_collections: [];
    favorite_authors: [];
  };
  profile: UserProfileData;
}

export interface UserProfileData {
  realname: string,
  bio: string,
  birthdate: string | null,
  gender: number | null,
  user_links: UserLinkData[],
  website: string | null,
  profile_picture: UserProfileAvatarData,
}

export interface UserProfileAvatarData {
  image_data: string | ArrayBuffer | null,
  src_link: string | null,
  src_path: string | null,
  is_user_property: boolean,
  is_adult_only: boolean,
  credits_url: string | null,
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

export interface AuthorData {
  author_id: number,
  nickname: string
}