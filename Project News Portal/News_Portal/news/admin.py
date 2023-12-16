from django.contrib import admin
from .models import *


def nullfy_quantity(modeladmin, request, queryset):
    queryset.update(quantity=0)


nullfy_quantity.short_description = 'Обнулить товары'


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'post_type', 'created_at', 'rating']
    list_filter = ('rating', 'author')
    search_fields = ('title',)
    actions = [nullfy_quantity]


class PostCategoryAdmin(admin.ModelAdmin):
    list_display = ['post', 'category']


class CommentsAdmin(admin.ModelAdmin):
    list_display = ['post', 'user', 'rating']


admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(Author)
admin.site.register(PostCategory, PostCategoryAdmin)
admin.site.register(Comment, CommentsAdmin)
