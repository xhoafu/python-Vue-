<template>
  <div class="login-container">
    <el-form
      :model="form"
      :rules="rules"
      ref="loginForm"
      label-width="100px"
      class="login-form"
    >
      <h2 class="login-title">登录</h2>
      <el-form-item label="用户名" prop="username">
        <el-input v-model="form.username" placeholder="请输入用户名" />
      </el-form-item>

      <el-form-item label="密码" prop="password">
        <el-input
          v-model="form.password"
          type="password"
          placeholder="请输入密码"
        />
      </el-form-item>

      <el-form-item>
        <el-button type="primary" block @click="handleLogin">登录</el-button>
        <div class="register-link">
          <span>没有账号？</span>
          <router-link to="/register">立即注册</router-link>
        </div>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { ElMessage } from "element-plus";
import { useRouter } from "vue-router";
import { login } from "@/api/login"; // 确保login API是正确定义的

// 表单数据
const form = ref({
  username: "",
  password: "",
});

// 表单规则
const usernameRules = [
  { required: true, message: "请输入用户名", trigger: "blur" },
];
const passwordRules = [
  { required: true, message: "请输入密码", trigger: "blur" },
];

// 引用表单
const loginForm = ref(null); // 用来引用表单

// 路由
const router = useRouter();

// 登录函数
const handleLogin = async () => {
  // 验证表单
  const isValid = await loginForm.value.validate();
  if (!isValid) return; // 如果验证失败，直接返回

  try {
    // 调用登录 API 函数
    const response = await login(form.value);

    const token = response.data.access;
    const refresh = response.data.refresh;

    // 存储 Token 和用户名
    localStorage.setItem("access", token);
    localStorage.setItem("refresh", refresh);
    localStorage.setItem("user_id", response.data.user_id);
    localStorage.setItem("username", form.value.username);
    ElMessage.success("登录成功");

    // 登录成功后跳转到管理页面
    router.push("/");
  } catch (error) {
    // 捕获并处理错误
    ElMessage.error("用户名或密码错误");
    console.error(error);
  }
};
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f5f5f5;
  background-image: url("../../assets/7f88e56754a8aab6d7617a871880b36a.jpg");
  background-size: cover; /* 调整图片大小以覆盖整个容器 */
  background-position: center; /* 居中显示图片 */
  background-repeat: no-repeat;
}

.login-form {
  width: 400px;
  padding: 20px;
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.login-title {
  text-align: center;
  margin-bottom: 20px;
  font-size: 24px;
}

.register-link {
  text-align: center;
  margin-top: 10px;
}

.register-link a {
  color: #409eff;
}
</style>
