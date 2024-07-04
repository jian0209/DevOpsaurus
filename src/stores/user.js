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
import { getInfo } from "src/api/auth";

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
    async getUserInfo() {
      await getInfo().then((res) => {
        console.log(res);
      });
    },
  },
});
