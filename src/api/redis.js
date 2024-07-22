import { api } from "src/boot/axios";

export function getRedisList(data) {
  return api.post("/redis/get_redis_list", data);
}

export function getRedisResult(data) {
  return api.post("/redis/get_redis_result", data);
}

export function setRedisValue(data) {
  return api.post("/redis/set_redis_value", data);
}
