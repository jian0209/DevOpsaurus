import { defineStore } from "pinia";
import { getToken, removeToken } from "src/utils/auth";

export const useUserStore = defineStore("user", {
  state: () => ({
    token: getToken() || "",
    userInfo: null,
  }),

  getters: {
    upperCaseName(state) {
      return state.name.toUpperCase();
    },
  },

  actions: {
    login(token) {
      this.token = token;
    },
    logout() {
      this.token = "";
      this.userInfo = null;
      removeToken();
    },
  },
});
