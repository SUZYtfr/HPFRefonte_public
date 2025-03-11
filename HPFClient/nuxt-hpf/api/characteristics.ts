import fetchController from "~/utils/api";
import { ICharacteristicFilters } from "@/types/characteristics";
import { CharacteristicTypeModel, CharacteristicModel } from "~/models/characteristics";

export const searchCharacteristics = (filters: ICharacteristicFilters | null) => fetchController.get<CharacteristicModel[]>(`/characteristics/characteristics/`, filters, CharacteristicModel);
export const searchCharacteristicsTypes = () => fetchController.get<CharacteristicTypeModel[]>(`/characteristics/characteristic-types/`, null, CharacteristicTypeModel);
