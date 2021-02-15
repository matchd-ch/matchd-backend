from django.db import models

from db.models import Student


class Distinction(models.Model):
    text = models.CharField(max_length=255)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('text', 'student',)
