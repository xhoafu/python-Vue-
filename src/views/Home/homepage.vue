<template>
  <div class="container">
    <Redplaylist />
    <!-- 轮播图 -->
    <div class="carousel-container">
      <div
        class="carousel"
        @mouseenter="pauseCarousel"
        @mouseleave="startCarousel"
      >
        <div
          class="carousel-item"
          v-for="(item, index) in carouselItems"
          :key="index"
        >
          <img :src="item.image" :alt="item.description" />
        </div>
      </div>
      <button class="prev-btn" @click="prevSlide">❮</button>
      <button class="next-btn" @click="nextSlide">❯</button>
      <div class="carousel-indicators">
        <span
          v-for="(item, index) in carouselItems"
          :key="index"
          class="indicator"
          :class="{ active: currentIndex === index }"
          @click="goToSlide(index)"
        ></span>
      </div>
    </div>

    <div class="header">
      <h2>个性化推荐</h2>
    </div>
    <div class="music-cards">
      <div class="row" v-for="(row, rowIndex) in chunkedSongs" :key="rowIndex">
        <div class="card" v-for="song in row" :key="song.song_id">
          <div class="card-content">
            <h3>{{ song.song_name }}</h3>
            <p>{{ song.artist }}</p>
            <p>{{ song.year }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from "vue";
import instance from "@/utils/request";
import Redplaylist from "./list/redplaylist.vue";

const carouselItems = ref([
  {
    image: require("@/assets/lbt1.jpg"),
    description: "图片1描述",
  },
  {
    image: require("@/assets/34.jpg"),
    description: "图片2描述",
  },
  {
    image: require("@/assets/34.jpg"),
    description: "图片3描述",
  },
]);
const currentIndex = ref(0);
const autoCarousel = ref(null);
const recommendations = ref([]);
const fetchRecommendations = async () => {
  try {
    const username =
      localStorage.getItem("username") ||
      "5a905f000fc1ff3df7ca807d57edb608863db05d";
    const response = await instance.get("music/recommend/", {
      params: { rec_id: username },
    });
    if (response.data && typeof response.data === "object") {
      if (Object.keys(response.data).length === 0) {
        console.error("Response data is empty:", response.data);
        recommendations.value = [];
      } else {
        recommendations.value = Object.values(response.data.data);
      }
    } else {
      console.error("Invalid response format:", response.data);
      recommendations.value = [];
    }

    console.log("Processed recommendations:", recommendations.value);
  } catch (error) {
    console.error("Error fetching recommendations:", error);
    recommendations.value = [];
  }
};
// 轮播图逻辑
const startCarousel = () => {
  autoCarousel.value = setInterval(() => {
    nextSlide();
  }, 5000); // 每5秒切换一次
};

const pauseCarousel = () => {
  clearInterval(autoCarousel.value);
};

const nextSlide = () => {
  currentIndex.value = (currentIndex.value + 1) % carouselItems.value.length;
};

const prevSlide = () => {
  currentIndex.value =
    (currentIndex.value - 1 + carouselItems.value.length) %
    carouselItems.value.length;
};

const goToSlide = (index) => {
  currentIndex.value = index;
};

watch(currentIndex, (newIndex) => {
  const carousel = document.querySelector(".carousel");
  if (carousel) {
    carousel.style.transform = `translateX(-${newIndex * 100}%)`;
  }
});

const chunkedSongs = computed(() => {
  const chunkSize = 5;
  const result = [];
  for (let i = 0; i < recommendations.value.length; i += chunkSize) {
    result.push(recommendations.value.slice(i, i + chunkSize));
  }
  return result;
});

onMounted(() => {
  fetchRecommendations();
  startCarousel();
});
</script>

<style scoped>
.container {
  height: 3000px;
  width: 100%;
  background: linear-gradient(to bottom, #eeeded, #ffffff);
  display: flex;
  flex-direction: column;
  padding: 20px;
  box-sizing: border-box;
}

/* 轮播图样式 */
.carousel-container {
  position: relative;
  left: 5%;
  width: 90%;
  height: 450px;
  overflow: hidden;
  margin-bottom: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.carousel {
  display: flex;
  width: 100%;
  height: 100%;
  transition: transform 0.5s ease;
}

.carousel-item {
  min-width: 100%;
  height: 100%;
}

.carousel-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.prev-btn,
.next-btn {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background-color: rgba(0, 0, 0, 0.5);
  color: white;
  border: none;
  padding: 10px;
  cursor: pointer;
  z-index: 10;
}

.prev-btn {
  left: 10px;
}

.next-btn {
  right: 10px;
}

.carousel-indicators {
  position: absolute;
  bottom: 10px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 10px;
}

.indicator {
  width: 12px;
  height: 12px;
  background-color: rgba(255, 255, 255, 0.5);
  border-radius: 50%;
  cursor: pointer;
}

.indicator.active {
  background-color: white;
}

.header {
  margin-bottom: 20px;
}

.header h2 {
  color: black;
  text-align: center;
  font-size: 24px;
}

.music-cards {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

.card {
  width: 18%;
  background-color: white;
  border-radius: 8px;
  padding: 15px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}

.card:hover {
  transform: translateY(-5px);
}

.card-content h3 {
  margin: 0 0 10px 0;
  font-size: 16px;
  color: #333;
}

.card-content p {
  margin: 5px 0;
  font-size: 14px;
  color: #666;
}
</style>
