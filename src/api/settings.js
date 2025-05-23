import { api } from "src/boot/axios";

export function getUserList(data) {
  return api.post("/user/list", data);
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

export function getRedisList(data) {
  return api.post("/redis/list", data);
}

export function editRedis(data) {
  return api.post("/redis/edit", data);
}

export function editStatusRedis(data) {
  return api.post("/redis/edit_status", data);
}

export function editFavouriteRedis(data) {
  return api.post("/redis/edit_favourite", data);
}

export function deleteRedis(data) {
  return api.post("/redis/delete", data);
}

export function addRedis(data) {
  return api.post("/redis/add", data);
}

export function testRedis(data) {
  return api.post("/redis/test", data);
}

//////////////// end redis ////////////////

export function getUpsList(data) {
  return api.post("/ups/list", data);
}

//////////////// end ups ////////////////

export function getNodesList(data) {
  return api.post("/nodes/list", data);
}

export function editNode(data) {
  return api.post("/nodes/edit", data);
}

export function editStatusNode(data) {
  return api.post("/nodes/edit_status", data);
}

export function deleteNode(data) {
  return api.post("/nodes/delete", data);
}

export function addNode(data) {
  return api.post("/nodes/add", data);
}

//////////////// end nodes ////////////////

export function getDatabaseList(data) {
  return api.post("/database/list", data);
}

export function editDatabase(data) {
  return api.post("/database/edit", data);
}

export function editStatusDatabase(data) {
  return api.post("/database/edit_status", data);
}

export function editFavouriteDatabase(data) {
  return api.post("/database/edit_favourite", data);
}

export function deleteDatabase(data) {
  return api.post("/database/delete", data);
}

export function addDatabase(data) {
  return api.post("/database/add", data);
}

export function getDatabases(data) {
  return api.post("/database/get_databases", data);
}

export function getTables(data) {
  return api.post("/database/get_tables", data);
}

//////////////// end database ////////////////

export function getCommandList(data) {
  return api.post("/command/list", data);
}

export function editCommand(data) {
  return api.post("/command/edit", data);
}

export function editStatusCommand(data) {
  return api.post("/command/edit_status", data);
}

export function editFavouriteCommand(data) {
  return api.post("/command/edit_favourite", data);
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
