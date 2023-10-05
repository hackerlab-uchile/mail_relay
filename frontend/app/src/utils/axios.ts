import axios, { HeadersDefaults } from "axios";

let BACKEND_HOST = process.env.NEXT_PUBLIC_BACKEND_HOST || "http://localhost";
let BACKEND_PORT = process.env.NEXT_PUBLIC_BACKEND_PORT || "8000";

let base_url = BACKEND_HOST + ":" + BACKEND_PORT;
console.log("base_url", base_url);

const apiClient = axios.create({
  baseURL: base_url,
  timeout: 1000,
  headers: {
    Accept: "application/json",
    "Content-Type": "application/json",
  },
});

apiClient.interceptors.request.use(function (config) {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default apiClient;
