import { defineStore } from "pinia";

export const useCommonStore = defineStore("common", {
  state: () => ({
    pageTitle: "",
  }),

  getters: {},

  actions: {
    setPageTitle(title) {
      this.pageTitle = title;
    },
  },
});
