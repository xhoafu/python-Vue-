from django.contrib import admin
from .models import MusicAuthor,Music
# Register your models here.


class MusicAdmin(admin.ModelAdmin):

    list_display = ('title','author','release_year','audio_file')
    list_filter = ('author','title')


class MusicAuthorAdmin(admin.ModelAdmin):

    list_display = ('name','age','bio')


admin.site.register(Music,MusicAdmin)
admin.site.register(MusicAuthor,MusicAuthorAdmin)