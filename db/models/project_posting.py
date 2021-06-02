from datetime import datetime

from django.db import models
from django.utils.translation import gettext as _
from wagtail.search import index


def default_date():
    return datetime.strptime('01.01.1970', '%m.%d.%Y').date()


class ProjectPostingState(models.TextChoices):
    DRAFT = 'draft', _('Draft')
    PUBLIC = 'public', _('Public')


class ProjectPosting(models.Model, index.Indexed):
    title = models.CharField(max_length=50, blank=True)
    slug = models.CharField(max_length=100, blank=True)
    project_type = models.ForeignKey('db.ProjectType', null=False, blank=False, on_delete=models.CASCADE)
    topic = models.ForeignKey('db.Topic', null=False, blank=False, on_delete=models.CASCADE)
    keywords = models.ManyToManyField('db.Keyword', related_name='project_postings')
    description = models.TextField(max_length=300)
    additional_information = models.TextField(max_length=1000)
    website = models.URLField(max_length=2048, blank=True)
    project_from_date = models.DateField(null=True, blank=True)
    employee = models.ForeignKey('db.Employee', on_delete=models.SET_NULL, blank=True, null=True)
    company = models.ForeignKey('db.Company', null=False, blank=False, on_delete=models.CASCADE,
                                related_name='project_postings')
    date_created = models.DateTimeField(auto_now_add=True)
    date_published = models.DateTimeField(null=True)

    @classmethod
    def get_indexed_objects(cls):
        return cls.objects.filter(state=ProjectPostingState.PUBLIC).\
            select_related('company', 'project_type', 'topic', 'employee').prefetch_related('keywords')

    search_fields = [
        index.FilterField('project_type_id'),
        index.FilterField('topic_id'),
        index.RelatedFields('keywords', [
            index.FilterField('id'),
        ]),
        index.FilterField('project_from_date', es_extra={
            'type': 'date',
            'format': 'yyyy-MM-dd',
            'null_value': default_date()
        })
    ]
