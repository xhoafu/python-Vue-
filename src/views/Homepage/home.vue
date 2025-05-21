<template>
  <div class="app-container">
    <Header />
    <div class="main-content">
      <router-view></router-view>
    </div>
    <Footer />
  </div>
</template>

<script setup>
import Header from "@/components/header.vue";
import Footer from "@/components/footer.vue";
</script>

<style scoped>
.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  overflow: hidden; /* 确保容器不会溢出 */
}

.main-content {
  flex: 1;
  padding: 2px 0px 3px 0px;
  font-size: 16px;
  background-color: #f0f2f5;
  overflow-y: auto; /* 主内容区域可以滚动 */
}
</style>
