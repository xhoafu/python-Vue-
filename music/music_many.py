import csv
import random
import numpy as np

def load_songs_data(csv_file):
    """读取CSV文件并返回结构化歌曲数据"""
    songs = []
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # 处理tags字段
            tags = []
            if row['tags']:
                tags = [tag.strip().lower() for tag in row['tags'].split(',')]

            songs.append({
                'track_id': row['track_id'],
                'name': row['name'],
                'artist': row['artist'],
                'tags': tags,
                'playcount': int(row['playcount']),
                'year': row['year']
            })
    return songs


class SongRecommender:
    def __init__(self, csv_path):
        self.songs = load_songs_data(csv_path)

    def recommend_by_tags(self, input_tags, num=20, random_mode=None):
        """
        根据输入tags推荐歌曲（增强版）
        :param input_tags: 逗号分隔的标签字符串（如 "rap,hip_hop"）
        :param num: 要返回的歌曲数量（默认20）
        :param random_mode: 随机模式选项 [None, 'shuffle', 'weighted']
        :return: 推荐歌曲列表，按策略排序
        """
        search_tags = [t.strip().lower() for t in input_tags.split(',') if t.strip()]

        matched = []
        for song in self.songs:
            if not song['tags']:
                continue
            if any(tag in song['tags'] for tag in search_tags):
                matched.append(song)

        # 随机化处理模块
        if random_mode == 'shuffle':
            # 完全随机采样（无重复）
            return random.sample(matched, min(len(matched), num))
        elif random_mode == 'weighted':
            # 播放量加权随机采样（允许热门歌曲更高概率出现）
            playcounts = [song['playcount'] + 1 for song in matched]  # +1避免0权重
            return random.choices(
                matched,
                weights=playcounts,
                k=min(len(matched), num)
            )
        else:
            # 默认按播放量降序
            matched.sort(key=lambda x: x['playcount'], reverse=True)
            return matched[:num]


# 使用示例
if __name__ == "__main__":
    recommender = SongRecommender(r'D:\学习\Python\Django\MusicApp\数据\track_metadata_df_sub_song_merged4.csv')

    # 示例：推荐包含rap标签的歌曲
    rap_recommendations = recommender.recommend_by_tags('rap')
    print(f"推荐包含rap的歌曲（共{len(rap_recommendations)}首）：")
    print(rap_recommendations)
    for i, song in enumerate(rap_recommendations[:5], 1):
        print(f"{i}. {song['name']} - {song['artist']} [{song['year']}] Tags: {', '.join(song['tags'])}")