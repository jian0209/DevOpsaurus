import { api } from "src/boot/axios";

export function login(data) {
  // username
  // password
  return api.post("/user/login", data);
}

export function logout() {
  return api.post("/user/logout", {});
}

export function getInfo() {
  return api.post("/user/get_user_info", {});
}

export function getMfaImg(data) {
  // username
  return api.post("/user/get_mfa_img", data);
}

export function mfaLogin(data) {
  // username
  // mfa_token
  return api.post("/user/mfa_login", data);
}

export function resetPassword(data) {
  // username
  // password
  return api.post("/user/reset_password", data);
}
