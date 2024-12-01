import $AxiosWrapper from "~/utils/api";
import { ICharacteristicFilters } from "@/types/characteristics";
import { CharacteristicTypeModel, CharacteristicModel } from "~/models/characteristics";

export const searchCharacteristics = (filters: ICharacteristicFilters | null): Promise<any> => $AxiosWrapper.get<CharacteristicModel>(`/private/characteristics/characteristics/`, filters, CharacteristicModel);
export const createCharacteristic = (characteristic: CharacteristicModel): Promise<any> => $AxiosWrapper.post<CharacteristicModel>(`/private/characteristics/characteristics/`, characteristic, CharacteristicModel);
export const updateCharacteristic = (characteristic: CharacteristicModel): Promise<any> => $AxiosWrapper.put<CharacteristicModel>(`/private/characteristics/characteristics/${characteristic.characteristic_id}/`, characteristic, CharacteristicModel);
export const deleteCharacteristic = (characteristic: CharacteristicModel): Promise<any> => $AxiosWrapper.delete<CharacteristicModel>(`/private/characteristics/characteristics/${characteristic.characteristic_id}/`, CharacteristicModel);
export const searchCharacteristicsTypes = (): Promise<any> => $AxiosWrapper.get<CharacteristicTypeModel>(`/private/characteristics/characteristic-types/`, null, CharacteristicTypeModel);
export const updateCharacteristicsType = (characteristicType: CharacteristicTypeModel): Promise<any> => $AxiosWrapper.put<CharacteristicTypeModel>(`/private/characteristics/characteristic-types/${characteristicType.characteristic_type_id}/`, characteristicType, CharacteristicTypeModel);
export const reorderCharacteristics = (characteristicType: CharacteristicTypeModel, newOrder: Array<Number>): Promise<any> => $AxiosWrapper.put<Array<Number>>(`/private/characteristics/characteristic-types/${characteristicType.characteristic_type_id}/order/`, {order: newOrder});
