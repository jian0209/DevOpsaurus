import { api } from "src/boot/axios";

export function getLogList(page) {
  return api.post(`/log/list/${page}`, {});
}
