from rest_framework import serializers
from .models import Playlist, PlaylistSong, PlaylistTag, Tag, UserPlaylistCollection
from music.models import Music  # 假设 Music 模型在另一个应用中
from django.contrib.auth.models import User

class TagSerializer(serializers.ModelSerializer):
    """
    标签序列化器
    """
    class Meta:
        model = Tag
        fields = '__all__'

class MusicSerializer(serializers.ModelSerializer):
    """
    歌曲序列化器
    """
    class Meta:
        model = Music
        fields = '__all__'

class PlaylistSongSerializer(serializers.ModelSerializer):
    """
    歌单与歌曲关联序列化器
    """
    song = MusicSerializer()  # 嵌套歌曲序列化器

    class Meta:
        model = PlaylistSong
        fields = ['song', 'order_number']

class UserSerializer(serializers.ModelSerializer):
    """
    用户序列化器（简化版）
    """
    class Meta:
        model = User
        fields = ['id', 'username']

class UserPlaylistCollectionSerializer(serializers.ModelSerializer):
    """
    用户收藏歌单序列化器
    """
    user = UserSerializer()
    playlist = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = UserPlaylistCollection
        fields = ['user', 'playlist', 'collected_at']

class PlaylistTagSerializer(serializers.ModelSerializer):
    """
    歌单与标签关联序列化器
    """
    tag = TagSerializer()  # 嵌套标签序列化器

    class Meta:
        model = PlaylistTag
        fields = ['tag']

    def create(self, validated_data):
        tag_data = validated_data.pop('tag')
        tag, _ = Tag.objects.get_or_create(name=tag_data['name'])
        playlist_tag = PlaylistTag.objects.create(tag=tag, **validated_data)
        return playlist_tag

    def update(self, instance, validated_data):
        tag_data = validated_data.pop('tag')
        tag, _ = Tag.objects.get_or_create(name=tag_data['name'])
        instance.tag = tag
        instance.save()
        return instance

class PlaylistSerializer(serializers.ModelSerializer):
    """
    歌单序列化器
    """
    user = UserSerializer()  # 嵌套用户序列化器
    songs = PlaylistSongSerializer(many=True)  # 嵌套歌单与歌曲关联序列化器
    tags = PlaylistTagSerializer(many=True, source='playlisttag_set')  # 嵌套歌单与标签关联序列化器
    collectors = UserPlaylistCollectionSerializer(many=True, read_only=True)  # 嵌套用户收藏序列化器

    class Meta:
        model = Playlist
        fields = [
            'playlist_id', 'user', 'name', 'description', 'cover_image',
            'created_at', 'updated_at', 'play_count', 'like_count',
            'is_public', 'songs', 'tags', 'collectors'
        ]

    def create(self, validated_data):
        # 处理嵌套数据的创建
        user_data = validated_data.pop('user')
        songs_data = validated_data.pop('songs', [])
        tags_data = validated_data.pop('tags', [])

        # 创建用户（如果需要，这里假设用户已经存在）
        user, _ = User.objects.get_or_create(username=user_data['username'])

        # 创建歌单
        playlist = Playlist.objects.create(user=user, **validated_data)

        # 创建歌曲关联
        for song_data in songs_data:
            song = Music.objects.get(id=song_data['song']['id'])
            PlaylistSong.objects.create(playlist=playlist, song=song, order_number=song_data['order_number'])

        # 创建标签关联
        for tag_data in tags_data:
            tag, _ = Tag.objects.get_or_create(name=tag_data['tag']['name'])
            PlaylistTag.objects.create(playlist=playlist, tag=tag)

        return playlist

    def update(self, instance, validated_data):
        # 处理嵌套数据的更新
        user_data = validated_data.pop('user', None)
        songs_data = validated_data.pop('songs', [])
        tags_data = validated_data.pop('tags', [])

        # 更新用户信息（如果需要）
        if user_data:
            instance.user.username = user_data['username']
            instance.user.save()

        # 更新歌单基本信息
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.cover_image = validated_data.get('cover_image', instance.cover_image)
        instance.is_public = validated_data.get('is_public', instance.is_public)
        instance.save()

        # 更新歌曲关联
        if songs_data:
            # 删除现有关联
            instance.songs.all().delete()
            for song_data in songs_data:
                song = Music.objects.get(id=song_data['song']['id'])
                PlaylistSong.objects.create(playlist=instance, song=song, order_number=song_data['order_number'])

        # 更新标签关联
        if tags_data:
            # 删除现有关联
            instance.playlisttag_set.all().delete()
            for tag_data in tags_data:
                tag, _ = Tag.objects.get_or_create(name=tag_data['tag']['name'])
                PlaylistTag.objects.create(playlist=instance, tag=tag)

        return instance