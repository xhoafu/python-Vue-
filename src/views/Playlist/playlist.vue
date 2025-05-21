<template>
  <div class="container">
    <div class="header">
      <h2>歌单展示</h2>
    </div>

    <div class="playlist-container">
      <div
        class="row"
        v-for="(row, rowIndex) in chunkedPlaylists"
        :key="rowIndex"
      >
        <div
          class="playlist-card"
          v-for="playlist in row"
          :key="playlist.playlist_id"
        >
          <div class="playlist-image">
            <img
              :src="playlist.cover_image"
              :alt="playlist.name"
              @click="goToPlaylistDetail(playlist.playlist_id)"
            />
          </div>
          <div class="playlist-info">
            <h3>{{ playlist.name }}</h3>
            <p>创建人: {{ playlist.user.username }}</p>
          </div>
        </div>
      </div>
    </div>
    <div class="pagination-controls">
      <button @click="prevPage" :disabled="currentPage === 1">上一页</button>
      <span>第 {{ currentPage }} 页，共 {{ pageData.page_count }} 页</span>
      <button @click="nextPage" :disabled="currentPage === pageData.page_count">
        下一页
      </button>
    </div>
    <div class="box"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { playlist } from "@/api/playlist";
import { useRouter } from "vue-router";

const router = useRouter();
const playlists = ref([]);
const pageData = ref({
  page_count: 0,
  current_page: 1,
  page_size: 0,
  total_items: 0,
});
const currentPage = ref(1);

// 获取歌单数据
const fetchPlaylists = async (page = 1) => {
  try {
    const response = await playlist();
    playlists.value = response.data.results;
    pageData.value = {
      page_count: Math.ceil(response.data.count / 20),
      current_page: page,
      page_size: 20,
      total_items: response.data.count,
    };
  } catch (error) {
    console.error("Error fetching playlists:", error);
  }
};

// 分组歌单数据
const chunkedPlaylists = computed(() => {
  const chunkSize = 5;
  const result = [];
  for (let i = 0; i < playlists.value.length; i += chunkSize) {
    result.push(playlists.value.slice(i, i + chunkSize));
  }
  return result;
});

// 分页控制
const prevPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--;
    fetchPlaylists(currentPage.value);
  }
};

const nextPage = () => {
  if (currentPage.value < pageData.value.page_count) {
    currentPage.value++;
    fetchPlaylists(currentPage.value);
  }
};

// 跳转到歌单详情页面
const goToPlaylistDetail = (playlistId) => {
  router.push({ name: "playlistDetail", params: { playlistId: playlistId } });
};

onMounted(() => {
  fetchPlaylists(currentPage.value);
});
</script>

<style scoped>
.container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  background-color: white;
  min-height: 100vh;
}

.header {
  text-align: center;
  margin-bottom: 20px;
}

.pagination-controls {
  padding-top: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 20px;
  gap: 20px;
}

.pagination-controls button {
  padding: 8px 16px;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.pagination-controls button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.playlist-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.row {
  display: flex;
  justify-content: space-between;
  gap: 20px;
}

.playlist-card {
  width: calc(20% - 16px);
  background-color: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
  cursor: pointer;
}

.playlist-card:hover {
  transform: translateY(-5px);
}

.playlist-image {
  width: 100%;
  height: 150px;
  overflow: hidden;
}

.playlist-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.playlist-info {
  padding: 15px;
}

.playlist-info h3 {
  margin: 0 0 10px 0;
  font-size: 16px;
  color: #333;
}

.playlist-info p {
  margin: 5px 0;
  font-size: 14px;
  color: #666;
}

.box {
  height: 30px;
}
</style>
