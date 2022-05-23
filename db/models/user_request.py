from django.db import models
from django.db.models.signals import post_save


class UserRequest(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    email = models.EmailField(blank=False, null=False)
    message = models.TextField(max_length=1024, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def post_save(sender, instance, created, **kwargs):
        post_save.disconnect(UserRequest.post_save,
                             UserRequest,
                             dispatch_uid='db.models.UserRequest')

        post_save.connect(UserRequest.post_save, UserRequest, dispatch_uid='db.models.UserRequest')


post_save.connect(UserRequest.post_save, UserRequest, dispatch_uid='db.models.UserRequest')
