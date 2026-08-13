import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests if available
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Token ${token}`;
  }
  return config;
});

export const authService = {
  register: (userData) => api.post('/register/', userData),
  login: (credentials) => api.post('/login/', credentials),
  logout: () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  },
};

export const caseService = {
  create: (data) => api.post('/cases/', data),
  uploadDocuments: (caseId, files) => {
    const formData = new FormData();
    files.forEach((file) => formData.append('documents', file));
    return api.post(`/cases/${caseId}/upload/`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
  getMyCases: () => api.get('/cases/my/'),  // <-- Dashboard uses this
  getCaseDetail: (caseId) => api.get(`/cases/${caseId}/`),
};

export default api;