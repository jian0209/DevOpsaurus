import { boot } from "quasar/wrappers";
import { useUserStore } from "src/stores/user";

export default boot(({ router }) => {
  router.beforeEach((to, from, next) => {
    const userStore = useUserStore();
    const loginRoute = "/login";
    const forbiddenRoute = "/forbidden";

    const token = userStore.token;

    if (token) {
      if (to.path === loginRoute) {
        next({ path: "/dashboard" });
      } else if (to.path === "/") {
        next({ path: "/dashboard" });
      } else {
        next();
      }
    } else {
      switch (to.path) {
        case forbiddenRoute:
          next();
          break;
        case loginRoute:
          next();
          break;
        default:
          next({ path: loginRoute });
      }
    }
  });
});
