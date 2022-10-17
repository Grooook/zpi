import { API_URL } from "constants/api";

export async function getSearchHelp() {
    const response = await fetch(API_URL + 'get_applications/');
    const responseData = await response.json();
    return responseData;
}

export async function login(credentials) {
    return fetch(API_URL + "login/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(credentials),
    }).then((data) => data.json());
}