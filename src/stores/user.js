import { defineStore } from "pinia";
import {
  setToken,
  getToken,
  removeToken,
  getLanguage,
  getUsername,
  setUsername,
  removeUsername,
} from "src/utils/auth";

export const useUserStore = defineStore("user", {
  state: () => ({
    token: getToken(),
    username: getUsername(),
    userInfo: null,
    language: getLanguage() || "en-US",
  }),

  getters: {},

  actions: {
    login(token, username) {
      this.token = token;
      this.username = username;
      setToken(token);
      setUsername(username);
    },
    logout() {
      this.token = null;
      this.userInfo = null;
      this.username = null;
      removeToken();
      removeUsername();
    },
    setUsername(username) {
      this.username = username;
      setUsername(username);
    },
    setUserInfo(userInfo) {
      this.userInfo = userInfo;
    },
  },
});
