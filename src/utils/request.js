import axios from 'axios';

const instance = axios.create({
  baseURL: 'http://127.0.0.1:8000/',
  headers: {
    'Content-Type': 'application/json',
  },
});

let isRefreshing = false; // 控制 Token 刷新状态
let refreshSubscribers = []; // 存储等待 Token 刷新的请求

// ✅ 新增：Base64 URL 安全解码函数
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

// ✅ 修改：Token 过期检查函数（兼容错误处理）
function checkTokenExpiration(token) {
  if (!token) return true; // 无 Token 视为过期

  try {
    const parts = token.split('.');
    if (parts.length !== 3) throw new Error('JWT 格式错误');
    
    const payload = base64UrlDecode(parts[1]); // 使用安全解码
    if (!payload) return true;

    const { exp } = JSON.parse(payload);
    return exp * 1000 < Date.now();
  } catch (error) {
    console.error('Token 解析失败:', error);
    localStorage.removeItem('access'); // 清除无效 Token
    return true; // 解析失败视为过期
  }
}

// ✅ 修改：Token 刷新函数（支持并发控制）
async function refreshAccessToken(refreshToken) {
  if (isRefreshing) {
    // 如果正在刷新，返回一个等待中的 Promise
    return new Promise((resolve) => {
      refreshSubscribers.push(resolve);
    });
  }

  isRefreshing = true;
  try {
    const response = await axios.post('api/token/refresh/', { refresh: refreshToken });
    const newToken = response.data.access;
    // 通知所有等待中的请求
    refreshSubscribers.forEach((resolve) => resolve(newToken));
    refreshSubscribers = [];
    return newToken;
  } catch (error) {
    console.error('Token 刷新失败:', error.response?.data || error.message);
    // 清除所有 Token 并跳转登录
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
  const token = localStorage.getItem('access');
  const refreshToken = localStorage.getItem('refresh');

  if (token) {
    const isExpired = checkTokenExpiration(token);
    if (isExpired && refreshToken) {
      try {
        const newToken = await refreshAccessToken(refreshToken);
        if (newToken) {
          localStorage.setItem('access', newToken);
          config.headers.Authorization = `Bearer ${newToken}`;
        } else {
          // 刷新失败，取消当前请求
          return Promise.reject(new Error('Token 刷新失败'));
        }
      } catch (error) {
        return Promise.reject(error);
      }
    } else {
      config.headers.Authorization = `Bearer ${token}`;
    }
  }
  return config;
}, (error) => {
  return Promise.reject(error);
});

export default instance;