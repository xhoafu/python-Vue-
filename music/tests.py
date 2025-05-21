from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import MusicAuthor, AuthorBanner

class AuthorBannerTest(TestCase):

    def setUp(self):
        # 创建一个测试作者
        self.author = MusicAuthor.objects.create(
            name="Test Author",
            bio="This is a test author bio.",
            age=30
        )

    def test_author_banner_image_upload(self):
        # 模拟上传图片文件
        image_content = b"fake image content for testing"
        uploaded_image = SimpleUploadedFile(
            "test_image.jpg",  # 文件名
            image_content,     # 文件内容
            content_type="image/jpeg"  # MIME 类型
        )

        # 向 AuthorBanner 表插入一条数据
        banner = AuthorBanner.objects.create(
            author=self.author,
            image=uploaded_image
        )

        # 验证 AuthorBanner 是否插入成功
        self.assertEqual(AuthorBanner.objects.count(), 1)
        self.assertEqual(banner.author.name, "Test Author")
        self.assertTrue(banner.image.name.startswith("author_images/test_image"))

        # 打印结果供调试（可选）
        print(f"Image Path: {banner.image.name}")
