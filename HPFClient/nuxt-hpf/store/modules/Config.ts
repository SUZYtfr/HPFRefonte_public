import { Module, VuexModule, MutationAction } from 'vuex-module-decorators'
import {
    getCharacteristics,
    getCharacteristicTypes,
} from "@/api/characteristics";
import {
    ICharacteristic,
    ICharacteristicType,
    ICharacteristicResponse,
    ICharacteristicTypeResponse
} from '~/types/characteristics'

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

    @MutationAction({ mutate: ['characteristics', 'characteristicTypes'] })
    public async LoadConfig() {
        const characteristicResponse = (await getCharacteristics({page_size: 245})).data as ICharacteristicResponse;
        const charTypeResponse = (await getCharacteristicTypes()).data as ICharacteristicTypeResponse;
        return {'characteristics': characteristicResponse.results, 'characteristicTypes': charTypeResponse.results};
    }

}
