import $AxiosWrapper from "~/utils/api";
import { ICharacteristicFilters } from "@/types/characteristics";
import { CharacteristicTypeModel, CharacteristicModel } from "~/models/characteristics";

export const searchCharacteristics = (filters: ICharacteristicFilters | null): Promise<any> => $AxiosWrapper.get<CharacteristicModel>(`/characteristics/characteristics/`, filters, CharacteristicModel);
export const searchCharacteristicsTypes = (): Promise<any> => $AxiosWrapper.get<CharacteristicTypeModel>(`/characteristics/characteristic-types/`, null, CharacteristicTypeModel);
