from django.db import models


class UserLanguageRelation(models.Model):
    student = models.ForeignKey('db.Student', on_delete=models.CASCADE)
    language = models.ForeignKey('db.Language', on_delete=models.CASCADE)
    language_level = models.ForeignKey('db.LanguageLevel', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('language', 'student',)
