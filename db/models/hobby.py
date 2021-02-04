from django.contrib.auth import get_user_model
from django.db import models


class Hobby(models.Model):
    name = models.CharField(max_length=255)
    student = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
