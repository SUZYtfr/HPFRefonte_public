import type { OffsetPaginationInfo, Scalars } from "#gql/default";

export interface ContactFormData {
  email: string;
  subject_id: string;
  content: string;
}

export enum FanfictionListType {
  Recent = 1,
  Selections = 2,
}

// Interface utilisée pour les b-menus
export interface MenuItem {
  label: string;
  icon?: string;
  tag?: string;
  to?: string;
  keywords: string;
  isActive: boolean;
  subItems?: MenuItem[];
}

export interface TipTapEditorConfig {
  showFooter: boolean;
  placeholder: string;
  fixedHeight: boolean;
  height: number;
  oneLineToolbar: boolean;
  canUseImage: boolean;
}

export interface TipTapReaderConfig {
  canSelect: boolean;
  quoteCharacterLimit: number;
  fontSize: number;
}

export interface TiptapEditorContent {
  content: string;
  wordCount: number;
}

export interface TransformedPaginated<T> {
  pageInfo: OffsetPaginationInfo;
  results: Array<T>;
  totalCount: Scalars["Int"]["output"];
}
