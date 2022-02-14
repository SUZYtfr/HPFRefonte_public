import { Module, VuexModule, Mutation, Action } from 'vuex-module-decorators'
import {
    getCharacteristics,
    getCharacteristicsTypes,
} from "@/api/characteristics";
import { ICharacteristic, ICharacteristicType } from '~/types/characteristics'

export interface ConfigState {
    characteristics: ICharacteristic[];
    characteristicTypes: ICharacteristicType[];
}

@Module({
    name: 'modules/Config',
    namespaced: true,
    stateFactory: true,
})
export default class _Config extends VuexModule implements ConfigState {
    public characteristics: ICharacteristic[] = []
    public characteristicTypes: ICharacteristicType[] = []

    @Mutation
    public SET_CHARACTERISTICS(characteristics: ICharacteristic[]) {
        this.characteristics = characteristics;
    }

    @Mutation
    public SET_CHARACTERISTIC_TYPES(characteristicTypes: ICharacteristicType[]) {
        this.characteristicTypes = characteristicTypes
    }

    @Action
    public async LoadConfig() {
        this.SET_CHARACTERISTICS((await getCharacteristics(null)).data.items);
        this.SET_CHARACTERISTIC_TYPES((await getCharacteristicsTypes()).data.items);
    }

    @Action
    public async ResetConfig() {
        this.SET_CHARACTERISTICS([]);
        this.SET_CHARACTERISTIC_TYPES([]);
    }
}
