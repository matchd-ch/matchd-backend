from django.db import models


class LanguageNiveau(models.Model):
    niveau = models.CharField(max_length=255)
