import { CharacteristicData } from "~/types/characteristics";

export function getClassTypeColor(characteristic: CharacteristicData): string {
  return getCaracteristicTypeColor(Number(characteristic.characteristicTypeId));
}

export function getCaracteristicTypeColor(characteristicTypeId: number | null): string {
  if (characteristicTypeId == null) return "";
  switch (characteristicTypeId) {
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

export function getCaracteristicTypeColorLight(characteristicTypeId: number | null): string {
  if (characteristicTypeId == null) return "";
  return getCaracteristicTypeColor(characteristicTypeId) + "-light";
}

export function getCaracteristicTypeColorLighter(characteristicTypeId: number | null): string {
  if (characteristicTypeId == null) return "";
  return getCaracteristicTypeColor(characteristicTypeId) + "-lighter";
}

export function getFullPath(characteristic: CharacteristicData, characteristics: CharacteristicData[]): string {
  let result = "";
  if (characteristic.parentId != null) {
    const parentCharacteristic: CharacteristicData | undefined = characteristics.find(
      (pCharacteristic: CharacteristicData) => pCharacteristic.id === characteristic.parentId,
    );
    if (parentCharacteristic != null)
      result = getFullPath(parentCharacteristic, characteristics) + parentCharacteristic.name + " \\ ";
  }
  return result;
}
