import { Module, VuexModule, Mutation, Action } from "vuex-module-decorators";
import { plainToInstance } from "class-transformer";
import {
  getCharacteristics,
  getCharacteristicsTypes
} from "@/api/characteristics";
import {
  getPublicThemes
} from "@/api/themes";
import { CharacteristicModel, CharacteristicTypeModel } from "~/models/characteristics";
import { ThemeModel } from "~/models/themes";

export interface ConfigState {
  characteristics: CharacteristicModel[];
  characteristicTypes: CharacteristicTypeModel[];
  themes: ThemeModel[];
}

@Module({
  name: "modules/Config",
  namespaced: true,
  stateFactory: true
})
export default class _Config extends VuexModule implements ConfigState {
  private _characteristics: CharacteristicModel[] = [];
  private _characteristicTypes: CharacteristicTypeModel[] = [];
  private _themes: ThemeModel[] = [];

  public get characteristics(): CharacteristicModel[] {
    if (process.client && this._characteristics != null && this._characteristics.length > 0 && (this._characteristics[0] instanceof CharacteristicModel) === false) {
      return plainToInstance(
        CharacteristicModel,
        this._characteristics
      );
    }
    return this._characteristics;
  }

  public get characteristicTypes(): CharacteristicTypeModel[] {
    if (process.client && this._characteristicTypes != null && this._characteristicTypes.length > 0 && (this._characteristicTypes[0] instanceof CharacteristicTypeModel) === false) {
      return plainToInstance(
        CharacteristicTypeModel,
        this._characteristicTypes
      );
    }
    return this._characteristicTypes;
  }

  public get themes(): ThemeModel[] {
    if (process.client && this._themes != null && this._themes.length > 0 && (this._themes[0] instanceof ThemeModel) === false) {
      return plainToInstance(
        ThemeModel,
        this._themes
      );
    }
    return this._themes;
  }

  // Theme actuel de l'utilisateur courant
  public get currentTheme(): ThemeModel | null {
    let currentTheme = null;
    // Theme évènementiel
    currentTheme = this._themes.find(theme => theme.use_default_from != null && theme.use_default_to != null && theme.use_default_from <= new Date() && theme.use_default_to >= new Date()) ?? null;

    if (process.client) {
      // Cas utilisateur connecté
      if (window.$nuxt.$auth.loggedIn && window.$nuxt.$auth.user?.preferences != null) {
        // Theme utilisateur
        // (si le thème évènementiel est null ou si l'utilisateur a overridé son thème)
        if ((currentTheme == null) ||
          ((window.$nuxt.$auth.user.preferences as any).theme_overriden_at != null &&
            currentTheme.use_default_to != null &&
            new Date((window.$nuxt.$auth.user.preferences as any).theme_overriden_at) > currentTheme.use_default_to))
          currentTheme = this._themes.find(theme => theme.id === (window.$nuxt.$auth.user?.preferences as any).theme) ?? null;
      }
    }

    // Theme par défaut si pas de thème évènementiel / pas de thème utilisateur
    if (currentTheme == null) currentTheme = this._themes.find(theme => theme.default) ?? null;

    return currentTheme;
  }

  @Mutation
  public SET_CHARACTERISTICS(characteristics: CharacteristicModel[]): void {
    this._characteristics = characteristics;
  }

  @Mutation
  public SET_CHARACTERISTIC_TYPES(characteristicTypes: CharacteristicTypeModel[]): void {
    this._characteristicTypes = characteristicTypes;
  }

  @Mutation
  public SET_THEMES(themes: ThemeModel[]): void {
    this._themes = themes;
  }

  // @Action
  // public CaracteristicToInstance(): void {
  //   this.SET_CHARACTERISTICS(plainToInstance(
  //     CharacteristicModel,
  //     this._characteristics
  //   ));
  // }

  // public CaracteristicTypeToInstance(): void {
  //   this.SET_CHARACTERISTIC_TYPES(plainToInstance(
  //     CharacteristicTypeModel,
  //     this._characteristicTypes
  //   ));
  // }

  @Action
  public async LoadConfig(): Promise<void> {
    let caracteristicsTemp;
    let caracteristicTypesTemp;
    let themesTemp;

    try {
      caracteristicsTemp = (await getCharacteristics(null));
    } catch (error) {
      caracteristicsTemp = [];
      console.log(error);
    }

    try {
      caracteristicTypesTemp = (await getCharacteristicsTypes());
    } catch (error) {
      caracteristicTypesTemp = [];
      console.log(error);
    }

    try {
      themesTemp = (await getPublicThemes(null)).results;
    } catch (error) {
      themesTemp = [];
      console.log(error);
    }

    this.SET_CHARACTERISTICS(caracteristicsTemp);
    this.SET_CHARACTERISTIC_TYPES(caracteristicTypesTemp);
    this.SET_THEMES(themesTemp);
  }

  @Action
  public ResetConfig(): void {
    this.SET_CHARACTERISTICS([]);
    this.SET_CHARACTERISTIC_TYPES([]);
    this.SET_THEMES([]);
  }
}
