from django.contrib.auth import get_user_model
from django.db import models


class OnlineProject(models.Model):
    url = models.URLField(max_length=2048)
    student = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
