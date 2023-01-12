from django.db import models


class TimeStampModel(models.Model):
    created_dtm = models.DateTimeField(auto_now_add=True)
    updated_dtm = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
