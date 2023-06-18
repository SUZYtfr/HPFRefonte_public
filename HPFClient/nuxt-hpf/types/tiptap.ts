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

  public constructor(init?: Partial<TipTapEditorConfig>) {
    Object.assign(this, init);
  }
}
