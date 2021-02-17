from django.db import models


class Distinction(models.Model):
    text = models.CharField(max_length=255)
    student = models.ForeignKey('db.Student', on_delete=models.CASCADE, related_name='distinctions')

    class Meta:
        unique_together = ('text', 'student',)
