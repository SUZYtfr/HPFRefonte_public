import { Store } from "vuex";
import { getModule } from "vuex-module-decorators";
import Config from "~/store/modules/Config";
import ModalsStates from "~/store/modules/ModalsStates";

let ConfigModule: Config;
let ModalsStatesModule: ModalsStates;

function initialiseStores(store: Store<any>): void {
  ConfigModule = getModule(Config, store);
  ModalsStatesModule = getModule(ModalsStates, store);
}

export { initialiseStores, ConfigModule, ModalsStatesModule };
