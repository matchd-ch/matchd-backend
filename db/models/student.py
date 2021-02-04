from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.db import models


class Student(models.Model):
    user = models.OneToOneField(to=get_user_model(), on_delete=models.CASCADE, related_name='student')
    mobile = models.CharField(max_length=12, blank=True, validators=[RegexValidator(regex=r'\+[0-9]{11}')])
    skills = models.ManyToManyField('db.Skill', related_name='skills')
