export class ImageHPFData {
  imageId: number | null = null;
  itemId: number | null = null;
  itemType: number | null = null;
  index: number | null = null;
  url: string | undefined = undefined;
  credits: string | null = null;
  alt: string | undefined = undefined;
  explicitContentType: ExplicitContentEnum | null = null;
  displayWidth: number | null = null;
  displayHeight: number | null = null;

  constructor(
    _imageId: number | null,
    _itemId: number | null,
    _itemType: number | null,
    _index: number | null,
    _url: string | null,
    _credits: string | null,
    _alt: string | null,
    _explicitContentType: ExplicitContentEnum | null,
    _displayWidth: number | null,
    _displayHeight: number | null,
  ) {
    this.imageId = _imageId;
    this.itemId = _itemId;
    this.itemType = _itemType;
    this.index = _index;
    this.url = _url !== null ? _url : "https://bulma.io/assets/images/placeholders/32x32.png";
    this.credits = _credits;
    this.alt = _alt !== null ? _alt : "";
    this.explicitContentType = _explicitContentType;
    this.displayWidth = _displayWidth;
    this.displayHeight = _displayHeight;
  }
}

export interface IContentImageFilters {
  username: string | null;
  explicitContentType: ExplicitContentEnum | null;
  missingCredits: boolean | null;
  // host: number | null;  // TODO
}

export enum ExplicitContentEnum {
  Safe = 0,
  Mature = 1,
  Gore = 2,
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
  isActive: boolean | null;
  href: string | null;
  alt: string | null;
  src: string | null;
}

export interface IBannerFilters {
  category: BannerCategoryEnum | null;
}
