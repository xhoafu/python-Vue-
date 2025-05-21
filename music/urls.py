from django.urls import path,re_path,include
from rest_framework.routers import DefaultRouter
from .views import MusicAuthorView,AuthorBannerView,MusicBannerView,MusicViewSet,MusicListViewSet,MusicRecommend,playlist

router = DefaultRouter()
router.register(r'music_filter',MusicViewSet,basename='music_filter')
router.register(r'author',MusicAuthorView)
router.register(r'authorbanner',AuthorBannerView)
router.register(r'music',MusicListViewSet,basename='music')

urlpatterns = [
    # path('music/',MusicView.as_view(),name='music'),
    # path('music/<int:pk>/',MusicDetaView.as_view(),name='music_deta'),
    path('',include(router.urls)),
    path('musicbanner/',MusicBannerView.as_view(),name='music_banner'),
    # path('author/',MusicAuthorView.as_view(),name='author'),
    # re_path("author/(?P<pk>\d+)",MusicAuthorDetaView.as_view(),name='author_deta'),
    # path("authorbanner/",AuthorBannerView.as_view(),name='author_banner1'),
    # re_path("authorbanner/(?P<pk>\d+)",AuthorBannerDetaView.as_view(),name='author_banner'),
    path('recommend/',MusicRecommend.as_view(),name='recommend'),
    path('playlist/',playlist.as_view(),name='playlist'),
]