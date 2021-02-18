from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Attachment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='user_type')
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    attachment_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='attachment_type')
    attachment_id = models.PositiveIntegerField()
    attachment_object = GenericForeignKey('attachment_type', 'attachment_id')

    key = models.CharField(max_length=100, blank=False, null=False)
