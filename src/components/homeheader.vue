<template>
  <div class="headers">
    <div class="box">
      <ul>
        <li>
          <a href="/" :class="{ active: isActive('/') }">首页</a>
        </li>
        <li>
          <a href="/author" :class="{ active: isActive('/author') }">歌手</a>
        </li>
        <li>
          <a href="/playlist" :class="{ active: isActive('/playlist') }"
            >歌单</a
          >
        </li>
        <li>
          <a href="/ranking" :class="{ active: isActive('/ranking') }"
            >排行榜</a
          >
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";

const route = useRoute(); // 获取当前路由

// 判断当前路径是否匹配导航项的路径
const isActive = (path) => {
  // 首页的特殊情况：只有当路径是 '/' 时才高亮
  if (path === "/") {
    return route.path === "/";
  }
  // 其他页面使用正则表达式来匹配路径
  const regex = new RegExp(`^${path.replace(/\//g, "\\/")}`);
  return regex.test(route.path);
};
</script>

<style scoped>
.headers {
  position: relative;
  height: 50px;
  width: 100%;

  padding-top: 0px;
  background-color: #fafbfa;
  display: flex;
}

.box {
  height: 100%;
  width: 60%;
  /* background-color: #8a3f3f; */
  margin: auto;
}

.box ul {
  display: flex;
  list-style: none;
  width: 100%;
  height: 100%;
  margin: 0;
  padding: 0;
}

.box ul li {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
}

.box ul li a {
  color: rgb(12, 12, 12);
  text-decoration: none;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  transition: color 0.3s ease;
}

.box ul li a:hover {
  color: #4dcb6b;
}

.box ul li a.active {
  color: #4dcb6b;
  font-weight: bold;
  border-bottom: 2px solid #4dcb6b;
}

@media (max-width: 768px) {
  .box ul {
    justify-content: space-around;
  }

  .box ul li a {
    font-size: 14px;
    padding: 0 10px;
  }
}
</style>
