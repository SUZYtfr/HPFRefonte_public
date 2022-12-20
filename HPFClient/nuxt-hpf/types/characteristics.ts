import { QueryParams, PaginatedResponse } from "@/types/basics";

export interface ICharacteristic {
    id: number;
    category_id: number;
    parent_id?: number;
    name: string;
    description?: string;
    order: number;
    fiction_count?: number;
}

export interface ICharacteristicType {
    id: number;
    name: string;
    min_limit: number;
    max_limit?: number;
}

export interface CharacteristicQueryParams extends QueryParams {
    category_id?: number;
    parent_id?: number;
    with_fiction_count?: boolean;
}

export interface ICharacteristicResponse extends PaginatedResponse {
  results: ICharacteristic[];
}

export interface ICharacteristicTypeResponse extends PaginatedResponse {
  results: ICharacteristicType[];
}
