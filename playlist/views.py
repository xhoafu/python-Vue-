from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .models import Playlist, PlaylistSong, PlaylistTag, UserPlaylistCollection
from .serializers import PlaylistSerializer, PlaylistSongSerializer, PlaylistTagSerializer, UserPlaylistCollectionSerializer
from music.models import Music  # 假设 Music 模型在另一个应用中
from django.contrib.auth.models import User
from django.db.models import Count
from .playlistpage import PlaylistPagination

class PlaylistViewSet(viewsets.ModelViewSet):
    """
    歌单视图集，支持 CRUD 操作
    """
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # 仅允许认证用户进行写操作
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description', 'tags__name']  # 支持按名称、描述和标签搜索
    ordering_fields = ['created_at', 'play_count', 'like_count']  # 支持按创建时间、播放次数和点赞数排序
    pagination_class = PlaylistPagination  # 指定分页类

    def perform_create(self, serializer):
        # 创建歌单时，将当前登录的用户作为创建者
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def collect(self, request, pk=None):
        """
        收藏歌单
        """
        playlist = self.get_object()
        UserPlaylistCollection.objects.get_or_create(user=request.user, playlist=playlist)
        return Response({'status': 'collected'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def uncollect(self, request, pk=None):
        """
        取消收藏歌单
        """
        playlist = self.get_object()
        UserPlaylistCollection.objects.filter(user=request.user, playlist=playlist).delete()
        return Response({'status': 'uncollected'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def recommended(self, request):
        """
        推荐歌单（按点赞数和播放次数排序）
        """
        playlists = Playlist.objects.annotate(
            total_likes=Count('like_count'),
            total_plays=Count('play_count')
        ).order_by('-total_likes', '-total_plays')[:10]  # 获取前10个推荐歌单
        serializer = self.get_serializer(playlists, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def page_info(self, request):
        """
        获取分页信息
        """
        paginator = self.pagination_class()
        paginator.paginate_queryset(self.get_queryset(), request)
        return Response({
            'page_count': paginator.page.paginator.num_pages,
            'current_page': paginator.page.number,
            'page_size': paginator.page_size,
            'total_items': paginator.page.paginator.count
        })

class PlaylistSongViewSet(viewsets.ModelViewSet):
    """
    歌单与歌曲关联视图集
    """
    queryset = PlaylistSong.objects.all()
    serializer_class = PlaylistSongSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        # 根据歌单ID过滤
        playlist_id = self.kwargs.get('playlist_id')
        if playlist_id:
            return PlaylistSong.objects.filter(playlist_id=playlist_id)
        return super().get_queryset()

class PlaylistTagViewSet(viewsets.ModelViewSet):
    """
    歌单与标签关联视图集
    """
    queryset = PlaylistTag.objects.all()
    serializer_class = PlaylistTagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        # 根据歌单ID过滤
        playlist_id = self.kwargs.get('playlist_id')
        if playlist_id:
            return PlaylistTag.objects.filter(playlist_id=playlist_id)
        return super().get_queryset()

class UserPlaylistCollectionViewSet(viewsets.ModelViewSet):
    """
    用户收藏歌单视图集
    """
    queryset = UserPlaylistCollection.objects.all()
    serializer_class = UserPlaylistCollectionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # 获取当前用户收藏的歌单
        return UserPlaylistCollection.objects.filter(user=self.request.user)