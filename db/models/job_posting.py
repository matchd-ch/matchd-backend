from django.db import models


class JobPosting(models.Model):
    description = models.TextField(max_length=1000)
    job_option = models.ForeignKey('db.JobOption', null=False, blank=False, on_delete=models.CASCADE)
    workload = models.CharField(max_length=255, blank=True, null=True)
    company = models.ForeignKey('db.Company', null=False, blank=False, on_delete=models.CASCADE)
    job_from_date = models.DateField(null=False, blank=False)
    job_to_date = models.DateField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)
