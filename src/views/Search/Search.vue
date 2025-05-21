<template>
  <div class="search-container">
    <h1>音乐搜索</h1>

    <!-- 搜索框 -->
    <input
      v-model="searchQuery"
      type="text"
      placeholder="输入搜索内容"
      class="search-input"
    />
    <button @click="fetchSearchResults">搜索</button>

    <!-- 显示搜索结果 -->
    <div v-if="filteredResults.length > 0" class="search-results">
      <div v-for="item in filteredResults" :key="item.id" class="result-card">
        <router-link :to="`/player/${item.id}`" class="link-item">
          <div class="result-content">
            <h3 class="result-title">{{ item.title }}</h3>
            <p class="result-author">{{ item.author_name }}</p>
          </div>
        </router-link>
      </div>
    </div>

    <!-- 显示无结果提示 -->
    <div v-else>
      <p>没有找到匹配的内容</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import axios from "@/api/axios"; // 使用axios发送请求

const searchQuery = ref(""); // 用户输入的搜索内容
const filteredResults = ref([]); // 存储后端返回的搜索结果

// 发送搜索请求到后端
const fetchSearchResults = async () => {
  if (!searchQuery.value.trim()) {
    filteredResults.value = [];
    return;
  }

  try {
    const response = await axios.get("/music/music_filter/", {
      params: {
        author_name: "", // 传递作者名作为查询参数
        title: searchQuery.value, // 假设标题为空，或者你可以让用户选择是否输入标题
      },
    });
    filteredResults.value = response.data; // 假设返回的数据是一个数组
    console.log("搜索结果:", response.data);
  } catch (error) {
    console.error("搜索请求失败", error);
    filteredResults.value = [];
  }
};
</script>

<style scoped>
.search-container {
  text-align: center;
  padding: 40px 20px;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.search-input {
  padding: 12px 15px;
  margin: 20px 0;
  border: 1px solid #ccc;
  border-radius: 25px;
  width: 300px;
  font-size: 16px;
  outline: none;
  transition: box-shadow 0.3s ease;
}

.search-input:focus {
  box-shadow: 0 0 5px rgba(81, 203, 238, 1);
}

button {
  padding: 12px 25px;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 25px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #45a049;
}

h1 {
  color: #333;
  margin-bottom: 30px;
  font-size: 2.5em;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
}
.search-results {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
  padding: 20px;
}

.result-card {
  background-color: #f8f8f8;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease-in-out;
}

.result-card:hover {
  transform: translateY(-5px);
}

.link-item {
  text-decoration: none;
  color: inherit;
  display: block;
}

.result-content {
  padding: 15px;
}

.result-title {
  font-size: 18px;
  margin: 0 0 10px 0;
  color: #333;
}

.result-author {
  font-size: 14px;
  color: #666;
  margin: 0;
}
</style>
