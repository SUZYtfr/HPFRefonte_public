export class ImageHPFData {
    image_id: number | null = null;
    item_id: number | null = null;
    item_type: number | null = null;
    id_in_text: number | null = null;
    url: string | null = null;
    credit: string | null = null;
    alt: string | null = null;
    age_restricted: boolean | null = null;

    constructor(_image_id: number | null, _item_id: number | null, _item_type: number | null, _id_in_text: number | null, _url: string | null, _credit: string | null, _alt: string | null, _age_restricted: boolean | null)
    {
        this.image_id = _image_id;
        this.item_id = _item_id;
        this.item_type = _item_type;
        this.id_in_text = _id_in_text;
        this.url = _url !== null ? _url : "https://bulma.io/images/placeholders/32x32.png";
        this.credit = _credit;
        this.alt = _alt;
        this.age_restricted = _age_restricted;
    }
  }