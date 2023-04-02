import { Exclude } from "class-transformer";
import { BasicClass } from "@/types/basics";

export class CharacteristicData extends BasicClass<CharacteristicData> {
  @Exclude()
  public get characteristic_id(): number {
    return this.id;
  }

  public characteristic_type_id: number = 0;
  public parent_id: number | null = null;
  public name: string = "";
  public description: string | null = null;
  public in_order: number = 0;
  public visible: boolean = true;
  public enabled: boolean = true;
}

export class CharacteristicTypeData extends BasicClass<CharacteristicTypeData> {
  @Exclude()
  public get characteristic_type_id(): number {
    return this.id;
  }

  public name: string = "";
  public min_occurence: number = 0;
  public max_occurence: number | null = null;
  public visible: boolean = true;
  public enabled: boolean = true;
}

export class ICharacteristicGetOptions {
  with_stats: boolean = false;
}

export interface ICharacteristicFilters {
  characteristic_type_id: number | null,
  parent_id: number | null,
  options: ICharacteristicGetOptions | null,
  limit: number | null
}
