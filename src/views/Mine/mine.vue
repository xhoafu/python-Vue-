<template>
  <div class="mine-container">
    <div v-if="isLoggedIn">
      <h1>用户信息</h1>
      <div class="user-info" v-if="user">
        <p>用户名: {{ user.username }}</p>
        <p>用户 ID: {{ user.id }}</p>
        <p>邮箱: {{ user.email }}</p>
        <p>是否超级用户: {{ user.is_superuser ? "是" : "否" }}</p>
        <p>是否活跃: {{ user.is_active ? "是" : "否" }}</p>
        <p>最后登录时间: {{ user.last_login }}</p>
        <p>注册时间: {{ user.date_joined }}</p>
      </div>
      <div v-else>
        <p>加载中...</p>
      </div>
    </div>
    <div v-else>
      <div class="login-prompt">
        <h2>欢迎访问</h2>
        <p>请登录以查看您的个人信息。</p>
        <button class="login-button">登录</button>
        <p>还没有账号？<a href="/register">立即注册</a></p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { mine } from "@/api/mine"; // 假设 mine 是一个获取用户信息的函数

// 用户信息
const user = ref(null);
const isLoggedIn = ref(false);
const isLoading = ref(false);

// 检查 user_id 并获取用户信息
const checkUserAndFetchData = async () => {
  isLoading.value = true;
  // 获取 user_id
  const user_id = localStorage.getItem("user_id");

  if (user_id) {
    console.log("user_id 存在，获取用户信息");
    isLoggedIn.value = true;

    try {
      const response = await mine(user_id);
      user.value = response.data;
      console.log("用户信息获取成功:", user.value);
    } catch (error) {
      console.error("获取用户信息失败:", error);
      isLoggedIn.value = false;
    } finally {
      isLoading.value = false;
    }
  } else {
    // 如果 user_id 不存在，不执行命令
    console.log("user_id 不存在，不执行命令");
    isLoggedIn.value = false;
    isLoading.value = false;
  }
};

// 在组件挂载后执行
onMounted(() => {
  checkUserAndFetchData();
});
</script>

<style scoped>
.mine-container {
  padding: 20px;
  max-width: 600px;
  margin: 0 auto;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.user-info {
  margin-top: 20px;
  padding: 20px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.user-info p {
  margin: 10px 0;
  font-size: 16px;
  color: #333;
}

.login-prompt {
  text-align: center;
  padding: 40px 20px;
}

.login-prompt h2 {
  margin-bottom: 20px;
  color: #333;
}

.login-button {
  background-color: #4caf50;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  margin: 20px 0;
}

.login-button:hover {
  background-color: #45a049;
}

.login-prompt a {
  color: #4caf50;
  text-decoration: none;
}

.login-prompt a:hover {
  text-decoration: underline;
}
</style>
