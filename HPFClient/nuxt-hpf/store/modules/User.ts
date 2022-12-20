import { Module, VuexModule, Mutation, Action } from 'vuex-module-decorators'
import { login, logout, getUserInfo } from '@/api/account'
import { AccountData, TokenResponse } from '@/types/account'
//import { getToken, setToken, removeToken } from '@/utils/cookies'

export interface UserState {
  token: string;
  nickname: string;
  email: string;
  realname: string;
  avatar: string;
  bio: string;
  roles: string[];
}

@Module({
    name: 'modules/User',
    namespaced: true,
    stateFactory: true,
  })
export default class User extends VuexModule implements UserState {
  //public token = getToken() || ''
  public token = ''
  public nickname = ''
  public email = ''
  public realname = ''
  public avatar = ''
  public bio = ''
  public roles: string[] = []

  @Mutation
  //A remettre en privé après le debug
  public SET_TOKEN(token: string) {
    this.token = token
  }

  @Mutation
  private SET_REALNAME(realname: string) {
    this.realname = realname
  }

  @Mutation
  private SET_NICKNAME(nickname: string) {
    this.nickname = nickname
  }

  @Mutation
  private SET_AVATAR(avatar: string) {
    this.avatar = avatar
  }

  @Mutation
  private SET_BIO(bio: string) {
    this.bio = bio
  }

  @Mutation
  private SET_ROLES(roles: string[]) {
    this.roles = roles
  }

  @Mutation
  private SET_USER_STATE(data: AccountData) {
    this.nickname = data.username;
    this.realname = data.profile.realname;
    this.email = data.email;
    this.bio = data.profile.bio;
  }

  @Action
  public async Login(userInfo: { nickname: string, password: string }) {
    let { nickname, password } = userInfo
    nickname = nickname.trim();
    password = password.trim();
    const response = (await login({ nickname, password })).data as TokenResponse;
    //setToken(data.accessToken)
    this.SET_TOKEN(response.access);
  }

  @Action
  public ResetToken() {
    //removeToken()
    this.SET_TOKEN('')
    this.SET_ROLES([])
  }

  @Action
  public async GetUserInfo() {
    if (this.token === '') {
      throw Error('GetUserInfo: token is undefined!');
    }
    const { data } = await getUserInfo();
    if (!data) {
      throw Error('Verification failed, please Login again.')
    }

    //roles must be a non-empty array
//     if (!roles || roles.length <= 0) {
//       throw Error('GetUserInfo: roles must be a non-null array!')
//     }
    this.SET_USER_STATE(data.results)
  }

  @Action
  public async LogOut() {
    if (this.token === '') {
      throw Error('LogOut: token is undefined!')
    }
    await logout()
    //removeToken()
    this.SET_TOKEN('')
    this.SET_ROLES([])
  }
}
