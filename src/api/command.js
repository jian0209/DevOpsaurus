import { api } from "src/boot/axios";

export function getCommandList() {
  return api.post("/command/command_list", {});
}

export function executeCommand(data) {
  return api.post("/command/execute", data);
}
