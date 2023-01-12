from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db import IntegrityError
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import View, generic

from article.models import Article


class ArticleCreateView(LoginRequiredMixin, generic.CreateView):
    model = Article
    fields = ("title", "content", "is_published")
    template_name = "article/create_article.html"

    def form_valid(self, form):
        try:
            form.instance.user = self.request.user
            form.save()
            return redirect("article:article_detail", form.instance.id)
        except IntegrityError:
            return JsonResponse({"status_code": 400, "message": "Title must be unique"})
        except Exception:
            return JsonResponse({"status_code": 500, "message": "Something went wrong"})


class ArticleListView(generic.ListView):
    model = Article
    template_name = "article/article_list.html"
    context_object_name = "articles"
    ordering = ("-published_date", "-id")

    def get_queryset(self):
        qs = super().get_queryset()
        published_articles = qs.filter(is_published=True)
        if "me" in self.request.GET:
            return qs.filter(user=self.request.user)
        return published_articles


class ArticleDetailView(generic.DetailView):
    model = Article
    template_name = "article/article_detail.html"
    context_object_name = "article"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = self.get_object()
        context["comments"] = article.comments.all()
        context["is_article_liked"] = article.likes.filter(
            id=self.request.user.id
        ).exists()
        context["likes_count"] = article.likes.all().count()
        context["is_article_owner"] = article.user == self.request.user
        return context


class ArticleUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Article
    template_name = "article/update_article.html"
    fields = ("title", "content", "is_published")
    context_object_name = "article"

    def dispatch(self, request, *args, **kwargs):
        """check user permission"""
        article = self.get_object()
        if article.user != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self) -> str:
        return reverse("article:article_detail", kwargs={"pk": self.kwargs.get("pk")})


class ArticleDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Article
    template_name = "article/article_detail.html"
    success_url = reverse_lazy("article:article_list")

    def dispatch(self, request, *args, **kwargs):
        article = self.get_object()
        if article.user != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class ArticleLikeView(LoginRequiredMixin, View):
    def post(self, request, article_id):
        article = get_object_or_404(Article, id=article_id)
        json_resp = {"success": True}
        # remove likes if user already liked the article else increase like
        if article.likes.filter(id=request.user.id).exists():
            article.likes.remove(request.user)
            json_resp["liked"] = False
        else:
            article.likes.add(request.user)
            json_resp["liked"] = True

        return JsonResponse(json_resp)
