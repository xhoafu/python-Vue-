<template>
  <!-- 加载状态 -->
  <div v-if="!playlist" class="loading">加载中...</div>

  <!-- 内容区域 -->
  <div v-else class="playlist-detail-container">
    <!-- 头部标题 -->
    <div class="header">
      <h2>{{ playlist.name }}</h2>
    </div>

    <!-- 歌单信息区域 -->
    <div class="playlist-header">
      <!-- 左侧封面 -->
      <div class="cover-wrapper">
        <img
          :src="playlist.cover_image"
          :alt="playlist.name"
          class="playlist-cover"
        />
      </div>

      <!-- 右侧信息 -->
      <div class="meta-info">
        <h3 class="title">{{ playlist.name }}</h3>
        <p class="creator">创建者：{{ playlist.user.username }}</p>
        <p class="description">
          描述：{{ playlist.description || "暂无描述" }}
        </p>
        <div class="stats">
          <span>播放：{{ playlist.play_count }}</span>
          <span>点赞：{{ playlist.like_count }}</span>
          <span>歌曲：{{ playlist.songs.length }}首</span>
        </div>
        <div>
          <button @click="addcollect(playlist.playlist_id)">添加收藏</button>
          <button @click="unaddcollect(playlist.playlist_id)">取消收藏</button>
        </div>
      </div>
    </div>

    <!-- 歌曲列表 -->
    <div class="song-list">
      <h3>歌曲列表</h3>
      <table class="song-table">
        <thead>
          <tr class="header-row">
            <th class="index-header">序号</th>
            <th class="song-header">歌曲</th>
            <th class="album-header">专辑</th>
            <th class="release-header">发行年限</th>
            <th class="duration-header">时长</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="(songData, index) in playlist.songs"
            :key="songData.song.id"
            class="song-row"
            @click="goToPlayer(songData.song.id)"
          >
            <td class="index">{{ index + 1 }}</td>
            <td class="song-title">{{ songData.song.title }}</td>
            <td class="album">{{ songData.song.album }}</td>
            <td class="release-year">{{ songData.song.release_year }}</td>
            <td class="duration">
              {{ formatDuration(songData.song.duration) }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import {
  playlistDetail,
  playlistcollet,
  playlistuncollet,
} from "@/api/playlist";

const route = useRoute();
const playlist = ref(null);
const username = localStorage.getItem("username");

const router = useRouter();

// 点击跳转处理
const goToPlayer = (id) => {
  router.push(`/player/${id}`);
};

// 格式化时长
const formatDuration = (seconds) => {
  const minutes = Math.floor(seconds / 60);
  const remainingSeconds = seconds % 60;
  return `${minutes}:${remainingSeconds.toString().padStart(2, "0")}`;
};

const addcollect = async (id) => {
  if (!username) {
    await router.push("/login");
  } else {
    try {
      const result = await playlistcollet(id);
      console.log("收藏成功", result);
      alert("收藏成功！"); // 添加成功提示
    } catch (error) {
      console.error("收藏失败", error);
      alert("收藏失败，请稍后再试。"); // 添加失败提示
    }
  }
};

const unaddcollect = async (id) => {
  if (!username) {
    await router.push("/login");
  } else {
    try {
      const result = await playlistuncollet(id);
      console.log("取消收藏", result);
      alert("取消收藏成功！"); // 添加成功提示
    } catch (error) {
      console.error("取消收藏失败", error);
      alert("取消收藏失败，请稍后再试。"); // 添加失败提示
    }
  }
};

onMounted(async () => {
  try {
    const id = route.params.playlistId;
    const response = await playlistDetail(id);
    playlist.value = response.data;
    console.log(playlist);
  } catch (error) {
    console.error("加载失败:", error);
    // 这里可以添加错误状态处理
  }
});
</script>

<style scoped>
/* 基础样式 */
.playlist-detail-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.loading {
  text-align: center;
  padding: 50px;
  font-size: 18px;
}

/* 头部区域 */
.header {
  text-align: center;
  margin-bottom: 30px;
}

/* 歌单信息布局 */
.playlist-header {
  display: flex;
  gap: 30px;
  margin-bottom: 40px;
}

.cover-wrapper {
  flex: 0 0 300px;
}

.playlist-cover {
  width: 100%;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.meta-info {
  flex: 1;
}

.title {
  margin: 0 0 15px 0;
  font-size: 28px;
}

.creator {
  color: #666;
  margin: 0 0 10px 0;
}

.description {
  color: #444;
  line-height: 1.6;
  margin: 0 0 15px 0;
}

.stats {
  display: flex;
  gap: 20px;
  color: #888;
}

/* 歌曲列表样式 */
.song-list {
  margin-top: 30px;
}

.song-list h3 {
  border-bottom: 1px solid #eee;
  padding-bottom: 10px;
}

/* 表格样式 */
.song-table {
  width: 100%;
  border-collapse: collapse;
}

.header-row {
  background-color: #f5f5f5;
  font-weight: bold;
  /* text-align: left; */
}

.song-row {
  transition: background 0.2s;
}

.song-row:nth-child(odd) {
  background-color: #ffffff; /* 白色背景 */
}

.song-row:nth-child(even) {
  background-color: #f5f5f5; /* 灰色背景 */
}

.song-row:hover {
  background-color: #e9e9e9; /* 悬停时的背景颜色 */
}

.song-table th,
.song-table td {
  padding: 12px 15px;
  border-bottom: 1px solid #eee;
}

.song-table th {
  font-size: 15px;
  color: #555;
}

.song-table td {
  font-size: 14px;
  color: #333;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .playlist-header {
    flex-direction: column;
  }

  .cover-wrapper {
    flex: none;
    max-width: 300px;
    margin: 0 auto;
  }

  .song-table th,
  .song-table td {
    padding: 8px 10px;
    font-size: 13px;
  }
}
</style>
