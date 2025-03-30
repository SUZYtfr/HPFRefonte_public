/* eslint-disable @typescript-eslint/explicit-function-return-type */

import fetchController from "~/utils/api";
import type { ICharacteristicFilters } from "@/types/characteristics";
import { CharacteristicTypeModel, CharacteristicModel } from "~/models/characteristics";
import type { UseFetchOptions } from "nuxt/app";

export const searchCharacteristics = (
  filters: ICharacteristicFilters | null,
  options?: UseFetchOptions<CharacteristicModel[]>,
) =>
  fetchController.get<CharacteristicModel[]>(
    "/characteristics/characteristics/",
    filters,
    CharacteristicModel,
    options,
  );

export const searchCharacteristicsTypes = (options?: UseFetchOptions<CharacteristicTypeModel[]>) =>
  fetchController.get<CharacteristicTypeModel[]>(
    "/characteristics/characteristic-types/",
    null,
    CharacteristicTypeModel,
    options,
  );
