from core.models import CommonInfo
from django.db import models

from django.contrib.auth import get_user_model


class KnowledgeBase(CommonInfo):

    title = models.CharField(max_length=225)
    description = models.TextField(null=True, blank=True)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title}"
