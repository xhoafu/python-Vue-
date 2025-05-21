from django.core.validators import FileExtensionValidator
from django.db import models

# Create your models here.


class MusicAuthor(models.Model):

    name = models.CharField(max_length=30)
    bio = models.TextField(blank=True,null=True)
    age = models.CharField(null=True)

    def __str__(self):
        return self.name


class Music(models.Model):
    """
    音乐
    """
    title = models.CharField(max_length=30)
    author = models.ForeignKey(MusicAuthor,on_delete=models.CASCADE,related_name='musics')
    release_year = models.IntegerField()
    duration = models.PositiveIntegerField()
    image = models.ImageField(upload_to='carousel_images/', verbose_name="图片", null=True, blank=True)
    album = models.CharField(max_length=30,blank=True,null=True)
    genre = models.CharField(max_length=30,blank=True,null=True)

    audio_file = models.FileField(
        upload_to='music/audio/',  # 音频文件上传到 media/music/audio 目录
        validators=[FileExtensionValidator(allowed_extensions=['mp3', 'wav', 'flac', 'aac'])],  # 只允许音频格式
        blank=True,  # 允许没有音频文件
        null=True
    )

    def __str__(self):
        return self.title


class Banner(models.Model):
    """
    音乐专辑轮播图
    """
    musics = models.ForeignKey(Music,on_delete=models.CASCADE,related_name='images')
    image = models.ImageField(upload_to='carousel_images/',verbose_name="图片", null=True, blank=True)
    add_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Carousel image for {self.music.title} ({'Main' if self.is_main_image else 'Secondary'})"


class AuthorBanner(models.Model):
    """
    音乐人专辑轮播图
    """
    author = models.ForeignKey(MusicAuthor,on_delete=models.CASCADE,related_name='author_images')
    image = models.ImageField(upload_to='author_images/',verbose_name="图片", null=True, blank=True)
    add_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Carousel image for {self.music.title} ({'Main' if self.is_main_image else 'Secondary'})"