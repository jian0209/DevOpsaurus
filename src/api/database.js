import { api } from "src/boot/axios";

export function getDatabaseList(data) {
  return api.post("/database/get_database_list", data);
}

export function executeQueryToGetData(data) {
  return api.post("/database/execute_query_to_get_data", data);
}
