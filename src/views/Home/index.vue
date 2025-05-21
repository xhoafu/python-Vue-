<template>
  <div class="app-container">
    <HomeHeader />
    <div class="main-content">
      <router-view></router-view>
    </div>
  </div>
</template>

<script setup>
import HomeHeader from "@/components/homeheader.vue";
</script>

<style scoped>
.app-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  min-height: 0;
}

.main-content {
  flex: 1;
  padding: 2px 0px 0px 0px;
  font-size: 16px;
  background-color: #f0f2f5;
  overflow-y: visible; /* 禁用子容器滚动 */
  height: auto;
}
</style>
