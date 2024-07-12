import { defineStore } from "pinia";
import {
  setLocalToken,
  getLocalToken,
  removeLocalToken,
  setSessionUsername,
  getSessionUsername,
  removeSessionUsername,
  setLocalRole,
  getLocalRole,
  removeLocalRole,
  setLocalLanguage,
  getLocalLanguage,
} from "src/utils/auth";

export const useUserStore = defineStore("user", {
  state: () => ({
    token: getLocalToken(),
    username: getSessionUsername(),
    role: getLocalRole(),
    userInfo: null,
    language: getLocalLanguage() || "en-US",
  }),

  getters: {},

  actions: {
    login(token, username, role) {
      this.setToken(token);
      this.setUsername(username);
      this.setRole(role);
    },
    logout() {
      this.token = null;
      this.userInfo = null;
      this.username = null;
      this.role = null;
      removeLocalToken();
      removeSessionUsername();
      removeLocalRole();
    },
    setToken(token) {
      this.token = token;
      setLocalToken(token);
    },
    setUsername(username) {
      this.username = username;
      setSessionUsername(username);
    },
    setRole(role) {
      this.role = role;
      setLocalRole(role);
    },
    setUserInfo(userInfo) {
      this.userInfo = userInfo;
    },
  },
});
