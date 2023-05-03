import { Module, VuexModule, Mutation } from "vuex-module-decorators";

@Module({
  name: "modules/ModalsStates",
  namespaced: true,
  stateFactory: true
})
export default class ModalsStates extends VuexModule {
  public loginModalActive: boolean = false;
  public registerModalActive: boolean = false;
  public contactModalActive: boolean = false;

  @Mutation
  public setLoginModalActive(loginModalActive: boolean): void {
    this.loginModalActive = loginModalActive;
  }

  @Mutation
  public setRegisterModalActive(registerModalActive: boolean): void {
    this.registerModalActive = registerModalActive;
  }

  @Mutation
  public setContactModalActive(contactModalActive: boolean): void {
    this.contactModalActive = contactModalActive;
  }
}
