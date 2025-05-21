<template>
  <div class="search_box">
    <input
      type="text"
      id="search"
      name="搜索"
      placeholder="搜索音乐、MV、歌单、用户"
      @click="goToSearchPage"
    />
  </div>
</template>

<script setup>
import { useRouter } from "vue-router";
const router = useRouter();

// 点击搜索框时跳转到搜索页面
const goToSearchPage = () => {
  router.push("/search");
};
</script>

<style scoped>
.search_box {
  width: 174px;
  height: 36px;
  margin: auto;
}
.search_box input {
  height: 36px;
  width: 174px;
  border: 1px solid #cccccc;
}
</style>
