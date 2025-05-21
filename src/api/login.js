import axios from '@/api/axios';

// 登录接口

export const login = (data) => {
  return axios.post("login/", {
    username: data.username,
    password: data.password,
  });
};