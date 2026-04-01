import axios from "axios";
import { getToken } from "../utils/auth";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000",
});

api.interceptors.request.use((config) => {
  const token = getToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export async function registerUser(data) {
  const response = await api.post("/auth/register", data);
  return response.data;
}

export async function loginUser(data) {
  const response = await api.post("/auth/login", data);
  return response.data;
}

export async function getProfile() {
  const response = await api.get("/auth/profile");
  return response.data;
}

export async function getTrendingBooks() {
  const response = await api.get("/recommendations/trending");
  return response.data;
}

export async function searchBooks(data) {
  const response = await api.post("/recommendations/", data);
  return response.data;
}

export async function getRecentRecommendations() {
  const response = await api.get("/recommendations/recent");
  return response.data;
}

export default api;