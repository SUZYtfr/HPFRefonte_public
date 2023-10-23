import $UseFetchWrapper from "~/utils/api";
import { ICharacteristicFilters } from "@/types/characteristics";
import { CharacteristicTypeModel, CharacteristicModel } from "~/models/characteristics";

export const getCharacteristics = (filters: ICharacteristicFilters | null): Promise<any> => $UseFetchWrapper.get<CharacteristicModel>("/characteristics/characteristics/", filters, CharacteristicModel);
export const getCharacteristicsTypes = (): Promise<any> => $UseFetchWrapper.get<CharacteristicTypeModel>("/characteristics/characteristic-types/", null, CharacteristicTypeModel);
