import { defineStore } from "pinia";
import { setToken, getToken, removeToken, getLanguage } from "src/utils/auth";

export const useUserStore = defineStore("user", {
  state: () => ({
    token: getToken(),
    userInfo: null,
    language: getLanguage() || "en-US",
  }),

  getters: {},

  actions: {
    login(token, userInfo) {
      this.token = token;
      this.userInfo = userInfo;
      setToken(token);
    },
    logout() {
      this.token = null;
      this.userInfo = null;
      removeToken();
    },
  },
});
