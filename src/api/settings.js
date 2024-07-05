import { api } from "src/boot/axios";

export function getUserList() {
  return api.post("/user/list", {});
}

export function editUser(data) {
  return api.post("/user/edit", data);
}

export function editStatusUser(data) {
  return api.post("/user/edit_status", data);
}

export function deleteUser(data) {
  return api.post("/user/delete", data);
}

export function addUser(data) {
  return api.post("/user/add", data);
}

//////////////// end user ////////////////

export function getRedisList() {
  return api.post("/redis/list", {});
}

//////////////// end redis ////////////////

export function getUpsList() {
  return api.post("/ups/list", {});
}

//////////////// end ups ////////////////

export function getNodesList() {
  return api.post("/nodes/list", {});
}

//////////////// end nodes ////////////////

export function getDatabaseList() {
  return api.post("/database/list", {});
}

//////////////// end database ////////////////

export function getCommandList() {
  return api.post("/command/list", {});
}

export function editCommand(data) {
  return api.post("/command/edit", data);
}

export function editStatusCommand(data) {
  return api.post("/command/edit_status", data);
}

export function deleteCommand(data) {
  return api.post("/command/delete", data);
}

export function addCommand(data) {
  return api.post("/command/add", data);
}

export function testCommand(data) {
  return api.post("/command/test", data);
}

//////////////// end command ////////////////

export function getSettings(page) {
  return api.post(`/settings/get/${page}`, {});
}

export function saveSettings(page, data) {
  return api.post(`/settings/save/${page}`, data);
}

export function testSettings(page, data) {
  return api.post(`/settings/test/${page}`, data);
}

//////////////// end setting ////////////////
