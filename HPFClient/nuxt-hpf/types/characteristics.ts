import { Exclude } from "class-transformer";
import { BasicClass } from "@/types/basics";

export class CharacteristicData extends BasicClass<CharacteristicData> {
  @Exclude()
  public get characteristicId(): number {
    return this.id;
  }

  public characteristicTypeId: number = 0;
  public parentId: number | null = null;
  public name: string = "";
  public description: string | null = null;
  public order: number = 0;
  public visible: boolean = true;
  public enabled: boolean = true;

  constructor(init?: Partial<CharacteristicData>) {
    super();
    Object.assign(this, init);
  }
}

export class CharacteristicTypeData extends BasicClass<CharacteristicTypeData> {
  @Exclude()
  public get characteristicTypeId(): number {
    return this.id;
  }

  public name: string = "";
  public minLimit: number = 0;
  public maxLimit: number | null = null;
  public visible: boolean = true;
  public enabled: boolean = true;
}

// export class ICharacteristicGetOptions {
//   with_stats: boolean = false;
// }

export interface ICharacteristicFilters {
  characteristicTypeId: number | null,
  parentId: number | null,
  // options: ICharacteristicGetOptions | null,
}
