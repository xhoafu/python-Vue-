from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class UserProfile(models.Model):
    GENDER_CHOICES = (
        ("male", u"男"),
        ("female", u"女")
    )

    user = models.OneToOneField(User,on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True,blank=True)
    profile_picture = models.ImageField(upload_to='profile_pic/',null=True,blank=True)
    phone =models.CharField(max_length=30,blank=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, default="female", verbose_name="性别")

    def __str__(self):
        return self.user.username