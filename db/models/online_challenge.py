from django.db import models


class OnlineChallenge(models.Model):
    url = models.URLField(max_length=2048)
    student = models.ForeignKey('db.Student',
                                on_delete=models.CASCADE,
                                related_name='online_challenges')
