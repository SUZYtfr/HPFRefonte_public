import { CharacteristicData, CharacteristicTypeData } from "~/types/characteristics";

export class CharacteristicModel extends CharacteristicData {
  public fictionCount: number = 0;
  public depth: number = 0;
}

export class CharacteristicTypeModel extends CharacteristicTypeData {
  public fictionCount: number = 0;
  public characteristics: CharacteristicModel[] = [];
}
