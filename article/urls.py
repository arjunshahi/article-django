from django.urls import path

from article import views as article_views

app_name = "article"

urlpatterns = [
    path("", article_views.ArticleListView.as_view(), name="article_list"),
    path("create/", article_views.ArticleCreateView.as_view(), name="article_create"),
    path(
        "detail/<int:pk>/",
        article_views.ArticleDetailView.as_view(),
        name="article_detail",
    ),
    path(
        "update/<int:pk>/",
        article_views.ArticleUpdateView.as_view(),
        name="article_update",
    ),
    path(
        "delete/<int:pk>/",
        article_views.ArticleDeleteView.as_view(),
        name="article_delete",
    ),
    path(
        "like/<int:article_id>/",
        article_views.ArticleLikeView.as_view(),
        name="like_article",
    ),
]
