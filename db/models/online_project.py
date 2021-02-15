from django.db import models


class OnlineProject(models.Model):
    url = models.URLField(max_length=2048)
    student = models.ForeignKey('db.Student', on_delete=models.CASCADE)
