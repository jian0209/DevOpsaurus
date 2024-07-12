import { api } from "src/boot/axios";

export function getDatabaseList() {
  return api.post("/database/get_database_list", {});
}

export function executeQueryToGetData(data) {
  return api.post("/database/execute_query_to_get_data", data);
}
