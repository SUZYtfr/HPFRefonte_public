export interface ICharacteristic {
    characteristic_id: number,
    characteristic_type_id: number,
    parent_id: number,
    name: string,
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