import { api } from "src/boot/axios";

export function getCommandList(data) {
  return api.post("/command/command_list", data);
}

export function executeCommand(data) {
  return api.post("/command/execute", data);
}
