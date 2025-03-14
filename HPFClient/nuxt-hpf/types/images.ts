export class ImageHPFData {
  image_id: number | null = null;
  item_id: number | null = null;
  item_type: number | null = null;
  index: number | null = null;
  url: string | undefined = undefined;
  credits: string | null = null;
  alt: string | undefined = undefined;
  explicit_content_type: ExplicitContentEnum | null = null;
  display_width: number | null = null;
  display_height: number | null = null;

  constructor(_image_id: number | null, _item_id: number | null, _item_type: number | null, _index: number | null, _url: string | null, _credits: string | null, _alt: string | null, _explicit_content_type: ExplicitContentEnum | null, _display_width: number | null, _display_height: number | null) {
    this.image_id = _image_id;
    this.item_id = _item_id;
    this.item_type = _item_type;
    this.index = _index;
    this.url = _url !== null ? _url : "https://bulma.io/assets/images/placeholders/32x32.png";
    this.credits = _credits;
    this.alt = _alt !== null ? _alt : "";
    this.explicit_content_type = _explicit_content_type;
    this.display_width = _display_width;
    this.display_height = _display_height;
  }
}

export interface IContentImageFilters {
  username: string | null;
  explicit_content_type: ExplicitContentEnum | null;
  missing_credits: boolean | null;
  // host: number | null;  // TODO
}

export enum ExplicitContentEnum {
  Safe = 0,
  Mature = 1 << 1,
  Gore = 1 << 2,
  All = ~(~0 << 4)
}

export enum BannerCategoryEnum {
  Website = 1,
  Partner = 2,
  Event = 3,
  Premium = 4,
  Theme = 5,
}

export interface IBannerData {
  id: number | null;
  category: BannerCategoryEnum | null;
  is_active: boolean | null;
  href: string | null;
  alt: string | null;
  src: string | null;
}

export interface IBannerFilters {
  category: BannerCategoryEnum | null;
}
