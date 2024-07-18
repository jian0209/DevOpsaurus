import { boot } from "quasar/wrappers";
import { useUserStore } from "src/stores/user";
import { ADMIN_ROLE, EDITOR_ROLE, READER_ROLE } from "src/utils/constants";

export default boot(({ router }) => {
  router.beforeEach((to, from, next) => {
    const userStore = useUserStore();
    const loginRoute = "/login";
    const forbiddenRoute = "/forbidden";
    const mfaRegisterRoute = "/login/mfa-register";
    const mfaRoute = "/login/mfa";
    const resetPasswordRoute = "/login/reset-password";
    const settingsRoute = "/settings";
    const logRoute = "/log";
    const redisSetRoute = "/redis/set";
    const nodesEditRoute = "/nodes/edit";
    const databaseEditRoute = "/database/edit";
    const databaseScheduleRoute = "/database/schedule";
    const commandRoute = "/command";
    const redisRoute = "/redis";
    const databaseRoute = "/database";
    const dashboardRoute = "/dashboard";

    const token = userStore.token;

    if (token) {
      if (
        (to.path.includes(settingsRoute) || to.path.includes(logRoute)) &&
        parseInt(userStore.role) !== ADMIN_ROLE
      ) {
        next({ path: forbiddenRoute });
      } else if (
        (to.path.includes(redisSetRoute) ||
          to.path.includes(nodesEditRoute) ||
          to.path.includes(databaseEditRoute) ||
          to.path.includes(databaseScheduleRoute) ||
          to.path.includes(commandRoute)) &&
        parseInt(userStore.role) !== EDITOR_ROLE &&
        parseInt(userStore.role) !== ADMIN_ROLE
      ) {
        next({ path: forbiddenRoute });
      } else if (
        (to.path.includes(redisRoute) || to.path.includes(databaseRoute)) &&
        parseInt(userStore.role) !== READER_ROLE &&
        parseInt(userStore.role) !== EDITOR_ROLE &&
        parseInt(userStore.role) !== ADMIN_ROLE
      ) {
        next({ path: forbiddenRoute });
      } else if (to.path === dashboardRoute && parseInt(userStore.role) === 0) {
        next({ path: "/ups-monitor" });
      } else if (to.path === loginRoute) {
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
