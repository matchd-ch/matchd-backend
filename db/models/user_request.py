from django.db import models

class UserRequest(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    email = models.EmailField(blank=False, null=False)
    message = models.TextField(max_length=1024, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)