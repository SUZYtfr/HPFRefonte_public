import { Store } from "vuex";
import { getModule } from "vuex-module-decorators";
import User from "~/store/modules/User";
import Config from "~/store/modules/Config";
import ModalsStates from "~/store/modules/ModalsStates";

let UserModule: User;
let ConfigModule: Config;
let ModalsStatesModule: ModalsStates;

function initialiseStores(store: Store<any>): void {
  UserModule = getModule(User, store);
  ConfigModule = getModule(Config, store);
  ModalsStatesModule = getModule(ModalsStates, store);
}

export { initialiseStores, UserModule, ConfigModule, ModalsStatesModule };
