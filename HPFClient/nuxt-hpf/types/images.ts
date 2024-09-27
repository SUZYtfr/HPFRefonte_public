export class ImageHPFData {
  imageId: number | null = null;
  itemId: number | null = null;
  itemType: number | null = null;
  index: number | null = null;
  url: string | undefined = undefined;
  credits: string | null = null;
  alt: string | undefined = undefined;
  isAdultOnly: boolean | null = null;
  displayWidth: number | null = null;
  displayHeight: number | null = null;

  constructor(_imageId: number | null, _itemId: number | null, _itemType: number | null, _index: number | null, _url: string | null, _credits: string | null, _alt: string | null, _isAdultOnly: boolean | null, _displayWidth: number | null, _displayHeight: number | null) {
    this.imageId = _imageId;
    this.itemId = _itemId;
    this.itemType = _itemType;
    this.index = _index;
    this.url = _url !== null ? _url : "https://bulma.io/images/placeholders/32x32.png";
    this.credits = _credits;
    this.alt = _alt !== null ? _alt : "";
    this.isAdultOnly = _isAdultOnly;
    this.displayWidth = _displayWidth;
    this.displayHeight = _displayHeight;
  }
}
