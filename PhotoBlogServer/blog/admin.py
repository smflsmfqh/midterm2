from django.contrib import admin
from .models import Post, Image

class PostAdmin(admin.ModelAdmin):
    fields = ('author', 'title', 'text', 'created_date', 'published_date', 'image')  # 여기에 이미지 필드를 추가

admin.site.register(Post, PostAdmin)
