from django.core.cache import cache
from django.db.models import Q
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework.generics import GenericAPIView
from .models import MusicAuthor, Music, AuthorBanner
from .serializers import MusicSerializers, MusicAuthorSerializers, MusicAuthorDetaSerializers, AuthorBannerSerializers, AuthorBannerDetaSerializers, MusicBannerSerializers
from rest_framework.response import Response
from rest_framework import status,viewsets
from django_filters.rest_framework import  DjangoFilterBackend
from rest_framework.decorators import action
from .filters import MusicFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .item_cf import ItemBasedCF
from .music_many import SongRecommender


# Create your views here.


# class MusicView(GenericAPIView):    # 音乐视图
#     queryset = Music.objects.all()
#     serializer_class = MusicSerializers
#
#     def get(self, request):
#         author = Music.objects.select_related('author').all()
#         return Response(self.serializer_class(instance=author, many=True).data)
#
#     def post(self, request):
#
#         serializer = self.serializer_class(data=request.data)
#
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
#
#
# class MusicDetaView(GenericAPIView):    #音乐详细视图
#     queryset = Music.objects.all()
#     serializer_class = MusicSerializers
#
#     def get(self, request, pk):
#         return Response(self.serializer_class(instance=self.get_object()).data)
#
#     def delete(self, request, pk):
#         try:
#             self.get_object().delete()
#
#             return Response(status=status.HTTP_204_NO_CONTENT)
#
#         except:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#
#     def put(self,request,pk):
#         instance = self.get_object()
#         serializer = self.serializer_class(instance=instance,data=request.data,partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)


class MusicViewSet(viewsets.ModelViewSet):
    queryset = Music.objects.all()
    serializer_class = MusicSerializers
    filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['title','author']
    filterset_class = MusicFilter

    def get_queryset(self):
        """
        根据 query 参数进行多字段模糊搜索
        """
        queryset = super().get_queryset()
        query = self.request.query_params.get('query', '')  # 获取查询参数
        print(self.request.user)

        if query:
            # 使用 Q 对象进行多字段模糊查询
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(name__icontains=query)
            )

        return queryset



class MusicListViewSet(viewsets.ModelViewSet):
    queryset = Music.objects.all()
    serializer_class = MusicSerializers
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['title','author']
    # filterset_class = MusicFilter

    @action(detail=False,methods=['get'])
    def musiclist(self,request):
        musics = list(self.get_queryset().order_by('?')[:10])
        serializer = self.serializer_class(instance=musics, many=True, context={'request': request})
        return Response(serializer.data,status=status.HTTP_200_OK)


# class MusicAuthorView(GenericAPIView):  # 作者视图
#     queryset = MusicAuthor.objects.all()
#     serializer_class = MusicAuthorSerializers
#
#     def get(self, request):
#
#         return Response(self.serializer_class(instance=self.get_queryset(), many=True).data)
#
#     def post(self, request):
#
#         serializer = self.serializer_class(data=request.data)
#
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
#
#
# class MusicAuthorDetaView(GenericAPIView):  # 嵌套的 作者嵌套音乐
#     queryset = MusicAuthor.objects.all()
#     serializer_class = MusicAuthorDetaSerializers
#
#     def get(self, request, pk):
#         # author = MusicAuthor.objects.get(pk=id)
#         return Response(self.serializer_class(instance=self.get_object()).data)


class MusicAuthorView(viewsets.ModelViewSet):
    queryset = MusicAuthor.objects.all()
    serializer_class = MusicAuthorSerializers
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']


