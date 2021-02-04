from django.contrib.auth import get_user_model
from django.db import models

from db.models import Language, LanguageLevel, Student


class UserLanguageRelation(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    language_level = models.ForeignKey(LanguageLevel, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('language', 'language_level',)
