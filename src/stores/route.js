import { defineStore } from "pinia";

export const useRouteStore = defineStore("router", {
  actions: {
    routeTo(route) {
      this.router.push(route);
    },
  },
});
