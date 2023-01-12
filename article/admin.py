from django.contrib import admin
from article.models import Article


class ArticleAdmin(admin.ModelAdmin):
    readonly_fields = ("published_date", "likes")


admin.site.register(Article, ArticleAdmin)
