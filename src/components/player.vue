<template>
  <!-- 加载状态 -->
  <div v-if="loading" class="loading-container">
    <div class="loading-spinner"></div>
    <p>正在加载歌曲信息...</p>
  </div>

  <!-- 错误状态 -->
  <div v-else-if="error" class="error-container">
    <h2>加载失败</h2>
    <p>无法获取歌曲信息，请稍后再试</p>
    <button @click="retryLoading">重试</button>
  </div>

  <!-- 内容区域 -->
  <div v-else class="player-container">
    <!-- 背景渐变 -->
    <div class="player-background"></div>

    <!-- 播放器内容 -->
    <div class="player-content">
      <!-- 专辑封面 -->
      <div class="album-cover">
        <img
          :src="songData.image"
          :alt="songData.title"
          class="cover-image"
          @error="handleImageError"
        />
      </div>

      <!-- 歌曲信息 -->
      <div class="song-info">
        <h1 class="song-title">{{ songData.title }}</h1>
        <p class="song-artist">{{ songData.author_name }}</p>
        <p class="song-album">{{ songData.album }}</p>
        <p class="song-year">{{ songData.release_year }}</p>
        <p class="song-genre">{{ songData.genre }}</p>
      </div>

      <!-- 播放控制 -->
      <div class="player-controls">
        <div class="control-buttons">
          <button class="control-button prev-button" @click="prevSong">
            <i class="fas fa-step-backward"></i>
          </button>
          <button
            class="control-button play-button"
            @click="togglePlay"
            :class="{ playing: isPlaying }"
          >
            <div class="button-shape">
              <i :class="['fas', isPlaying ? 'fa-pause' : 'fa-play']"></i>
            </div>
          </button>
          <button class="control-button next-button" @click="nextSong">
            <i class="fas fa-step-forward"></i>
          </button>
        </div>

        <div class="progress-container">
          <div class="progress-bar">
            <div class="progress" :style="{ width: progressWidth }"></div>
          </div>
          <div class="time-display">
            <span class="current-time">{{ formatTime(currentTime) }}</span>
            <span class="duration">{{ formatTime(songData.duration) }}</span>
          </div>
        </div>
      </div>

      <!-- 歌词部分 -->
      <div class="lyrics-container">
        <div class="lyrics-content">
          <!-- 这里可以动态加载歌词 -->
          <p v-if="!lyricsLoaded" class="lyrics-loading">加载歌词中...</p>
          <p v-else-if="lyricsError" class="lyrics-error">无法加载歌词</p>
          <div v-else class="lyrics-lines">
            <p
              v-for="(line, index) in lyrics"
              :key="index"
              :class="{ active: activeLyricIndex === index }"
            >
              {{ line }}
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import { getsong } from "@/api/songs";

const route = useRoute();
const songData = ref(null);
const loading = ref(true);
const error = ref(false);
const isPlaying = ref(false);
const currentTime = ref(0);
const lyrics = ref([]);
const lyricsLoaded = ref(false);
const lyricsError = ref(false);
const activeLyricIndex = ref(0);

// 音频元素
const audio = new Audio();

// 初始化音频
const initAudio = () => {
  if (songData.value && songData.value.audio_file) {
    audio.src = songData.value.audio_file;
    audio.load();

    // 监听音频事件
    audio.addEventListener("timeupdate", updateProgress);
    audio.addEventListener("ended", handleSongEnd);
  }
};

// 获取歌曲数据
const fetchSongData = async () => {
  try {
    const id = route.params.id;
    songData.value = await getsong(id);
    initAudio();
  } catch (err) {
    console.error("加载歌曲信息失败:", err);
    error.value = true;
  } finally {
    loading.value = false;
  }
};

// 重试加载
const retryLoading = () => {
  error.value = false;
  loading.value = true;
  fetchSongData();
};

// 切换播放状态
const togglePlay = () => {
  if (isPlaying.value) {
    audio.pause();
  } else {
    audio.play();
  }
  isPlaying.value = !isPlaying.value;
};

// 上一首歌
const prevSong = () => {
  // 这里可以实现上一首歌的逻辑
  console.log("播放上一首歌");
};

// 下一首歌
const nextSong = () => {
  // 这里可以实现下一首歌的逻辑
  console.log("播放下一首歌");
};

// 更新进度条
const updateProgress = () => {
  currentTime.value = audio.currentTime;
};

// 处理歌曲结束
const handleSongEnd = () => {
  isPlaying.value = false;
};

// 格式化时间
const formatTime = (seconds) => {
  const minutes = Math.floor(seconds / 60);
  const remainingSeconds = Math.floor(seconds % 60);
  return `${minutes}:${remainingSeconds.toString().padStart(2, "0")}`;
};

// 加载歌词
const loadLyrics = async () => {
  try {
    // 这里可以实现歌词加载逻辑
    // 例如从API获取歌词或从文件加载
    lyricsLoaded.value = true;
  } catch (err) {
    console.error("加载歌词失败:", err);
    lyricsError.value = true;
  }
};

// 处理图片加载失败
const handleImageError = (e) => {
  e.target.src = "default-album-cover.jpg"; // 替换为默认专辑封面
};

