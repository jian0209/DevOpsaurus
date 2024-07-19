import { api } from "src/boot/axios";

export function getRedisList() {
  return api.post("/redis/get_redis_list", {});
}

export function getRedisResult(data) {
  return api.post("/redis/get_redis_result", data);
}

export function setRedisValue(data) {
  return api.post("/redis/set_redis_value", data);
}
