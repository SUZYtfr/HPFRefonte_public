import { Type, Exclude, Transform } from "class-transformer";
import { BasicClass } from "./basics";

export class ThemeData extends BasicClass<ThemeData> {
  @Exclude()
  public get theme_id(): number {
    return this.id;
  }

  public name: string = "";
  public default: boolean = true;
  public enabled: boolean = true;

  @Transform(({ value }) => new Date(value), { toClassOnly: true })
  @Transform(({ value }) => { return ((value instanceof Date) ? value.toISOString() : value); }, { toPlainOnly: true })
  public use_default_from: Date | null = null;

  @Transform(({ value }) => new Date(value), { toClassOnly: true })
  @Transform(({ value }) => { return ((value instanceof Date) ? value.toISOString() : value); }, { toPlainOnly: true })
  public use_default_to: Date | null = null;

  @Type(() => ThemeDetail)
  public detail: ThemeDetail | null = null;

  constructor(init?: Partial<ThemeData>) {
    super();
    Object.assign(this, init);
  }
}

export class ThemeDetail {
  primary: string = "#42162b";
  primary_light: string = "#8f5a74";
  hpf_primary_lighter: string = "#f1f2f7";
  banner_url: string = "https://cdn.pixabay.com/photo/2017/02/04/04/56/hogwarts-2036645_960_720.jpg";
  nightTheme: boolean = false;

  constructor(init?: Partial<ThemeDetail>) {
    Object.assign(this, init);
  }
}
