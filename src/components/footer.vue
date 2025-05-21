<template>
  <div :class="{ 'footer-visible': isVisible }" class="footer">
    <p>音乐如诗，声声入心</p>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from "vue";

const isVisible = ref(true); // 初始状态为显示
const lastScrollPosition = ref(0);

const handleScroll = () => {
  const currentScrollPosition =
    window.scrollY || document.documentElement.scrollTop;

  // 优先检查是否接近底部
  const windowHeight = window.innerHeight;
  const documentHeight = document.documentElement.scrollHeight;
  const distanceFromBottom =
    documentHeight - (currentScrollPosition + windowHeight);

  // 如果距离底部小于 100px，强制显示底部栏
  if (distanceFromBottom < 100) {
    isVisible.value = true;
    return; // 直接结束函数，不执行后续方向判断
  }

  // 判断滚动方向（容差 5px 避免微小抖动）
  if (Math.abs(currentScrollPosition - lastScrollPosition.value) < 5) return;

  // 向下滚动显示，向上滚动隐藏
  isVisible.value = currentScrollPosition > lastScrollPosition.value;

  // 更新上次滚动位置（需要放在方向判断之后）
  lastScrollPosition.value = currentScrollPosition;
};

onMounted(() => {
  window.addEventListener("scroll", handleScroll);
});

onUnmounted(() => {
  window.removeEventListener("scroll", handleScroll);
});
</script>

<style scoped>
/* 保持原有样式不变 */
.footer {
  position: fixed;
  bottom: -60px;
  left: 0;
  width: 100%;
  height: 60px;
  background-color: rgb(51, 51, 51);
  display: flex;
  justify-content: center;
  align-items: center;
  box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.1);
  transition: bottom 0.3s ease;
  z-index: 100;
}

.footer-visible {
  bottom: 0;
}

.footer p {
  color: #ffffff;
  font-size: 16px;
  font-weight: 300;
  letter-spacing: 1px;
  text-align: center;
}
</style>
