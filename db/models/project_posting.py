from datetime import datetime

from django.db import models
from django.utils.translation import gettext as _
from wagtail.search import index


def default_date():
    return datetime.strptime('01.01.1970', '%m.%d.%Y').date()


class ProjectPostingState(models.TextChoices):
    DRAFT = 'draft', _('Draft')
    PUBLIC = 'public', _('Public')


# pylint: disable=R0902
class ProjectPosting(models.Model, index.Indexed):
    title = models.CharField(max_length=50, blank=True)
    slug = models.CharField(max_length=100, blank=True)
    project_type = models.ForeignKey('db.ProjectType',
                                     null=False,
                                     blank=False,
                                     on_delete=models.CASCADE)
    keywords = models.ManyToManyField('db.Keyword', related_name='project_postings')
    description = models.TextField(max_length=1500)
    team_size = models.PositiveIntegerField()
    compensation = models.TextField(max_length=300)
    website = models.URLField(max_length=2048, blank=True)
    project_from_date = models.DateField(null=True, blank=True)
    employee = models.ForeignKey('db.Employee', on_delete=models.SET_NULL, blank=True, null=True)
    student = models.ForeignKey('db.Student',
                                on_delete=models.CASCADE,
                                blank=True,
                                null=True,
                                related_name='project_postings')
    company = models.ForeignKey('db.Company',
                                null=True,
                                blank=True,
                                on_delete=models.CASCADE,
                                related_name='project_postings')
    form_step = models.IntegerField(
        default=2)    # since we save the project posting in step 1 the default value is 2
    state = models.CharField(choices=ProjectPostingState.choices,
                             default=ProjectPostingState.DRAFT,
                             max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    date_published = models.DateTimeField(null=True)

    @classmethod
    def get_indexed_objects(cls):
        return cls.objects.filter(state=ProjectPostingState.PUBLIC).\
            select_related('company', 'project_type', 'employee', 'student').prefetch_related('keywords')

    def project_keywords(self):
        return [obj.id for obj in self.keywords.all()]

    def cultural_fits(self):
        if self.company:
            return [obj.id for obj in self.company.cultural_fits.all()]
        return [obj.id for obj in self.student.cultural_fits.all()]

    def soft_skills(self):
        if self.company:
            return [obj.id for obj in self.company.soft_skills.all()]
        return [obj.id for obj in self.student.soft_skills.all()]

    def is_student(self):
        return self.student is not None

    def is_company(self):
        return self.company is not None

    def get_owner(self):
        if self.company:
            return self.employee.user
        return self.student.user

    search_fields = [
        index.SearchField('title', partial_match=True),
        index.SearchField('description', partial_match=True),
        index.FilterField('team_size'),
        index.FilterField('date_published'),
        index.FilterField('state'),
        index.RelatedFields('student', [
            index.FilterField('state'),
        ]),
        index.RelatedFields('company', [
            index.FilterField('type'),
            index.FilterField('state'),
        ]),
        index.FilterField('project_type_id'),
        index.FilterField('project_from_date'),
        index.FilterField('project_keywords'),
        index.FilterField('is_student', es_extra={'type': 'boolean'}),
        index.FilterField('is_company', es_extra={'type': 'boolean'}),
    ]
