import { Type, Exclude, Transform } from "class-transformer";
import { BasicClass } from "./basics";

export class ThemeData extends BasicClass<ThemeData> {
  @Exclude()
  public get themeId(): number {
    return this.id;
  }

  public name: string = "";
  public default: boolean = true;
  public enabled: boolean = true;

  @Transform(
    ({ value }) => {
      return value != null ? new Date(value) : null;
    },
    { toClassOnly: true },
  )
  @Transform(
    ({ value }) => {
      return value instanceof Date ? value.toISOString() : value;
    },
    { toPlainOnly: true },
  )
  public useDefaultFrom: Date | null = null;

  @Transform(
    ({ value }) => {
      return value != null ? new Date(value) : null;
    },
    { toClassOnly: true },
  )
  @Transform(
    ({ value }) => {
      return value instanceof Date ? value.toISOString() : value;
    },
    { toPlainOnly: true },
  )
  public useDefaultTo: Date | null = null;

  // Plusieurs entrées "jsonisées" dans detail (Light, Dark, Contrast)
  @Type(() => ThemeDetail)
  public details: ThemeDetail[] = [];

  constructor(init?: Partial<ThemeData>) {
    super();
    Object.assign(this, init);
  }
}

// Type de détail (Schéma de couleur)
export enum ColorSchemeEnum {
  Light = 1,
  Dark = 2,
  Contrast = 3,
}
// Metadata de l'enum
export const ColorSchemeEnumMetadata = new Map<ColorSchemeEnum, { description: string; icon: string }>([
  [ColorSchemeEnum.Light, { description: "Clair", icon: "sun" }],
  [ColorSchemeEnum.Dark, { description: "Sombre", icon: "moon" }],
  [ColorSchemeEnum.Contrast, { description: "Contraste élevé", icon: "adjust" }],
]);

export class ThemeDetail {
  primary: string = "#42162b";
  primaryLight: string = "#8f5a74";
  hpfPrimaryLighter: string = "#f1f2f7";
  // TODO changer banner_url en bannièreId (stockée dans la table bannière)
  // Il faut préparer un ecran flottant permettant de choisir une bannière depuis la route des banner (cet outil doit permettre de choisir des images d'une manière générale, d'en ajouter et d'en supprimer)
  // Une image = a minima :
  //    - src (chemin relatif sur le serveur)
  //    - category (theme, banniere utilisateur, autre, (voir l'enum côté serveur))
  // Cet outil doit aussi permettre d'ajouter une nouvelle banner, dans ce cas là j'envoi au serveur une image comme pour l'avatar lors de l'inscription (byte[] + category = theme)
  // Je récupère un id de banner que j'utilise dans bannerId du detail.bannerId
  bannerUrl: string = "https://cdn.pixabay.com/photo/2017/02/04/04/56/hogwarts-2036645_960_720.jpg";

  colorScheme: ColorSchemeEnum = ColorSchemeEnum.Light;

  constructor(init?: Partial<ThemeDetail>) {
    Object.assign(this, init);
  }
}
