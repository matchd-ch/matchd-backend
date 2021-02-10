from django.db import models

from db.models import Student


class OnlineProject(models.Model):
    url = models.URLField(max_length=2048)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
