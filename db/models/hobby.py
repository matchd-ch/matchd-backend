from django.db import models

from db.models import Student


class Hobby(models.Model):
    name = models.CharField(max_length=255)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='hobbies')

    class Meta:
        unique_together = ('name', 'student',)
