
export function authLoginUser(token, user) {
  localStorage.setItem("accessToken", token);
  localStorage.setItem("user", user);
  localStorage.setItem("isAuthenticated", true);
}

export function authlogoutUser() {
  localStorage.removeItem("accessToken");
  localStorage.removeItem("user");
  localStorage.removeItem("isAuthenticated");
  redirect('/login')
}

export function isUserAuthenticated() {
  return localStorage.getItem("isAuthenticated");
}

function redirect(url) {
  window.location.href = url;
}
