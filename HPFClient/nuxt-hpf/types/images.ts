export class ImageHPFData {
  image_id: number | null = null;
  item_id: number | null = null;
  item_type: number | null = null;
  index: number | null = null;
  url: string | undefined = undefined;
  credits: string | null = null;
  alt: string | undefined = undefined;
  is_adult_only: boolean | null = null;
  display_width: number | null = null;
  display_height: number | null = null;

  constructor(_image_id: number | null, _item_id: number | null, _item_type: number | null, _index: number | null, _url: string | null, _credits: string | null, _alt: string | null, _is_adult_only: boolean | null, _display_width: number | null, _display_height: number | null) {
    this.image_id = _image_id;
    this.item_id = _item_id;
    this.item_type = _item_type;
    this.index = _index;
    this.url = _url !== null ? _url : "https://bulma.io/images/placeholders/32x32.png";
    this.credits = _credits;
    this.alt = _alt !== null ? _alt : "";
    this.is_adult_only = _is_adult_only;
    this.display_width = _display_width;
    this.display_height = _display_height;
  }
}
