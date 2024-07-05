import { toast } from 'vue3-toastify';
import { userApis } from '../../apis/user';
import { getCookie, isRespError, fetchRespError, isUndefined } from '@/utils';
import { SEESION_ID } from '../../config';

// initial state
const state = {
    userInfo: {
        name: "",
        displayName: "",
        isAdmin: "",
        others: {}
    },
    loggedIn: false,
    intervalId: undefined,
    logoutCallback: undefined
}

// getters
const getters = {
    username: (state: any) => {
        return state.userInfo.name;
    },

    displayName: (state: any) => {
        return state.userInfo.displayName;
    },

    isAdmin: (state: any) => {
        return state.userInfo.isAdmin;
    },

    isLoggedIn: (state: any) => {
        return state.userInfo.loggedIn;
    },

    otherInfo: (state: any) => {
        return state.userInfo.others;
    }
}

// actions
const actions = {
    fetchUser({ commit, state }: any) {
        if (isUndefined(getCookie(SEESION_ID))) {
            state.logoutCallback();
            commit("delUserInfo");
            return;
        }
        userApis.fetchUser()
            .then(async (resp: Response) => {
                const data = await resp.json();
                if (isRespError(data)) {
                    const err = fetchRespError(data);
                    throw new Error(err);
                }
                commit("setUserInfo",
                    {
                        username: data["username"],
                        displayName: data["username"],
                        isAdmin: data["admin"] !== 0,
                        others: data
                    }
                );
            }).catch(err => {
                toast.error(err);
                state.logoutCallback();
                commit("delUserInfo");
            });
    },
} 

// mutations
const mutations = {
    startInterval({ state, dispatch }: any) {
        if (!isUndefined(state.intervalId)) {
            clearInterval(state.intervalId);
        }
        state.intervalId = setInterval(() => dispatch("fetchUser"), 60000);
    },

    stopInterval(state: any) {
        if (!isUndefined(state.intervalId)) {
            clearInterval(state.intervalId);
            state.intervalId = undefined;
        }
    },

    setUserInfo({ state, commit }: any, { username, displayName, isAdmin, others }: any) {
        state.userInfo.name = username;
        state.userInfo.displayName = displayName;
        state.userInfo.isAdmin = isAdmin;
        state.userInfo.others = others;
        state.userInfo.isLoggedIn = true;
        commit("startInterval");
    },

    delUserInfo({ state, commit }: any) {
        state.userInfo.name = "";
        state.userInfo.displayName = "";
        state.userInfo.isAdmin = false;
        state.userInfo.others = {};
        state.userInfo.isLoggedIn = false;
        commit("stopInterval");
    },
}

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
}
