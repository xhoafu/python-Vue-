<template>
  <div class="container">
    <div class="register-box">
      <h1>注册</h1>
      <form @submit.prevent="registers">
        <input v-model="form.username" placeholder="用户名" required />
        <input v-model="form.email" type="email" placeholder="邮箱" required />
        <input
          v-model="form.password"
          type="password"
          placeholder="密码"
          required
          autocomplete="new-password"
        />
        <button type="submit">注册</button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
// import axios from "../../api/axios";
import { useRouter } from "vue-router";
import { register } from "@/api/register";

// const username = ref("");
// const email = ref("");
// const password = ref("");
const form = ref({
  username: "",
  email: "",
  password: "",
});
const router = useRouter();
const registers = async () => {
  try {
    const response = await register(form.value);
    const response1 = await alert("注册成功，请登录");
    // 跳转到登录页面
    router.push("/login");
  } catch (error) {
    console.error("注册失败", error);
    alert("注册失败，请检查输入信息");
  }
};
</script>

<style scoped>
.container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f9f9f9;
  background-image: url(../../assets/g.jpg);
  background-size: cover; /* 调整图片大小以覆盖整个容器 */
  background-position: center; /* 居中显示图片 */
  background-repeat: no-repeat;
}

.register-box {
  background-color: white;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  width: 300px;
  text-align: center;
}

h1 {
  font-size: 22px;
  margin-bottom: 20px;
}

form {
  display: flex;
  flex-direction: column;
  align-items: center;
}

input {
  width: 100%;
  padding: 10px;
  margin-bottom: 15px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 16px;
  box-sizing: border-box;
  text-overflow: ellipsis;
}

button {
  width: 100%;
  padding: 10px;
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
  transition: background 0.3s;
}

button:hover {
  background-color: #218838;
}
</style>
