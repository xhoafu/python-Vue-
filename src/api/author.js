import axios from '@/api/axios';


export const authorDetalist = (data) => {
    return axios.get(`music/authorbanner/${data}/`);
  };