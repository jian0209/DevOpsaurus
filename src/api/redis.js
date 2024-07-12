import { api } from "src/boot/axios";

export function getRedisList() {
  return api.post("/redis/get_redis_list", {});
}

export function setRedisValue(data) {
  return api.post("/redis/set_redis_value", data);
}
