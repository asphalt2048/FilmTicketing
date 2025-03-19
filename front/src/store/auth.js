import AuthService from "@/api/authService";

const username = JSON.parse(localStorage.getItem('username'));
const initialState = username
    ?{ status: { loggedIn: true}, username: username}
    :{ status: { loggedIn: false }, username: null };

export  const auth = {
    namespaced: true,
    state: initialState,
    actions: {
        login({commit}, user) {
            return AuthService.login(user).then(
                username => {//to-do
                    commit('loginSuccess', username);
                    return Promise.resolve(username);
                },
                error => {
                    commit('loginFailure');
                    return Promise.reject(error);
                }
            );
        },
        logout({commit}) {
            AuthService.logout();
            commit('logout');
        },
        refreshToken({commit}){
            return AuthService.refreshToken().then(
                access => {
                    console.log("access token refreshed")
                    return Promise.resolve(access)
                },
                error => {
                    alert("refresh failed")
                    commit('logout')
                    return Promise.reject(error)
                }
            )
        }
    },
    mutations: {
        loginSuccess(state, username){
            state.status.loggedIn = true;
            state.username = username;
        },
        loginFailure(state){
            state.status.loggedIn = false;
            state.username = null;
        },
        logout(state){
            state.status.loggedIn = false;
            state.username = null;
        }
    }
};