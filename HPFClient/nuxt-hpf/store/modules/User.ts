import { Module, VuexModule, Mutation, Action } from "vuex-module-decorators";
import { login, logout, getUserInfo } from "@/api/users";
// import { getToken, setToken, removeToken } from "@/utils/cookies"

export interface UserState {
  token: string;
  name: string;
  avatar: string;
  introduction: string;
  roles: string[];
}

@Module({
  name: "modules/User",
  namespaced: true,
  stateFactory: true
})
export default class User extends VuexModule implements UserState {
  // public token = getToken() || ""
  public token = "";
  public name = "";
  public avatar = "";
  public introduction = "";
  public roles: string[] = [];

  @Mutation
  // TODO A remettre en privé après le debug
  public SET_TOKEN(token: string): void {
    this.token = token;
  }

  @Mutation
  private SET_NAME(name: string): void {
    this.name = name;
  }

  @Mutation
  private SET_AVATAR(avatar: string): void {
    this.avatar = avatar;
  }

  @Mutation
  private SET_INTRODUCTION(introduction: string): void {
    this.introduction = introduction;
  }

  @Mutation
  private SET_ROLES(roles: string[]): void {
    this.roles = roles;
  }

  @Action
  public async Login(userInfo: { username: string; password: string }): Promise<void> {
    let { username, password } = userInfo;
    username = username.trim();
    password = password.trim();
    const { data } = await login({ username, password });
    // setToken(data.accessToken)
    this.SET_TOKEN(data.accessToken);
  }

  @Action
  public ResetToken(): void {
    // removeToken()
    this.SET_TOKEN("");
    this.SET_ROLES([]);
  }

  @Action
  public async GetUserInfo(): Promise<void> {
    if (this.token === "") {
      throw new Error("GetUserInfo: token is undefined!");
    }
    const { data } = await getUserInfo({ /* Your params here */ });
    if (!data) {
      throw new Error("Verification failed, please Login again.");
    }
    const { roles, name, avatar, introduction } = data.user;
    // roles must be a non-empty array
    if (!roles || roles.length <= 0) {
      throw new Error("GetUserInfo: roles must be a non-null array!");
    }
    this.SET_ROLES(roles);
    this.SET_NAME(name);
    this.SET_AVATAR(avatar);
    this.SET_INTRODUCTION(introduction);
  }

  @Action
  public async LogOut(): Promise<void> {
    if (this.token === "") {
      throw new Error("LogOut: token is undefined!");
    }
    await logout();
    // removeToken()
    this.SET_TOKEN("");
    this.SET_ROLES([]);
  }
}
