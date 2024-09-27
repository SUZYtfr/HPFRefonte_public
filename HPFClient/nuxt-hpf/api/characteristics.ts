import $AxiosWrapper from "~/utils/api";
import $ApolloWrapper from "~/utils/apolloApi";
import characteristicsQuery from "./queries/characteristicsQuery.gql";
import characteristicTypesQuery from "./queries/characteristicTypesQuery.gql";
import { ICharacteristicFilters } from "@/types/characteristics";
import { CharacteristicTypeModel, CharacteristicModel } from "~/models/characteristics";

// export const getCharacteristics = (filters: ICharacteristicFilters | null): Promise<any> => $AxiosWrapper.get<CharacteristicModel>("/characteristics/characteristics/", filters, CharacteristicModel);
export const createCharacteristic = (characteristic: CharacteristicModel): Promise<any> => $AxiosWrapper.post<CharacteristicModel>("/characteristics/characteristics/", characteristic, CharacteristicModel);
export const updateCharacteristic = (characteristic: CharacteristicModel): Promise<any> => $AxiosWrapper.put<CharacteristicModel>("/characteristics/characteristics/" + characteristic.characteristicId + "/", characteristic, CharacteristicModel);
export const deleteCharacteristic = (characteristic: CharacteristicModel): Promise<any> => $AxiosWrapper.delete<CharacteristicModel>("/characteristics/characteristics/" + characteristic.characteristicId + "/", CharacteristicModel);

// export const getCharacteristicsTypes = (): Promise<any> => $AxiosWrapper.get<CharacteristicTypeModel>("/characteristics/characteristic-types/", null, CharacteristicTypeModel);
export const updateCharacteristicsType = (characteristicType: CharacteristicTypeModel): Promise<any> => $AxiosWrapper.put<CharacteristicTypeModel>("/characteristics/characteristic-types/" + characteristicType.characteristicTypeId + "/", characteristicType, CharacteristicTypeModel);
export const reorderCharacteristics = (characteristicType: CharacteristicTypeModel, newOrder: Array<Number>): Promise<any> => $AxiosWrapper.put<Array<Number>>("/characteristics/characteristic-types/" + characteristicType.characteristicTypeId + " /order/", {order: newOrder});

export const getCharacteristics = (filters: ICharacteristicFilters | null): Promise<any> => $ApolloWrapper.query<CharacteristicModel>(characteristicsQuery, null, "paginatedCharacteristics", CharacteristicModel);
export const getCharacteristicsTypes = (): Promise<any> => $ApolloWrapper.query<CharacteristicTypeModel>(characteristicTypesQuery, null, "paginatedCharacteristicTypes", CharacteristicTypeModel);