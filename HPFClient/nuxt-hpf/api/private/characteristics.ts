import $AxiosWrapper from "~/utils/api";
import { ICharacteristicFilters } from "@/types/characteristics";
import { CharacteristicTypeModel, CharacteristicModel } from "~/models/characteristics";
import type { UseFetchOptions } from "nuxt/app";

export const searchCharacteristics = (filters: ICharacteristicFilters | null, options?: UseFetchOptions<CharacteristicModel[]>) => $AxiosWrapper.get<CharacteristicModel[]>(`/private/characteristics/characteristics/`, filters, CharacteristicModel, options);
export const createCharacteristic = (characteristic: CharacteristicModel, options?: UseFetchOptions<CharacteristicModel>) => $AxiosWrapper.post<CharacteristicModel>(`/private/characteristics/characteristics/`, characteristic, CharacteristicModel, options);
export const updateCharacteristic = (characteristic: CharacteristicModel, options?: UseFetchOptions<CharacteristicModel>) => $AxiosWrapper.put<CharacteristicModel>(`/private/characteristics/characteristics/${characteristic.characteristic_id}/`, characteristic, CharacteristicModel, options);
export const deleteCharacteristic = (characteristic: CharacteristicModel, options?: UseFetchOptions<CharacteristicModel>) => $AxiosWrapper.delete<CharacteristicModel>(`/private/characteristics/characteristics/${characteristic.characteristic_id}/`, CharacteristicModel, options);
export const searchCharacteristicsTypes = (options?: UseFetchOptions<CharacteristicTypeModel[]>) => $AxiosWrapper.get<CharacteristicTypeModel[]>(`/private/characteristics/characteristic-types/`, null, CharacteristicTypeModel, options);
export const updateCharacteristicsType = (characteristicType: CharacteristicTypeModel, options?: UseFetchOptions<CharacteristicTypeModel>) => $AxiosWrapper.put<CharacteristicTypeModel>(`/private/characteristics/characteristic-types/${characteristicType.characteristic_type_id}/`, characteristicType, CharacteristicTypeModel, options);
export const reorderCharacteristics = (characteristicType: CharacteristicTypeModel, newOrder: Array<Number>, options?: UseFetchOptions<any>) => $AxiosWrapper.put<Array<Number>>(`/private/characteristics/characteristic-types/${characteristicType.characteristic_type_id}/order/`, {order: newOrder}, null, options);
