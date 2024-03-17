import { ImageHPFData } from "@/types/images";

export class TipTapEditorContent {
  public content: string | null = null;
  public wordcount: number = 0;
  public content_images: ImageHPFData[] | null = null;

  public constructor(init?: Partial<TipTapEditorContent>) {
    Object.assign(this, init);
  }
}

export class TipTapEditorConfig {
  public showFooter: boolean = true;
  public placeholder: string = "";
  public readOnly: boolean = true;
  public fixedHeight: boolean = true;
  public height: number = 125;
  public defaultValue: string = "";
  public canQuote: boolean = false;
  public quoteLimit: number = 250;
  public fontSize: number = 100;
  public oneLineToolbar: boolean = false;
  public canUseImage: boolean = false;
  public constructor(init?: Partial<TipTapEditorConfig>) {
    Object.assign(this, init);
  }
}
