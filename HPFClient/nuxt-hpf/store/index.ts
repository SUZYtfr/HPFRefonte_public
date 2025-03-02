import type { Context } from "@nuxt/types";
import type { ActionTree } from "vuex";
import { getModule } from "vuex-module-decorators";
import Config from "~/store/modules/Config";
import Common from "~/store/modules/CommonState";

export interface RootState {
  description: string
}

// export const state = (): RootState => ({
//   description: "I'm defined as an initial state"
// })

// export const getters: GetterTree<RootState, RootState> = {
//   reversedName: (state): string => state.description.split('').reverse().join('')
// }

// export const MutationType = {
//   CHANGE_DESCRIPTION: 'changeDescription'
// }

// export const mutations: MutationTree<RootState> = {
//   [MutationType.CHANGE_DESCRIPTION]: (state, newDescription: string) => { state.description = newDescription }
// }

export const actions: ActionTree<RootState, RootState> = {
  async nuxtServerInit({ commit }, _context: Context) {
    const configModule = getModule(Config, _context.store);
    await configModule.LoadConfig();
    // On indique un rafrachissement de la page
    const commonModule = getModule(Common, _context.store);
    commonModule.setWasRefreshed(true);
  }
};

// import { Store } from "vuex";
// import { initialiseStores } from "~/utils/store-accessor";
// const initializer = (store: Store<any>): any => initialiseStores(store);
// export const plugins = [initializer];
// export * from "~/utils/store-accessor";

// import Vuex from "vuex";
// import ModalsStates from "~/store/modules/ModalsStates";
// import Config from "~/store/modules/Config";

// export function createStore() {
//     return new Vuex.Store({
//         modules: {
//             ModalsStates,
//             Config,
//         }
//     })
// }
