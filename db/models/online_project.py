from django.db import models


class OnlineProject(models.Model):
    url = models.URLField(max_length=255, unique=True)
