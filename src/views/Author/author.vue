<template>
  <div class="home-container">
    <div class="header">
      <!-- <img src="../../assets/music_man.png" alt="Music Man" /> -->
      <h2>推荐歌手</h2>
    </div>
    <div class="container">
      <div
        class="row"
        v-for="(row, rowIndex) in chunkedArtists"
        :key="rowIndex"
      >
        <div
          class="artist-card"
          v-for="artist in row"
          :key="artist.id"
          @click="goToAuthorDetail(artist.author)"
        >
          <img
            :src="artist.image"
            :alt="artist.author_name.name"
            class="artist-image"
          />
          <p class="artist-name">{{ artist.author_name.name }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();

// 点击跳转处理
const goToAuthorDetail = (authorId) => {
  router.push(`/author/${authorId}`);
};

// 歌手数据

const artists = [
  {
    id: 4,
    author_name: {
      name: "方大同",
      age: "41",
      bio: "一位知名的香港男歌手",
      id: 4,
    },
    image: "http://127.0.0.1:8000/media/author_images/image1_2AgZW4G.jpg",
    add_time: "2024-12-01T16:25:43.532740+08:00",
    author: 4,
  },
  {
    id: 5,
    author_name: {
      name: "周杰伦",
      age: "45",
      bio: "周杰伦是中国台湾的流行乐男歌手、音乐人",
      id: 5,
    },
    image: "http://127.0.0.1:8000/media/author_images/image7_o9wbOQ1.jpg",
    add_time: "2024-12-01T16:26:54.217635+08:00",
    author: 5,
  },
  {
    id: 6,
    author_name: {
      name: "方大同",
      age: "41",
      bio: "一位知名的香港男歌手",
      id: 4,
    },
    image: "http://127.0.0.1:8000/media/author_images/image2_rFa2UTJ.jpg",
    add_time: "2024-12-01T16:27:14.847628+08:00",
    author: 4,
  },
  {
    id: 2,
    author_name: {
      name: "李荣浩",
      age: "36",
      bio: null,
      id: 2,
    },
    image: "http://127.0.0.1:8000/media/author_images/image5_Y4j7cad.jpg",
    add_time: "2024-12-01T15:08:50.273800+08:00",
    author: 2,
  },
  {
    id: 3,
    author_name: {
      name: "李健",
      age: "45",
      bio: null,
      id: 3,
    },
    image: "http://127.0.0.1:8000/media/author_images/image6_4B72jnX.jpg",
    add_time: "2024-12-01T15:42:36.703830+08:00",
    author: 3,
  },
  {
    id: 8,
    author_name: {
      name: "林俊杰",
      age: "44",
      bio: "2003年，林俊杰发行首张创作专辑《乐行者》。2004年凭专辑《第二天堂》中的《江南》一曲成名。2013年至2015年举办“时线Timeline世界巡回演唱会”和安可场“时线：新地球世界巡回演唱会”，唱遍4大洲、31个城市，刷新个人纪录。2014年以专辑《因你而在》夺得第25届台湾金曲奖最佳国语男歌手奖。2016年凭借专辑《和自己对话》获得第27届台湾金曲奖最佳国语男歌手奖，并推出个人首部音乐纪录片《听·见林俊杰》。截止到2019年，已发行13张正式专辑，累计创作数百首歌曲。",
      id: 9,
    },
    image: "http://127.0.0.1:8000/media/author_images/lijj.png",
    add_time: "2025-04-13T21:07:14.766919+08:00",
    author: 9,
  },
  {
    id: 9,
    author_name: {
      name: "陶喆",
      age: "57",
      bio: "1969年7月11日出生于中国香港，毕业于加利福尼亚大学洛杉矶分校，是华语流行乐男歌手、音乐制作人、词曲创作人，被誉为中国台湾流行乐坛的“R&B教父”。",
      id: 12,
    },
    image: "http://127.0.0.1:8000/media/author_images/tz.png",
    add_time: "2025-04-13T21:09:01.130673+08:00",
    author: 12,
  },
  {
    id: 10,
    author_name: {
      name: "陈奕迅",
      age: "49",
      bio: "陈奕迅1995年因获得第14届新秀歌唱大赛冠军而出道，1996年发行首张专辑《陈奕迅》。他以独特的嗓音和深情的演唱风格闻名，音乐风格涵盖流行、摇滚、民谣等多种类型。他的代表作品包括《K歌之王》、《十年》、《浮夸》、《富士山下》、《孤勇者》等。他曾多次获得台湾金曲奖最佳国语男歌手奖，并被誉为香港乐坛的代表性人物之一。除了音乐事业，陈奕迅还涉足影视领域，主演过多部电影和电视剧，如《旺角大家姐》、《金钱帝国》等。他积极参与公益活动，多次为慈善机构筹款，并担任联合国儿童基金会亲善大使。",
      id: 10,
    },
    image: "http://127.0.0.1:8000/media/author_images/cyx.png",
    add_time: "2025-04-13T21:10:45.212135+08:00",
    author: 10,
  },
  {
    id: 11,
    author_name: {
      name: "薛之谦",
      age: "41",
      bio: "1983年7月17日出生于上海市，毕业于格里昂酒店管理学院，是中国内地流行乐男歌手、音乐制作人、影视演员。",
      id: 11,
    },
    image: "http://127.0.0.1:8000/media/author_images/xzq.png",
    add_time: "2025-04-13T21:11:46.564759+08:00",
    author: 11,
  },
  {
    id: 12,
    author_name: {
      name: "许嵩",
      age: "39",
      bio: "中国内地流行乐男歌手、词曲创作人、音乐制作人，毕业于安徽医科大学。2009年，许嵩发行首张词曲全创作专辑《自定义》，从而正式出道。",
      id: 13,
    },
    image: "http://127.0.0.1:8000/media/author_images/xs.png",
    add_time: "2025-04-13T21:12:56.119427+08:00",
    author: 13,
  },
];

// 将数组分块（每行5个）
const chunkedArtists = computed(() => {
  const chunkSize = 5;
  return Array.from(
    { length: Math.ceil(artists.length / chunkSize) },
    (_, index) => artists.slice(index * chunkSize, (index + 1) * chunkSize)
  );
});
</script>

<style scoped>
.home-container {
  min-height: 100vh;
  background-color: #f5f5f5;
}

.header {
  height: 150px;
  background: white;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 30px;
}

.header img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
  gap: 2%; /* 添加间距 */
}

.artist-card {
  width: 18%;
  background: white;
  border-radius: 8px;
  overflow: hidden;
  transition: all 0.3s ease;
  cursor: pointer;
}

.artist-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.artist-image {
  width: 100%;
  height: 180px;
  object-fit: cover;
  border-bottom: 1px solid #eee;
}

.artist-name {
  padding: 12px;
  font-size: 14px;
  font-weight: 600;
  color: #333;
  text-align: center;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* 响应式设计 */
@media (max-width: 992px) {
  .row {
    flex-wrap: wrap;
    justify-content: flex-start;
    gap: 3%;
  }

  .artist-card {
    width: 30%;
    margin-bottom: 20px;
  }
}

@media (max-width: 576px) {
  .artist-card {
    width: 48%;
  }

  .header {
    height: 250px;
  }

  .artist-image {
    height: 150px;
  }
}
</style>
