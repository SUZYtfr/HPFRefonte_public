import { Module, VuexModule, Mutation } from "vuex-module-decorators";

@Module({
  name: "modules/CommonState",
  namespaced: true,
  stateFactory: true
})
export default class CommonState extends VuexModule {
  public wasRefreshed: boolean = false;

  @Mutation
  public setWasRefreshed(wasRefreshed: boolean): void {
    this.wasRefreshed = wasRefreshed;
  }
}
