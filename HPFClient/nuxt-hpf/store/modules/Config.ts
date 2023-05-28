import { Module, VuexModule, Mutation, Action } from "vuex-module-decorators";
import { plainToInstance } from "class-transformer";
import {
  getCharacteristics,
  getCharacteristicsTypes
} from "@/api/characteristics";
// import { CharacteristicData, CharacteristicTypeData } from "~/types/characteristics";
import { CharacteristicModel, CharacteristicTypeModel } from "~/models/characteristics";

export interface ConfigState {
  characteristics: CharacteristicModel[];
  characteristicTypes: CharacteristicTypeModel[];
}

@Module({
  name: "modules/Config",
  namespaced: true,
  stateFactory: true
})
export default class _Config extends VuexModule implements ConfigState {
  private _characteristics: CharacteristicModel[] = [];
  private _characteristicTypes: CharacteristicTypeModel[] = [];

  public get characteristics(): CharacteristicModel[] {
    if (process.client && this._characteristics !== null && this._characteristics.length > 0 && (this._characteristics[0] instanceof CharacteristicModel) === false) {
      return plainToInstance(
        CharacteristicModel,
        this._characteristics
      );
    }
    return this._characteristics;
  }

  public get characteristicTypes(): CharacteristicTypeModel[] {
    if (process.client && this._characteristicTypes !== null && this._characteristicTypes.length > 0 && (this._characteristicTypes[0] instanceof CharacteristicTypeModel) === false) {
      return plainToInstance(
        CharacteristicTypeModel,
        this._characteristicTypes
      );
    }
    return this._characteristicTypes;
  }

  @Mutation
  public SET_CHARACTERISTICS(characteristics: CharacteristicModel[]): void {
    this._characteristics = characteristics;
  }

  @Mutation
  public SET_CHARACTERISTIC_TYPES(characteristicTypes: CharacteristicTypeModel[]): void {
    this._characteristicTypes = characteristicTypes;
  }

  // @Action
  // public CaracteristicToInstance(): void {
  //   this.SET_CHARACTERISTICS(plainToInstance(
  //     CharacteristicModel,
  //     this._characteristics
  //   ));
  // }

  // public CaracteristicTypeToInstance(): void {
  //   this.SET_CHARACTERISTIC_TYPES(plainToInstance(
  //     CharacteristicTypeModel,
  //     this._characteristicTypes
  //   ));
  // }

  @Action
  public async LoadConfig(): Promise<void> {
    let caracteristicsTemp;
    let caracteristicTypesTemp;
    try {
      caracteristicsTemp = (await getCharacteristics(null)).items;
    } catch (error) {
      caracteristicsTemp = [];
      console.log(error);
    }

    try {
      caracteristicTypesTemp = (await getCharacteristicsTypes()).items;
    } catch (error) {
      caracteristicTypesTemp = [];
      console.log(error);
    }

    this.SET_CHARACTERISTICS(caracteristicsTemp);
    this.SET_CHARACTERISTIC_TYPES(caracteristicTypesTemp);
  }

  @Action
  public ResetConfig(): void {
    this.SET_CHARACTERISTICS([]);
    this.SET_CHARACTERISTIC_TYPES([]);
  }
}
