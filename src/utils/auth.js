const TOKEN_KEY = "DevOpsaurus_token";

export function getLocalToken() {
  return localStorage.getItem(TOKEN_KEY);
}

export function setLocalToken(token) {
  return localStorage.setItem(TOKEN_KEY, token);
}

export function removeLocalToken() {
  return localStorage.removeItem(TOKEN_KEY);
}

const USERNAME_KEY = "DevOpsaurus_username";

export function getSessionUsername() {
  return sessionStorage.getItem(USERNAME_KEY);
}

export function setSessionUsername(username) {
  return sessionStorage.setItem(USERNAME_KEY, username);
}

export function removeSessionUsername() {
  return sessionStorage.removeItem(USERNAME_KEY);
}

const ROLE_KEY = "DevOpsaurus_role";

export function getLocalRole() {
  return localStorage.getItem(ROLE_KEY);
}

export function setLocalRole(role) {
  return localStorage.setItem(ROLE_KEY, role);
}

export function removeLocalRole() {
  return localStorage.removeItem(ROLE_KEY);
}

const LANGUAGE_KEY = "DevOpsaurus_language";

export function getLocalLanguage() {
  return localStorage.getItem(LANGUAGE_KEY);
}

export function setLocalLanguage(language) {
  return localStorage.setItem(LANGUAGE_KEY, language);
}
