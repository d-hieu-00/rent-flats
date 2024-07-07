import { toast } from 'vue3-toastify';
import { userApis } from '@/apis/user';
import { SEESION_ID } from '@/config';
import { emitEvent, getCookie, delCookie, isRespError, fetchRespError, isUndefined } from '@/utils';

const NAV_ITEMS = [
  {
    reg: /(\/home|\/home\/.*|^\/$|^$)/,
    val: "home"
  },
  {
    reg: /(\/login)/,
    val: "login"
  },
  {
    reg: /(\/signup)/,
    val: "signup"
  },
  {
    reg: /(\/rented)/,
    val: "rented"
  },
  {
    reg: /(\/feedback)/,
    val: "feedback"
  },
  {
    reg: /(\/bill)/,
    val: "bill"
  },
  {
    reg: /(\/profile)/,
    val: "profile"
  }
]

// initial state
const state = {
    activeNavigation: "home"
}

// getters
const getters = {
  activeNavigation: (state: any) => {
    return state.activeNavigation;
  },
}

// actions
const actions = {
  routedTo({ state }: any, path: string) {
    const navigation = NAV_ITEMS.find((item: any) => item.reg.test(path));
    if (isUndefined(navigation)) {
      state.activeNavigation = "";
    } else {
      state.activeNavigation = navigation?.val;
    }
    emitEvent("update-navigation");
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations: {}
}
