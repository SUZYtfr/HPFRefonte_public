import { Store } from 'vuex'
import { getModule } from 'vuex-module-decorators'
import User from '~/store/modules/User'
import Config from '~/store/modules/Config'

let UserModule: User
let ConfigModule: Config

function initialiseStores(store: Store<any>): void {
    UserModule = getModule(User, store)
    ConfigModule = getModule(Config, store)
}

export { initialiseStores, UserModule, ConfigModule }