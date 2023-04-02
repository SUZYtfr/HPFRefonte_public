import $AxiosWrapper from "~/utils/api";
import { ICharacteristicFilters } from "@/types/characteristics";
import { CharacteristicTypeModel, CharacteristicModel } from "~/models/characteristics";

export const getCharacteristics = (filters: ICharacteristicFilters | null): Promise<any> => $AxiosWrapper.get<CharacteristicModel>("/characteristics", filters, CharacteristicModel);
export const getCharacteristicsTypes = (): Promise<any> => $AxiosWrapper.get<CharacteristicTypeModel>("/characteristics_types", null, CharacteristicTypeModel);
