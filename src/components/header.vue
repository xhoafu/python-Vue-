<template>
  <div class="headers">
    <div class="headers_corn">
      <div class="image_md" @click="home">
        <img src="../assets/music_logo.png" alt="Logo" class="image" />
      </div>
      <div
        class="music_guan"
        @click="home"
        :class="{
          active:
            isActive('/') ||
            isActive('/playlist') ||
            isActive('/author') ||
            isActive('/ranking'),
        }"
      >
        <h3>音乐馆</h3>
      </div>
      <div
        class="music_guan"
        @click="mine"
        :class="{ active: isActive('/mine') }"
      >
        <h3>我的音乐</h3>
      </div>
      <Topic />
      <div class="login_button">
        <button v-if="!isLoggedIn" @click="login">登录</button>
        <span v-else>{{ userName }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter, useRoute } from "vue-router";
import Topic from "@/components/topic.vue";

const isLoggedIn = ref(false);
const userName = ref("");
const route = useRoute();
const router = useRouter();

// 检查用户是否已登录
const checkLoginStatus = () => {
  const token = localStorage.getItem("access");
  if (token) {
    isLoggedIn.value = true;
    userName.value = localStorage.getItem("username") || "用户名";
  }
  console.log(userName.value);
};

const mine = () => {
  router.push("/mine");
};

const home = () => {
  router.push("/");
};

// 登录函数
const login = () => {
  router.push("/login");
};

const isActive = (path) => {
  // 如果是根路径，直接匹配
  if (path === "/") {
    return route.path === path;
  }
  // 如果是其他路径，检查是否以指定路径开头
  return route.path.startsWith(path);
};

// 页面加载时检查登录状态
onMounted(() => {
  checkLoginStatus();
});
</script>

<style scoped>
.headers {
  height: 90px;
  width: 100%;
  background-color: #fafbfa;
  display: flex;
}
.headers_corn {
  width: 80%;
  height: 90px;
  position: absolute;
  right: 10%;
  background-color: #fff;
  display: flex;
}
.image_md {
  width: 170px;
  height: 100%;
}
.image {
  height: 85px;
  width: 134px;
  margin: auto;
  padding-top: 3px;
}
.music_guan {
  width: 100px;
  height: 100%;
  text-align: center;
  /* padding-top: 12px; */
  /* padding-block: 12px; */
  margin: auto;
  right: 0px;
}

.music_guan:hover {
  background-color: rgb(49, 194, 124); /* 鼠标悬停时背景颜色为深绿色 */
  color: white; /* 鼠标悬停时文字颜色为白色 */
}
.music_guan h3 {
  padding: 12px;
}

.music_guan.active {
  background-color: rgb(49, 194, 124); /* 当前页面的背景颜色 */
}

.login_button {
  height: 90px;
  width: 54px;
  margin: auto;
  display: flex;
  justify-content: center;
  align-items: center;
}

.login_button button {
  height: 100%;
  width: 100%;
  display: flex;
  flex-direction: row;
  /* width: 34px; */
  align-items: center;
  justify-content: center;
  padding: 8px 15px;
  background-color: #fafbfa;
  color: rgb(11, 8, 8);
  border: none;
  border-radius: 4px;
  cursor: pointer;
  max-width: 100%;
  text-align: center;
}

.login_button :hover {
  background-color: rgb(49, 194, 124);
  color: #fff;
}
</style>
