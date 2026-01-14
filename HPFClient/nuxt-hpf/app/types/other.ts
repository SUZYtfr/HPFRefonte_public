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
