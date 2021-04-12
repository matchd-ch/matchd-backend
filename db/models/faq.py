from django.db import models


class FAQ(models.Model):
    category = models.ForeignKey('db.FAQCategory', on_delete=models.CASCADE, related_name='faq', blank=False, null=False)
    title = models.CharField(max_length=255, blank=False, null=False)
    question = models.CharField(max_length=1000, blank=False, null=False)
    answer = models.CharField(max_length=1000, blank=False, null=False)
