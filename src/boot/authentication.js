import { boot } from "quasar/wrappers";
import { useUserStore } from "src/stores/user";

export default boot(({ router }) => {
  router.beforeEach((to, from, next) => {
    const userStore = useUserStore();
    const loginRoute = "/login";
    const forbiddenRoute = "/forbidden";
    const mfaRegisterRoute = "/login/mfa-register";
    const mfaRoute = "/login/mfa";
    const resetPasswordRoute = "/login/reset-password";

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
        case mfaRegisterRoute:
          next();
          break;
        case mfaRoute:
          next();
          break;
        case resetPasswordRoute:
          next();
          break;
        default:
          next({ path: loginRoute });
      }
    }
  });
});