onMounted(() => {
  fetchSongData();
  loadLyrics();
});
</script>

<style scoped>
/* 基础样式 */
:deep() {
  --primary-color: #1db954;
  --secondary-color: #535353;
  --background: #121212;
  --text-primary: #ffffff;
  --text-secondary: #b3b3b3;
}

body {
  margin: 0;
  font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
  background-color: var(--background);
  color: var(--text-primary);
}

/* 加载状态 */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background: rgba(0, 0, 0, 0.8);
}

.loading-spinner {
  width: 50px;
  height: 50px;
  border: 4px solid var(--secondary-color);
  border-top-color: var(--primary-color);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 20px;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* 错误状态 */
.error-container {
  padding: 40px;
  text-align: center;
  background: #2d2d2d;
  border-radius: 12px;
  max-width: 400px;
  margin: 100px auto;
}

.error-container h2 {
  color: #e74c3c;
  margin-bottom: 16px;
}

.error-container button {
  background: var(--primary-color);
  color: white;
  border: none;
  padding: 12px 30px;
  border-radius: 25px;
  cursor: pointer;
  font-size: 16px;
  transition: transform 0.2s;
}

.error-container button:hover {
  transform: scale(1.05);
}

/* 播放器容器 */
.player-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
}

.player-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(45deg, #2a2a2a 0%, #121212 100%);
  z-index: -1;
}

/* 专辑封面 */
.album-cover {
  max-width: 300px;
  margin: 0 auto 40px;
  position: relative;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.5);
  transition: transform 0.3s;
}

.album-cover:hover {
  transform: scale(1.02);
}

.cover-image {
  width: 100%;
  height: auto;
  display: block;
  aspect-ratio: 1/1;
}

/* 歌曲信息 */
.song-info {
  text-align: center;
  margin-bottom: 40px;
}

.song-title {
  font-size: 2rem;
  margin: 0 0 12px;
  letter-spacing: -0.5px;
}

.song-artist {
  color: var(--primary-color);
  font-size: 1.2rem;
  margin: 0 0 8px;
}

.song-album {
  color: var(--text-secondary);
  margin: 8px 0;
}

/* 播放控制 - 重点修改部分 */
.player-controls {
  max-width: 600px;
  margin: 0 auto;
}

.control-buttons {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 30px;
  margin-bottom: 30px;
}

.control-button {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: var(--text-primary);
  width: 50px;
  height: 50px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* 三角形播放按钮 */
.play-button {
  position: relative;
  width: 80px;
  height: 80px;
  background: rgba(255, 255, 255, 0.1);
  clip-path: polygon(0 0, 100% 50%, 0 100%);
  border: none;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.play-button::before {
  content: "";
  position: absolute;
  inset: 0;
  background: var(--primary-color);
  opacity: 0;
  clip-path: polygon(0 0, 100% 50%, 0 100%);
  transition: opacity 0.3s;
}

.play-button i {
  color: var(--primary-color);
  font-size: 1.8rem;
  transform: translateX(15%);
  transition: all 0.3s;
}

/* 播放状态 */
.play-button.playing {
  clip-path: none;
  border-radius: 12px;
  background: rgba(29, 185, 84, 0.2);
  border: 2px solid var(--primary-color);
}

.play-button.playing::before {
  opacity: 0.1;
}

.play-button.playing i {
  color: #fff;
  transform: none;
  letter-spacing: -3px;
}

/* 悬停效果 */
.play-button:hover {
  transform: scale(1.05);
  filter: drop-shadow(0 0 12px rgba(29, 185, 84, 0.3));
}

.play-button:hover::before {
  opacity: 0.1;
}

/* 进度条 */
.progress-container {
  margin: 20px 0;
}

.progress-bar {
  height: 4px;
  background: var(--secondary-color);
  border-radius: 2px;
  margin: 10px 0;
  cursor: pointer;
}

.progress {
  height: 100%;
  background: var(--primary-color);
  border-radius: 2px;
  transition: width 0.1s linear;
}

.time-display {
  display: flex;
  justify-content: space-between;
  color: var(--text-secondary);
  font-size: 0.9rem;
}

/* 歌词区域 */
.lyrics-container {
  max-width: 600px;
  margin: 40px auto 0;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  padding: 20px;
}

.lyrics-content {
  max-height: 300px;
  overflow-y: auto;
  scroll-behavior: smooth;
}

.lyrics-lines p {
  color: var(--text-secondary);
  margin: 12px 0;
  transition: all 0.3s;
  font-size: 1.1rem;
  line-height: 1.6;
}

.lyrics-lines p.active {
  color: var(--text-primary);
  font-size: 1.3rem;
  font-weight: 500;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .player-container {
    padding: 20px;
  }

  .song-title {
    font-size: 1.8rem;
  }

  .control-buttons {
    gap: 20px;
  }

  .control-button {
    width: 40px;
    height: 40px;
  }

  .play-button {
    width: 60px;
    height: 60px;
  }

  .play-button i {
    font-size: 1.5rem;
  }

  .lyrics-container {
    margin: 20px auto;
  }
}
</style>
