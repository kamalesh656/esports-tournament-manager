import axios from 'axios';

const BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

export const authApi = axios.create({
  baseURL: `${BASE_URL}/api/auth`,
});

export const api = axios.create({
  baseURL: `${BASE_URL}/api`,
});

// Attach token automatically to every request
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default authApi;