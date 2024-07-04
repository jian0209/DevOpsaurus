const TOKEN_KEY = "DevOpsaurus_token";

export function getToken() {
  return localStorage.getItem(TOKEN_KEY);
}

export function setToken(token) {
  return localStorage.setItem(TOKEN_KEY, token);
}

export function removeToken() {
  return localStorage.removeItem(TOKEN_KEY);
}

const USERNAME_KEY = "DevOpsaurus_username";

export function getUsername() {
  return sessionStorage.getItem(USERNAME_KEY);
}

export function setUsername(username) {
  return sessionStorage.setItem(USERNAME_KEY, username);
}

export function removeUsername() {
  return sessionStorage.removeItem(USERNAME_KEY);
}

const LANGUAGE_KEY = "DevOpsaurus_language";

export function getLanguage() {
  return localStorage.getItem(LANGUAGE_KEY);
}

export function setLanguage(language) {
  return localStorage.setItem(LANGUAGE_KEY, language);
}
