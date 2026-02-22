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
  readOnly: boolean;
  fixedHeight: boolean;
  height: number;
  defaultValue: string;
  canQuote: boolean;
  quoteLimit: number;
  fontSize: number;
  oneLineToolbar: boolean;
  canUseImage: boolean;
}

export interface TiptapEditorContent {
  content: string;
  wordCount: number;
}

export interface ReviewState extends TiptapEditorContent {
  canGrade: boolean;
  grading?: number;
}
