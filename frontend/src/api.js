import axios from 'axios';

export const authApi = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/auth',
});

export const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api',
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