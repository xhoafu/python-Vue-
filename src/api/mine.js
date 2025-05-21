import axios from "@/api/axios"


export const mineplaylist = () => {
    return axios.get("playlist/collections/");
  };

export const mine = (data) => {
    return axios.get(`user/user/${data}`);
}