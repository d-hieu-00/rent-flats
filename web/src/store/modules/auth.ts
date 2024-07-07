import { toast } from 'vue3-toastify';
import { userApis } from '@/apis/user';
import { SEESION_ID } from '@/config';
import { emitEvent, getCookie, delCookie, isRespError, fetchRespError, isUndefined } from '@/utils';

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
    console.log("form getters.isLoggedIn", state)
    return state.loggedIn;
  },

  otherInfo: (state: any) => {
    return state.userInfo.others;
  }
}

// actions
const actions = {
  fetchUser({ dispatch, state }: any) {
    if (isUndefined(getCookie(SEESION_ID))) {
      if (!isUndefined(state.logoutCallback))
        state.logoutCallback();
      dispatch("delUserInfo");
      return;
    }
    userApis.fetchUser()
      .then(async (resp: Response) => {
        const data = await resp.json();
        if (isRespError(data)) {
          throw fetchRespError(data);
        }
        dispatch("setUserInfo",
          {
            username: data["username"],
            displayName: data["username"],
            isAdmin: data["admin"] !== 0,
            others: data
          }
        );
      }, async (respErr: Response) => {
        throw fetchRespError(await respErr.json());
      }).catch(err => {
        toast.error(err);
        if (!isUndefined(state.logoutCallback))
          state.logoutCallback();
        dispatch("delUserInfo");
      });
  },

  startInterval({ state, dispatch }: any) {
    if (isUndefined(state.intervalId)) {
      state.intervalId = setInterval(() => dispatch("fetchUser"), 3000);
    }
  },

  setUserInfo({ state, dispatch }: any, { username, displayName, isAdmin, others }: any) {
    state.userInfo.name = username;
    state.userInfo.displayName = displayName;
    state.userInfo.isAdmin = isAdmin;
    state.userInfo.others = others;
    state.loggedIn = true;
    console.log("setUserInfo", state.loggedIn)
    emitEvent('user-info-change');
    dispatch("startInterval");
  },

  delUserInfo({ state, dispatch }: any) {
    state.userInfo.name = "";
    state.userInfo.displayName = "";
    state.userInfo.isAdmin = false;
    state.userInfo.others = {};
    state.loggedIn = false;

    console.log("delUserInfo", state.loggedIn)
    emitEvent('user-info-change');
    delCookie(SEESION_ID);
    dispatch("stopInterval");
  },

  stopInterval({ state }: any) {
    const id = state.intervalId;
    if (!isUndefined(state.intervalId)) {
      clearInterval(state.intervalId);
      state.intervalId = undefined;
    }
  },
}

// mutations
const mutations = {
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
