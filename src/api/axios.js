// src/axios.js
import axios from 'axios';

const instance = axios.create({
  baseURL: 'http://127.0.0.1:8000/',
  headers: {
    'Content-Type': 'application/json',
  },
});

let isRefreshing = false;
let refreshSubscribers = [];

// Base64 URL 安全解码函数
function base64UrlDecode(str) {
  let output = str.replace(/-/g, '+').replace(/_/g, '/');
  switch (output.length % 4) {
    case 0: break;
    case 2: output += '=='; break;
    case 3: output += '='; break;
    default: throw new Error('Invalid Base64 string');
  }
  try {
    return decodeURIComponent(escape(atob(output)));
  } catch (e) {
    console.error('Base64 解码失败:', e);
    return null;
  }
}

// Token 过期检查
function checkTokenExpiration(token) {
  try {
    const parts = token.split('.');
    if (parts.length !== 3) throw new Error('Invalid JWT format');
    
    const payload = base64UrlDecode(parts[1]);
    if (!payload) return true;
    
    const { exp } = JSON.parse(payload);
    return exp * 1000 < Date.now();
  } catch (error) {
    console.error('Token 解析失败:', error);
    return true;
  }
}

// 刷新 Token
async function refreshAccessToken(refreshToken) {
  if (isRefreshing) {
    return new Promise((resolve) => {
      refreshSubscribers.push(resolve);
    });
  }

  isRefreshing = true;
  try {
    const response = await axios.post('api/token/refresh/', { refresh: refreshToken });
    const newToken = response.data.access;
    refreshSubscribers.forEach((resolve) => resolve(newToken));
    refreshSubscribers = [];
    return newToken;
  } catch (error) {
    console.error('Token 刷新失败:', error.response?.data || error.message);
    localStorage.removeItem('access');
    localStorage.removeItem('refresh');
    window.location.href = '/login';
    return null;
  } finally {
    isRefreshing = false;
  }
}

// 请求拦截器
instance.interceptors.request.use(async (config) => {
  let token = localStorage.getItem('access');
  const refreshToken = localStorage.getItem('refresh');

  if (token) {
    const isTokenExpired = checkTokenExpiration(token);
    if (isTokenExpired && refreshToken) {
      try {
        const newToken = await refreshAccessToken(refreshToken);
        if (newToken) {
          localStorage.setItem('access', newToken);
          config.headers['Authorization'] = `Bearer ${newToken}`;
        } else {
          return Promise.reject(new Error('Token 刷新失败'));
        }
      } catch (error) {
        return Promise.reject(error);
      }
    } else {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
  }
  return config;
}, (error) => {
  return Promise.reject(error);
});

export default instance;