from datetime import date

from django.contrib.auth import get_user_model
from django.db import models

from shared.models import TimeStampModel

User = get_user_model()


class Article(TimeStampModel):
    title = models.CharField(max_length=150)
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="articles")
    is_published = models.BooleanField(default=False, db_index=True)
    published_date = models.DateField(null=True, blank=True)
    likes = models.ManyToManyField(User, blank=True)

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        """If is_published is True set the published_date to current date"""
        if self.is_published:
            self.published_date = date.today()
        super().save(*args, **kwargs)

    class Meta:
        db_table = "article"
        constraints = [
            models.UniqueConstraint(fields=["title", "user"], name="unique_user_title")
        ]


class ArticleComment(TimeStampModel):
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name="comments"
    )
    comment = models.CharField(max_length=255)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="article_comments", blank=True
    )

    class Meta:
        db_table = "article_comment"

    def __str__(self) -> str:
        return self.comment
