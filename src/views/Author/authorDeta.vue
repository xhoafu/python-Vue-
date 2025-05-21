<template>
  <!-- 加载状态 -->
  <div v-if="loading" class="loading-container">
    <div class="loading-spinner"></div>
    <p>正在加载歌手信息...</p>
  </div>

  <!-- 错误状态 -->
  <div v-else-if="error" class="error-container">
    <h2>加载失败</h2>
    <p>无法获取歌手信息，请稍后再试</p>
    <button @click="retryLoading">重试</button>
  </div>

  <!-- 内容区域 -->
  <div v-else class="artist-detail-container">
    <!-- 头部信息 -->
    <div class="artist-header">
      <div class="cover-wrapper">
        <img
          :src="artistData.image"
          :alt="artistData.author_name.name"
          class="artist-cover"
          @error="handleImageError"
        />
      </div>
      <div class="basic-info">
        <h1 class="artist-name">{{ artistData.author_name.name }}</h1>
        <div class="meta-info">
          <div class="info-item">
            <span class="label">年龄</span>
            <span class="value">{{ artistData.author_name.age }} 岁</span>
          </div>
        </div>
        <div class="artist-content">
          <h2 class="section-title">歌手简介</h2>
          <p class="bio">
            {{ artistData.author_name.bio || "暂无歌手简介" }}
          </p>
        </div>
      </div>
    </div>

    <!-- 详细信息 -->

    <!-- 歌曲列表 -->
    <div class="music-list">
      <h2 class="section-title">歌手作品</h2>
      <div class="song-table">
        <div class="header-row">
          <div class="index-header">序号</div>
          <div class="title-header">歌名</div>
          <div class="album-header">专辑</div>
        </div>
        <div
          v-for="(music, index) in artistData.musics"
          :key="music.id"
          class="song-row"
          @click="goToPlayer(music.id)"
        >
          <div class="song-index">{{ index + 1 }}</div>
          <div class="song-title">{{ music.title }}</div>
          <div class="song-album">{{ music.album }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { authorDetalist } from "@/api/author";

const route = useRoute();
const router = useRouter();

// 点击跳转处理
const goToPlayer = (id) => {
  router.push(`/player/${id}`);
};
const artistData = ref(null);
const loading = ref(true);
const error = ref(false);

// 格式化时间
const formattedAddTime = computed(() => {
  if (!artistData.value) return "";
  const date = new Date(artistData.value.add_time);
  return date.toLocaleDateString("zh-CN", {
    year: "numeric",
    month: "long",
    day: "numeric",
  });
});

// 图片加载失败处理
const handleImageError = (e) => {
  e.target.src = "@/assets/8.jpg"; // 替换为你的默认图片路径
};

// 重试加载
const retryLoading = async () => {
  error.value = false;
  loading.value = true;
  await loadData();
};

// 加载数据
const loadData = async () => {
  try {
    const id = route.params.id;
    const response = await authorDetalist(id);
    artistData.value = response.data;
    console.log(artistData);
  } catch (err) {
    console.error("加载失败:", err);
    error.value = true;
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  loadData();
});
</script>

<style scoped>
/* 基础样式 */
.artist-detail-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
  background-color: #fff;
  min-height: 100vh;
}

/* 头部区域 */
.artist-header {
  display: flex;
  gap: 40px;
  margin-bottom: 50px;
}

.cover-wrapper {
  flex: 0 0 300px;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

.artist-cover {
  width: 100%;
  height: 400px;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.artist-cover:hover {
  transform: scale(1.05);
}

.basic-info {
  flex: 1;
  padding-top: 20px;
}

.artist-name {
  font-size: 36px;
  margin: 0 0 20px 0;
  color: #333;
}

.meta-info {
  display: flex;
  gap: 30px;
  margin-bottom: 25px;
}

.info-item {
  display: flex;
  flex-direction: column;
}

.label {
  font-size: 14px;
  color: #666;
  margin-bottom: 5px;
}

.value {
  font-size: 18px;
  color: #333;
  font-weight: 500;
}

/* 内容区域 */
.artist-content {
  border-top: 1px solid #eee;
  padding-top: 30px;
}

.section-title {
  font-size: 24px;
  color: #333;
  margin: 0 0 20px 0;
}

.bio {
  line-height: 1.8;
  font-size: 16px;
  color: #444;
  white-space: pre-wrap;
}

/* 歌曲列表 */
.music-list {
  margin-top: 40px;
}

/* 表格样式 */
.song-table {
  width: 100%;
}

.header-row {
  display: flex;
  padding: 12px 0;
  border-bottom: 2px solid #eee;
  font-weight: bold;
  color: #555;
}

.index-header,
.title-header,
.album-header {
  padding: 0 15px;
}

.index-header {
  width: 100px;
}

.title-header {
  flex: 1;
}

.album-header {
  width: 200px;
  text-align: right;
}

.song-row {
  display: flex;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid #eee;
  transition: background-color 0.3s ease;
}

.song-row:nth-child(odd) {
  background-color: #ffffff; /* 白色背景 */
}

.song-row:nth-child(even) {
  background-color: #f5f5f5; /* 灰色背景 */
}

.song-index,
.song-title,
.song-album {
  padding: 0 15px;
}

.song-index {
  width: 100px;
}

.song-title {
  flex: 1;
}

.song-album {
  width: 200px;
  text-align: right;
  color: #666;
}

/* 添加悬停效果 */
.song-row:hover {
  background-color: #e9e9e9; /* 悬停时的背景颜色 */
}

/* 加载状态 */
.loading-container {
  text-align: center;
  padding: 100px 20px;
}

.loading-spinner {
  width: 50px;
  height: 50px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3498db;
  border-radius: 50%;
  margin: 0 auto 20px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

/* 错误状态 */
.error-container {
  text-align: center;
  padding: 100px 20px;
}

.error-container h2 {
  color: #e74c3c;
  margin-bottom: 15px;
}

.error-container button {
  background: #3498db;
  color: white;
  border: none;
  padding: 10px 25px;
  border-radius: 5px;
  cursor: pointer;
  transition: background 0.3s;
}

.error-container button:hover {
  background: #2980b9;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .artist-header {
    flex-direction: column;
  }

  .cover-wrapper {
    flex: none;
    max-width: 300px;
    margin: 0 auto;
  }

  .artist-cover {
    height: auto;
  }

  .artist-name {
    font-size: 28px;
    text-align: center;
  }

  .meta-info {
    flex-direction: column;
    gap: 15px;
    text-align: center;
  }

  .header-row,
  .song-row {
    flex-direction: column;
  }

  .index-header,
  .title-header,
  .album-header,
  .song-index,
  .song-title,
  .song-album {
    width: 100%;
    text-align: left;
    margin-bottom: 5px;
  }
}
</style>
