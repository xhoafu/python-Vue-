from django.contrib import admin
from .models import Playlist, PlaylistSong, PlaylistTag, Tag, UserPlaylistCollection
from music.models import Music  # 假设 Music 模型在另一个应用中
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

# 注册 Tag 模型
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# 注册 Playlist 模型
class PlaylistSongInline(admin.TabularInline):
    model = PlaylistSong
    extra = 1
    verbose_name = "歌曲"
    verbose_name_plural = "歌曲列表"

class PlaylistTagInline(admin.TabularInline):
    model = PlaylistTag
    extra = 1
    verbose_name = "标签"
    verbose_name_plural = "标签列表"

@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'created_at', 'is_public')
    list_filter = ('is_public', 'created_at')
    search_fields = ('name', 'description', 'user__username')
    date_hierarchy = 'created_at'
    inlines = [PlaylistSongInline, PlaylistTagInline]

# 注册 PlaylistSong 模型
@admin.register(PlaylistSong)
class PlaylistSongAdmin(admin.ModelAdmin):
    list_display = ('playlist', 'song', 'order_number')
    list_filter = ('playlist',)
    search_fields = ('playlist__name', 'song__title')

# 注册 PlaylistTag 模型
@admin.register(PlaylistTag)
class PlaylistTagAdmin(admin.ModelAdmin):
    list_display = ('playlist', 'tag')
    list_filter = ('playlist',)
    search_fields = ('playlist__name', 'tag__name')

# 注册 UserPlaylistCollection 模型
@admin.register(UserPlaylistCollection)
class UserPlaylistCollectionAdmin(admin.ModelAdmin):
    list_display = ('user', 'playlist', 'collected_at')
    list_filter = ('collected_at',)
    search_fields = ('user__username', 'playlist__name')
    date_hierarchy = 'collected_at'