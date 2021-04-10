from django.db import models


class UserLanguageRelation(models.Model):
    student = models.ForeignKey('db.Student', on_delete=models.CASCADE, related_name='languages')
    language = models.ForeignKey('db.Language', on_delete=models.CASCADE)
    language_level = models.ForeignKey('db.LanguageLevel', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('language', 'student',)

    def language_level_concat(self):
        return f'{self.language.id}-{self.language_level.id}'
