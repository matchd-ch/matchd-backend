from django.db import models


class LanguageNiveau(models.Model):
    name = models.CharField(max_length=255, unique=True)
