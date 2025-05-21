import axios from "@/api/axios"
export const register = (data) => {
  return axios.post("/user/user/", {
  username: data.username,
  email: data.email,
  password: data.password,
});}