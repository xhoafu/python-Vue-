import pickle
import random
import csv
import math
from operator import itemgetter


class ItemBasedCF():
    # 初始化参数
    def __init__(self):
        # 选择相似的 20 首音乐，推荐 10 首
        self.n_sim_music = 20
        self.n_rec_music = 10

        # 训练集和测试集
        self.trainSet = {}
        self.testSet = {}

        # 物品相似度矩阵
        self.music_sim_matrix = {}
        self.music_popular = {}
        self.music_count = 0

        # 推荐的歌曲
        self.music_massage = {}

        # print("相似歌曲个数: %d" % self.n_sim_music)
        # print("推荐歌曲个数: %d" % self.n_rec_music)

    # 读取 CSV 数据并划分训练集和测试集
    def get_dataset(self, filename, pivot=0.75):
        trainSet_len = 0
        testSet_len = 0

        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)  # 使用 csv 读取文件
            next(reader)  # 跳过表头（如果有）

            for line in reader:
                if len(line) < 4:
                    print(f"Warning: 跳过格式错误的行 -> {line}")
                    continue

                track_id, user_id, playcount, name = line[:4]  # 只取前 4 列
                try:
                    playcount = float(playcount)  # 转换播放次数为 float
                except ValueError:
                    print(f"Skipping invalid playcount: '{playcount}' for user '{user_id}' and song '{track_id}'")
                    continue

                # 按 pivot 划分数据集
                if random.random() < pivot:
                    self.trainSet.setdefault(user_id, {})
                    self.trainSet[user_id][track_id] = playcount
                    trainSet_len += 1
                else:
                    self.testSet.setdefault(user_id, {})
                    self.testSet[user_id][track_id] = playcount
                    testSet_len += 1

        print("✅ 成功分隔训练集和测试集")
        print("训练集大小：%s" % trainSet_len)
        print("测试集大小：%s" % testSet_len)

    def calcu_music_sim(self):
        """
        计算歌曲的相似度矩阵（基于听歌次数的共现矩阵）
        """
        # 统计每首歌曲被多少用户听过
        for user, musics in self.trainSet.items():
            for music in musics:
                if music not in self.music_popular:
                    self.music_popular[music] = 0
                self.music_popular[music] += 1  # 统计歌曲被多少用户听过

        self.music_count = len(self.music_popular)
        print("🎵 被听过的歌曲总数：%d" % self.music_count)

        # 遍历训练数据，构建共现矩阵
        for user, musics in self.trainSet.items():
            for m1 in musics:
                for m2 in musics:
                    if m1 == m2:  # 同一首歌曲，跳过
                        continue
                    self.music_sim_matrix.setdefault(m1, {})
                    self.music_sim_matrix[m1].setdefault(m2, 0)
                    self.music_sim_matrix[m1][m2] += 1  # 统计歌曲 m1 和 m2 被同一用户听过的次数

        print("✅ 歌曲共现矩阵构建成功！")

        for m1, related_musics in self.music_sim_matrix.items():
            for m2, count in related_musics.items():
                # 考虑当两首歌曲都未被点评过的情况，相似度直接设置为0
                if self.music_popular.get(m1, 0) == 0 or self.music_popular.get(m2, 0) == 0:
                    self.music_sim_matrix[m1][m2] = 0
                else:
                    # 计算余弦相似度
                    self.music_sim_matrix[m1][m2] = count / math.sqrt(self.music_popular[m1] * self.music_popular[m2])

        print("✅ 成功计算相似度矩阵")

    def save(self):

        with open('保存文件/movie_sim_matrix.pkl', 'wb') as f:
            pickle.dump(itemCF.music_sim_matrix, f)  # 保存相似度矩阵

        with open('保存文件/trainSet.pkl', 'wb') as f:
            pickle.dump(itemCF.trainSet, f)  # 保存训练集数据

        with open('保存文件/testSet.pkl', 'wb') as f:
            pickle.dump(itemCF.testSet, f)  # 保存测试集数据

    def writ(self):

        # 加载相似度矩阵和训练数据
        with open(r'D:\学习\Python\Django\MusicApp\数据\movie_sim_matrix.pkl', 'rb') as f:
            self.music_sim_matrix = pickle.load(f)

        with open(r'D:\学习\Python\Django\MusicApp\数据\trainSet.pkl', 'rb') as f:
            self.trainSet = pickle.load(f)

        # with open(r'D:\学习\Python\机器学习练习\itemcf\练习保存文件\testSet.pkl', 'rb') as f:
        #     itemCF.testSet = pickle.load(f)

    """根据歌曲 ID 获取歌曲详细信息"""
    def get_song_info_by_id(self, top_n, song_info):
        for song_id, score in top_n:
            if song_id in song_info:
                self.music_massage[song_id] = song_info[song_id]
        return self.music_massage

    """给定用户，基于物品相似度矩阵推荐歌曲"""
    def recommend(self, user):

        n = self.n_rec_music  # 推荐的歌曲数
        k = self.n_sim_music  # 选取的相似歌曲数
        rank = {}  # 存储推荐结果

        # 获取用户听过的歌曲（避免 KeyError）
        listened_musics = self.trainSet.get(user, {})

        # 获取全局最大播放次数，进行归一化
        max_playcount = max(playcount for user in self.trainSet.values() for playcount in user.values())

        for music, playcount in listened_musics.items():
            # 确保当前歌曲在相似度矩阵中
            if music in self.music_sim_matrix:
                # 获取与当前歌曲最相似的 k 首歌曲
                similar_items = sorted(self.music_sim_matrix[music].items(), key=itemgetter(1), reverse=True)[:k]

                for related_music, w in similar_items:
                    if related_music in listened_musics:
                        continue  # 如果用户已经听过该歌曲，则跳过

                    # 归一化播放次数，防止过大影响
                    norm_playcount = float(playcount) / max_playcount  # 归一化到 0-1

                    rank.setdefault(related_music, 0)
                    rank[related_music] += w * norm_playcount  # 推荐分数 = 相似度 * 归一化播放次数

        # 排序推荐歌曲，获取前 `n` 首推荐，以及 `n:k` 作为候选推荐
        sorted_rank = sorted(rank.items(), key=itemgetter(1), reverse=True)

        top_n = sorted_rank[:n]  # 最高评分的 n 首推荐
        next_k_n = sorted_rank[n:k]  # n 之后到 k 的推荐

        """对推荐的歌的信息获取"""
        file = r'D:\学习\Python\Django\MusicApp\数据\track_metadata_df_sub_song_merged.csv'
        song_info = self.load_song_info(file)

        song_details = self.get_song_info_by_id(top_n, song_info)
        # if song_details:
        #         print(
        #             f"歌曲 ID: {song_id}, 歌曲名: {song_details['song_name']}, 艺术家: {song_details['artist']}, 推荐分数: {score}")
        # else:
        #         print(f"歌曲 ID: {song_id} 未找到相关信息")

        # print("🎶 推荐给用户的前 {} 首歌曲:".format(n), top_n)
        # print("📌 备选推荐 {} 到 {} 的歌曲:".format(n, k), next_k_n)
        # print(song_details)

        return top_n, next_k_n,song_details  # 返回推荐结果

    """加载歌曲信息"""
    def load_song_info(self, filename):
        song_info = {}
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader)  # 跳过表头a
                for line in reader:
                    # print(f"Processing line: {line}")  # 打印每行数据
                    if len(line) < 3:
                        print(f"Skipping line with too few columns: {line}")
                        continue  # 跳过列数少于3的行
                    # 提取所有列
                    song_id, user_id, playcount, song_mane, artist, year  = line  # 使用 * 语法提取剩余列
                    song_info[song_id] = {
                        'song_id': song_id,
                        'song_name': song_mane,
                        'artist': artist,
                        'year': year # 存储其他列数据
                    }
            # print("File reading completed!")
        except Exception as e:
            print(f"Error loading song info: {e}")
        return song_info


# if __name__ == '__main__':
    # rating_file = r'D:\学习\Python\机器学习练习\itemcf\music_itemcf\history,music_cf\运行后数据\track_metadata_df_sub_song_merged.csv'
    # itemCF = ItemBasedCF()
    # itemCF.writ()
    # itemCF.recommend('6a8a142084a4818c0dcac48bdfb3c39deacf5168')
    # itemCF.get_dataset(rating_file)
    # itemCF.calcu_music_sim()
    # itemCF.save()
