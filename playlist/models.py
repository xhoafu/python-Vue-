from django.db import models
from django.contrib.auth.models import User
from music.models import Music  # 假设 Music 模型在同一个应用中

class Tag(models.Model):
    """
    标签模型，用于歌单分类
    """
    name = models.CharField(max_length=50, unique=True)  # 标签名称，唯一约束

    def __str__(self):
        return self.name

class Playlist(models.Model):
    """
    歌单模型
    """
    playlist_id = models.AutoField(primary_key=True)  # 歌单唯一标识符（自增主键）
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='playlists')  # 创建歌单的用户（外键）
    name = models.CharField(max_length=255)  # 歌单名称
    description = models.TextField(blank=True, null=True)  # 歌单描述（可选）
    cover_image = models.ImageField(upload_to='playlist_covers/', blank=True, null=True)  # 歌单封面图片
    created_at = models.DateTimeField(auto_now_add=True)  # 歌单创建时间（自动填充）
    updated_at = models.DateTimeField(auto_now=True)  # 歌单最后更新时间（自动填充）
    play_count = models.IntegerField(default=0)  # 歌单播放次数（默认0）
    like_count = models.IntegerField(default=0)  # 歌单点赞数（默认0）
    is_public = models.BooleanField(default=True)  # 歌单是否公开（默认公开）
    tags = models.ManyToManyField(Tag, through='PlaylistTag', related_name='playlists')  # 多对多关系，通过中间表PlaylistTag

    def __str__(self):
        return self.name

class PlaylistSong(models.Model):
    """
    歌单与歌曲的关联表
    """
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, related_name='songs')  # 歌单ID（外键）
    song = models.ForeignKey(Music, on_delete=models.CASCADE, related_name='playlists')  # 歌曲ID（外键）
    order_number = models.IntegerField(blank=True, null=True)  # 歌曲在歌单中的顺序（可选）

    class Meta:
        unique_together = ('playlist', 'song')  # 联合唯一约束，确保同一歌单中不会重复添加同一首歌

    def __str__(self):
        return f"{self.playlist.name} - {self.song.title}"

class PlaylistTag(models.Model):
    """
    歌单与标签的关联表
    """
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)  # 歌单ID（外键）
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)  # 标签ID（外键）

    class Meta:
        unique_together = ('playlist', 'tag')  # 联合唯一约束，确保同一歌单不会重复添加同一标签

    def __str__(self):
        return f"{self.playlist.name} - {self.tag.name}"

class UserPlaylistCollection(models.Model):
    """
    用户收藏歌单表
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='collected_playlists')  # 用户ID（外键）
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, related_name='collectors')  # 歌单ID（外键）
    collected_at = models.DateTimeField(auto_now_add=True)  # 收藏时间（自动填充）

    class Meta:
        unique_together = ('user', 'playlist')  # 联合唯一约束，确保同一用户不会重复收藏同一歌单

    def __str__(self):
        return f"{self.user.username} collected {self.playlist.name}"