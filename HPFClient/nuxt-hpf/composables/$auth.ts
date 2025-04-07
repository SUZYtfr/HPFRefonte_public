/* Juste le temps de passer à vue 3, ensuite dégommer */

import { UserModel } from "~/models";
import { UserPreferencesData, UserProfileData } from "~/types/users";

const mockUser = new UserModel()
mockUser.username = 'Toto'
mockUser.preferences = new UserPreferencesData();
mockUser.preferences.theme = [1, 5, 6, 7][Math.floor(Math.random() * 4)];
mockUser.profile = new UserProfileData();

const mockAuth = {
    loggedIn: false,
    user: null,

    setUser: () => {},
    logout: async () => {},
    loginWith: async () => {
        mockAuth.user = mockUser;
        mockUser.preferences.theme = [1, 5, 6, 7][Math.floor(Math.random() * 4)];
    },
}

export default mockAuth;