# class AuthorBannerDetaView(GenericAPIView): # 作者轮播图的嵌套作者信息视图
#     queryset = AuthorBanner.objects.all()
#     serializer_class = AuthorBannerDetaSerializers
#
#     def get(self, request, pk):
#         return Response(self.serializer_class(instance=self.get_object()).data)
#
#     def delete(self, request, pk):
#         try:
#             self.get_object().delete()
#             return Response(status=status.HTTP_204_NO_CONTENT)
#         except:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#
#     def put(self, request, pk):
#         instance = self.get_object()
#         serializer = self.serializer_class(instance=instance, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
#
#
# class AuthorBannerView(GenericAPIView):  # 作者轮播图的视图
#     queryset = AuthorBanner.objects.all()
#     serializer_class = AuthorBannerSerializers
#
#     def get(self,request):
#         return Response(self.serializer_class(instance=self.get_queryset(),many=True).data)
#
#     def post(self,request):
#         serializer = self.serializer_class(data=request.data)
#
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



class AuthorBannerView(viewsets.ModelViewSet):
        queryset = AuthorBanner.objects.all()
        serializer_class = AuthorBannerDetaSerializers



class  MusicBannerView(GenericAPIView):
    queryset = AuthorBanner
    serializer_class = MusicBannerSerializers

    def get(self,request):
        return Response(self.serializer_class(instance=self.get_queryset()).data)


# class MusicRecommend(APIView):
#     @method_decorator(cache_page(60 * 60))  # 视图级缓存（不影响代码执行）
#     def get(self, request):
#         print(request.query_params.get('rec_id'))
#         user_id = request.query_params.get('rec_id') or '6a8a142084a4818c0dcac48bdfb3c39deacf5168'
#         cache_key = f"music_recommendations_user_{user_id}"
#
#         cached_data = cache.get(cache_key)
#         if cached_data:
#             return Response(cached_data, status=status.HTTP_200_OK)
#
#         # 计算推荐
#         ItemCf = ItemBasedCF()
#         ItemCf.writ()
#         top_n, next_k_n, song_details = ItemCf.recommend(user_id)
#         cache.set(cache_key, song_details, timeout=60 * 60)  # 1 小时缓存
#         return Response(song_details, status=201)


class MusicRecommend(APIView):
    @method_decorator(cache_page(60 * 60))
    def get(self, request):
        # 1. 校验必需参数
        rec_id = request.query_params.get('rec_id')
        if not rec_id or len(rec_id) <= 25:  # 如果 rec_id 为空或长度不大于 25，则使用默认 ID
            rec_id = '5a905f000fc1ff3df7ca807d57edb608863db05d'

        # 2. 构建缓存键
        cache_key = f"music_recommendations_user_{rec_id}"

        # 3. 检查缓存
        cached_data = cache.get(cache_key)
        if cached_data is not None:
            return Response(cached_data, status=status.HTTP_200_OK)

        # 4. 计算推荐结果
        item_cf = ItemBasedCF()
        item_cf.writ()
        top_n, next_k_n, song_details = item_cf.recommend(rec_id)

        # 5. 更新缓存
        cache.set(cache_key, song_details, timeout=60 * 60)

        # 6. 返回响应
        return Response(
            {
                "data": song_details,
                "metadata": {"cached": False, "rec_id": rec_id}
            },
            status=status.HTTP_200_OK
        )



class playlist(APIView,SongRecommender):
    @method_decorator(cache_page(60 * 60))
    def get(self, request):
        recommender = SongRecommender(r'D:\学习\Python\Django\MusicApp\数据\track_metadata_df_sub_song_merged4.csv')
        rap_recommendations = recommender.recommend_by_tags('rap', random_mode='weighted')
        rap_recommendations1 = recommender.recommend_by_tags("rock",random_mode='shuffle')
        rap_recommendations2 = recommender.recommend_by_tags("electronic", random_mode='weighted')
        # # 完全随机模式
        # print(recommender.recommend_by_tags("jazz", random_mode='shuffle'))
        #
        # # 加权随机模式
        # print(recommender.recommend_by_tags("rock", random_mode='weighted'))
        return Response({
            '说唱':rap_recommendations,
            '摇滚':rap_recommendations1,
            '电子音乐':rap_recommendations2
        },status=status.HTTP_200_OK)