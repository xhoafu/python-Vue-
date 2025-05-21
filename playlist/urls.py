from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PlaylistViewSet, PlaylistSongViewSet, PlaylistTagViewSet, UserPlaylistCollectionViewSet

router = DefaultRouter()
router.register(r'playlists', PlaylistViewSet)
router.register(r'playlists/(?P<playlist_id>\d+)/songs', PlaylistSongViewSet)
router.register(r'playlists/(?P<playlist_id>\d+)/tags', PlaylistTagViewSet)
router.register(r'collections', UserPlaylistCollectionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]