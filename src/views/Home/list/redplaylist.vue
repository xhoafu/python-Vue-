/* 按钮禁用样式 */
<template>
  <div class="recommended-playlists">
    <h2>推荐歌单</h2>
    <div class="carousel-wrapper">
      <button
        class="carousel-button prev-button"
        @click="prevSlide"
        :disabled="currentIndex === 0"
      >
        <i class="fas fa-chevron-left"></i>
      </button>
      <div class="carousel-container">
        <div
          class="carousel"
          :style="{ transform: `translateX(-${currentIndex * 100}%)` }"
        >
          <div
            class="carousel-slide"
            v-for="(slide, index) in slides"
            :key="index"
          >
            <div class="playlist-grid">
              <div
                v-for="playlist in slide"
                :key="playlist.playlist_id"
                class="playlist-card"
                @click="goToPlaylistDetail(playlist.playlist_id)"
              >
                <img
                  :src="playlist.cover_image"
                  :alt="playlist.name"
                  class="playlist-cover"
                />
                <h3>{{ playlist.name }}</h3>
                <p>{{ playlist.description }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
      <button
        class="carousel-button next-button"
        @click="nextSlide"
        :disabled="currentIndex === slides.length - 1"
      >
        <i class="fas fa-chevron-right"></i>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { playlistrecommended } from "@/api/playlist";
import { useRouter } from "vue-router";

const router = useRouter();
const playlists = ref([]);
const currentIndex = ref(0);

// 将歌单分成每组5个
const slides = computed(() => {
  const chunkSize = 5;
  const result = [];
  for (let i = 0; i < playlists.value.length; i += chunkSize) {
    result.push(playlists.value.slice(i, i + chunkSize));
  }
  return result;
});

const goToPlaylistDetail = (playlistId) => {
  router.push({ name: "playlistDetail", params: { playlistId: playlistId } });
};

// 获取推荐歌单
const fetchRecommendedPlaylists = async () => {
  try {
    const response = await playlistrecommended();
    playlists.value = response.data;
  } catch (err) {
    console.error("获取推荐歌单失败:", err);
  }
};

const prevSlide = () =>
  (currentIndex.value = Math.max(0, currentIndex.value - 1));
const nextSlide = () =>
  (currentIndex.value = Math.min(
    slides.value.length - 1,
    currentIndex.value + 1
  ));

onMounted(fetchRecommendedPlaylists);
</script>

<style scoped>
.recommended-playlists {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
}

.carousel-wrapper {
  position: relative;
  display: flex;
  align-items: center;
  gap: 20px;
}

.carousel-container {
  flex: 1;
  overflow: hidden;
}

.carousel {
  display: flex;
  transition: transform 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}

.carousel-slide {
  flex: 0 0 100%;
  min-width: 0;
}

.playlist-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 20px;
  padding: 0 10px;
}

/* 按钮禁用样式 */
.carousel-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.playlist-card {
  background-color: #fff;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.playlist-card:hover {
  transform: translateY(-5px);
}

.playlist-cover {
  width: 100%;
  height: 180px;
  object-fit: cover;
}

.playlist-card h3 {
  margin: 15px 0 10px;
  font-size: 18px;
}

.playlist-card p {
  margin: 0 15px 15px;
  color: #666;
  font-size: 14px;
  flex-grow: 1;
}

.carousel-button {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background-color: rgba(255, 255, 255, 0.5);
  border: none;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.3s;
  z-index: 10;
}

.carousel-button:hover {
  background-color: rgba(255, 255, 255, 0.8);
}

.prev-button {
  left: 10px;
}

.next-button {
  right: 10px;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .playlist-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}

@media (max-width: 992px) {
  .playlist-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 768px) {
  .playlist-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 576px) {
  .playlist-grid {
    grid-template-columns: repeat(1, 1fr);
  }
}
</style>
