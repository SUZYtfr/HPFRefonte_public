export interface ICharacteristic {
    characteristic_id: number,
    characteristic_type_id: number,
    parent_id: number,
    name: string,
    description: string,
    in_order: number,
}

export interface ICharacteristicType {
    characteristic_type_id: number,
    creation_user_id: number,
    creation_date: Date,
    modification_user_id: number,
    modification_date: Date,
    name: string,
    min_occurence: number,
    max_occurence: number,
    visible: boolean,
    enabled: boolean
}

export class ICharacteristicGetOptions {
    with_stats: boolean = false;
}

export interface ICharacteristicFilters {
    characteristic_type_id: number | null,
    parent_id: number | null,
    options: ICharacteristicGetOptions | null,
    limit: number | null
}