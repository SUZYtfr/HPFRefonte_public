export class TipTapEditorContent {
  public content: string | null = null;
  public wordcount: number = 0;

  public constructor(init?: Partial<TipTapEditorContent>) {
    Object.assign(this, init);
  }
}
