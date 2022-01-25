import { ICharacteristic } from "@/types/characteristics";

export function getClassTypeColor(characteristic: ICharacteristic): string {
    return getCaracteristicTypeColor(characteristic.characteristic_type_id);
}

export function getCaracteristicTypeColor(characteristic_type_id: number): string {
    switch (characteristic_type_id) {
        case 1:
            return "characteristic-bg-litteraire";
        case 2:
            return "characteristic-bg-genre";
        case 3:
            return "characteristic-bg-langue";
        case 4:
            return "characteristic-bg-warning";
        case 5:
            return "characteristic-bg-rating";
        case 6:
            return "characteristic-bg-epoque";
        case 7:
            return "characteristic-bg-personnage";
        case 8:
            return "characteristic-bg-relation";
        default:
            return "";
    }
}

export function getFullPath(characteristic: ICharacteristic, characteristics: ICharacteristic[]): string {
    let result = "";
    if (characteristic.parent_id != null) {
        const parentCharacteristic: ICharacteristic | undefined =
            characteristics.find(
                (pCharacteristic: ICharacteristic) =>
                    pCharacteristic.characteristic_id == characteristic.parent_id
            );
        if (parentCharacteristic != null)
            result = getFullPath(parentCharacteristic, characteristics) +
                parentCharacteristic.name +
                " \\ ";
    }
    return result;
}