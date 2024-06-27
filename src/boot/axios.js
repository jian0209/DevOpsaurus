import { boot } from "quasar/wrappers";
import axios from "axios";

// Be careful when using SSR for cross-request state pollution
// due to creating a Singleton instance here;
// If any client changes this (global) instance, it might be a
// good idea to move this instance creation inside of the
// "export default () => {}" function below (which runs individually
// for each client)
const api = axios.create({
  baseURL: "http://localhost:9001",
  timeout: 10000,
});

api.interceptors.request.use(
  (config) => {
    // do something before request is sent
    // const store = useUserStore()
    // if (store.token) {
    //   // let each request carry token
    //   config.headers['X-Token'] = store.token
    // }
    // return config
  },
  (error) => {
    // do something with request error
    return Promise.reject(error);
  },
);

// response interceptor
api.interceptors.response.use(
  (response) => {
    const res = response.data;
    if (response.status === 200) {
      return {
        data: res,
        code: 0,
        msg: response.statusText || "success",
        success: true,
      };
    }
    return Promise.reject({
      data: res,
      code: response.status,
      msg: response.statusText || "error",
      success: false,
    });
  },
  (error) => {
    const headers = error.response.headers;
    const msg = headers["x-error-msg"];
    const code = headers["x-error-ret"];

    return Promise.reject({
      data: error.response,
      code: code,
      msg: msg || error.message,
      success: false,
    });
  },
);

export default boot(({ app }) => {
  // for use inside Vue files (Options API) through this.$axios and this.$api

  app.config.globalProperties.$axios = axios;
  // ^ ^ ^ this will allow you to use this.$axios (for Vue Options API form)
  //       so you won't necessarily have to import axios in each vue file

  app.config.globalProperties.$api = api;
  // ^ ^ ^ this will allow you to use this.$api (for Vue Options API form)
  //       so you can easily perform requests against your app's API
});

export { api };
