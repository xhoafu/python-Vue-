from rest_framework import serializers
from .models import MusicAuthor, Music, AuthorBanner


class MusicSerializers(serializers.ModelSerializer):  # 音乐嵌套作者名字序列化器
    author_name = serializers.CharField(source='author.name')

    # author_name = MusicAuthorSerializers(source='author')
    class Meta:
        model = Music
        fields = '__all__'

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image:
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        return None


class MusicAuthorSerializers(serializers.ModelSerializer):  # 作者序列化器
    class Meta:
        model = MusicAuthor
        fields = ['name', 'age', 'bio', 'id']


class MusicAuthorDetaSerializers(serializers.ModelSerializer):  # 作者嵌套其所做音乐的序列化器
    musics = MusicSerializers(many=True)

    class Meta:
        model = MusicAuthor
        fields = ['name', 'age', 'bio', 'musics']


class AuthorBannerSerializers(serializers.ModelSerializer):  # 作者轮播图序列化器
    author_name = serializers.CharField(source='author.name')

    class Meta:
        model = AuthorBanner
        fields = '__all__'


# class AuthorBannerDetaSerializers(serializers.ModelSerializer):  # 作者嵌套图片轮播图
#     author_name = MusicAuthorSerializers(source='author')
#
#     class Meta:
#         model = AuthorBanner
#         # fields = ['image','author','author_name'
#         fields = '__all__'
class AuthorBannerDetaSerializers(serializers.ModelSerializer):
    author_name = MusicAuthorSerializers(source='author')
    # 添加歌曲数据
    musics = MusicSerializers(
        source='author.musics',
        many=True,
        read_only=True
    )

    class Meta:
        model = AuthorBanner
        fields = [
            'id', 'image', 'author',
            'author_name', 'musics', 'add_time'
        ]


class MusicBannerSerializers(serializers.ModelSerializer):
    author_name = AuthorBannerSerializers(read_only=True)

    class Meta:
        model = Music
        fields = '__all__'
