<template>
  <div class="music-container">
    <nav class="music-nav">
      <h1>🎵 Music Hub</h1>
      <div class="nav-links">
        <a href="#hot">热门推荐</a>
        <a href="#charts">榜单</a>
        <a href="#genres">分类</a>
      </div>
    </nav>

    <section class="hot-recommend" id="hot">
      <h2>🔥 本周热门推荐</h2>
      <div class="music-grid">
        <div class="music-card" v-for="song in hotSongs" :key="song.title">
          <img :src="song.cover" class="album-cover" alt="专辑封面" />
          <div class="song-info">
            <h3>{{ song.title }}</h3>
            <p class="artist">{{ song.artist }}</p>
            <p class="description">{{ song.description }}</p>
            <div class="rating">
              <span
                v-for="n in 5"
                :key="n"
                :class="['star', n <= song.rating ? 'filled' : '']"
                >★</span
              >
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="charts" id="charts">
      <h2>📊 热门榜单</h2>
      <div class="chart-list">
        <div
          class="chart-item"
          v-for="(chart, index) in charts"
          :key="chart.name"
        >
          <div class="chart-rank">{{ index + 1 }}</div>
          <img :src="chart.cover" class="chart-cover" alt="榜单封面" />
          <div class="chart-info">
            <h3>{{ chart.name }}</h3>
            <p>{{ chart.artist }}</p>
            <span class="chart-tag">{{ chart.genre }}</span>
          </div>
        </div>
      </div>
    </section>

    <section class="genres" id="genres">
      <h2>🎧 音乐风格</h2>
      <div class="genre-grid">
        <div class="genre-card" v-for="genre in genres" :key="genre.name">
          <div class="genre-icon" :style="{ backgroundColor: genre.color }">
            {{ genre.emoji }}
          </div>
          <h3>{{ genre.name }}</h3>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
// 模拟数据
const hotSongs = [
  {
    title: "Summer Vibes",
    artist: "Ocean Waves",
    cover: "https://picsum.photos/150/150?random=1",
    description: "充满夏日气息的电子流行曲",
    rating: 4,
  },
  {
    title: "Midnight City",
    artist: "The Starlights",
    cover: "https://picsum.photos/150/150?random=2",
    description: "梦幻合成器流行乐",
    rating: 5,
  },
  {
    title: "Urban Jungle",
    artist: "City Beats",
    cover: "https://picsum.photos/150/150?random=3",
    description: "充满律动的都市节奏",
    rating: 4,
  },
];

const charts = [
  {
    name: "流行巅峰榜",
    artist: "Various Artists",
    genre: "流行",
    cover: "https://picsum.photos/80/80?random=4",
  },
  {
    name: "独立之声",
    artist: "Indie Collective",
    genre: "独立",
    cover: "https://picsum.photos/80/80?random=5",
  },
  {
    name: "电子风暴",
    artist: "EDM Nation",
    genre: "电子",
    cover: "https://picsum.photos/80/80?random=6",
  },
];

const genres = [
  { name: "流行", emoji: "🎤", color: "#FF6B6B" },
  { name: "摇滚", emoji: "🎸", color: "#4ECDC4" },
  { name: "电子", emoji: "🎧", color: "#45B7D1" },
  { name: "爵士", emoji: "🎷", color: "#96CEB4" },
  { name: "古典", emoji: "🎻", color: "#FFEEAD" },
  { name: "嘻哈", emoji: "🎤", color: "#D4A5A5" },
];
</script>

<style scoped>
.music-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  background-color: #1a1a1a;
  color: white;
  min-height: 100vh;
}

.music-nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 0;
  border-bottom: 1px solid #333;
}

.nav-links a {
  color: white;
  text-decoration: none;
  margin-left: 30px;
  transition: color 0.3s;
}

.nav-links a:hover {
  color: #4ecdc4;
}

.music-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.music-card {
  background: #2a2a2a;
  border-radius: 10px;
  padding: 15px;
  display: flex;
  transition: transform 0.3s;
}

.music-card:hover {
  transform: translateY(-5px);
}

.album-cover {
  width: 100px;
  height: 100px;
  border-radius: 8px;
  margin-right: 15px;
}

.song-info h3 {
  margin: 0 0 5px 0;
  color: #4ecdc4;
}

.artist {
  color: #888;
  font-size: 0.9em;
  margin: 0 0 10px 0;
}

.description {
  font-size: 0.9em;
  line-height: 1.4;
  margin-bottom: 10px;
}

.rating .star {
  color: #666;
}

.rating .filled {
  color: #ffd700;
}

.chart-list {
  background: #2a2a2a;
  border-radius: 10px;
  padding: 20px;
}

.chart-item {
  display: flex;
  align-items: center;
  padding: 15px 0;
  border-bottom: 1px solid #333;
}

.chart-item:last-child {
  border-bottom: none;
}

.chart-rank {
  font-size: 1.5em;
  width: 50px;
  text-align: center;
}

.chart-cover {
  width: 60px;
  height: 60px;
  border-radius: 8px;
  margin-right: 15px;
}

.chart-tag {
  background: #4ecdc4;
  color: white;
  padding: 3px 8px;
  border-radius: 4px;
  font-size: 0.8em;
}

.genre-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.genre-card {
  background: #2a2a2a;
  padding: 20px;
  border-radius: 10px;
  text-align: center;
  transition: transform 0.3s;
}

.genre-card:hover {
  transform: scale(1.05);
}

.genre-icon {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  margin: 0 auto 15px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2em;
}

h2 {
  padding-left: 10px;
  border-left: 4px solid #4ecdc4;
  margin: 40px 0 30px;
}
</style>
