import axios from "axios";

const BASE = "http://127.0.0.1:8000/api";

function getToken() {
  return localStorage.getItem("access_token") || "";
}

const api = axios.create({
  baseURL: BASE,
});

api.interceptors.request.use((config) => {
  const token = getToken();
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

export async function login(username, password) {
  const res = await api.post("/login/", { username, password });
  const { access, refresh } = res.data;
  localStorage.setItem("access_token", access);
  localStorage.setItem("refresh_token", refresh);
  return true;
}

export function logout() {
  localStorage.removeItem("access_token");
  localStorage.removeItem("refresh_token");
}

export async function getHistory() {
  const res = await api.get("/history/");
  return res.data;
}

export async function uploadCSV(file) {
  const fd = new FormData();
  fd.append("file", file);
  const res = await api.post("/upload/", fd, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return res.data;
}

function authHeaders() {
  const token = localStorage.getItem("access_token"); 
  return token ? { Authorization: `Bearer ${token}` } : {};
}

export async function downloadReport() {
  const res = await axios.get(`${BASE}/report/`, {
    responseType: "blob",
    headers: authHeaders(),
  });
  return res.data;
}