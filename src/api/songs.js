// songs.js
import axios from '@/api/axios';

export const getMusicRecommendations = async () => {
  try {
    const response = await axios.get("music/recommend/", {
      params: { rec_id: localStorage.getItem("username") }
    });
    return response.data.data;
  } catch (error) {
    console.error("请求失败:", error);
    return [];
  }
};


export const getsong = async (data) => {
  try {
    const response1 = await axios.get(`music/music/${data}/`);
    console.log(response1.data)
    return response1.data;
    
  } catch (error) {
    console.error("获取歌曲信息失败:", error);
    // 可以根据需要返回默认值或抛出错误
    throw error;
  }
};