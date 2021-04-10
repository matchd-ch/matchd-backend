from django.db import models


class JobPostingLanguageRelation(models.Model):
    job_posting = models.ForeignKey('db.JobPosting', on_delete=models.CASCADE, related_name='languages')
    language = models.ForeignKey('db.Language', on_delete=models.CASCADE)
    language_level = models.ForeignKey('db.LanguageLevel', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('language', 'job_posting',)

    def language_level_concat(self):
        return f'{self.language.id}-{self.language_level.id}'
