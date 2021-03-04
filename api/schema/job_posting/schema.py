import graphene
from django.utils.translation import gettext as _
from graphql_auth.bases import Output
from graphql_jwt.decorators import login_required

from api.schema.job_option import JobOptionInputType
from db.exceptions import FormException
from db.forms import process_job_posting_form_step_1


class JobPostingInputStep1(graphene.InputObjectType):
    description = graphene.String(description=_('Description'), required=True)
    job_option = graphene.Field(JobOptionInputType, required=True)
    workload = graphene.String(description=_('Workload'), required=True)
    job_from_date = graphene.String(required=True)
    job_to_date = graphene.String(required=False)
    url = graphene.String(required=False)


class JobPostingStep1(Output, graphene.Mutation):

    job_posting_id = graphene.ID()

    class Arguments:
        step1 = JobPostingInputStep1(description=_('Job Posting Input Step 1 is required.'), required=True)

    class Meta:
        description = _('Creates a job posting')

    @classmethod
    @login_required
    def mutate(cls, root, info, **data):
        user = info.context.user
        form_data = data.get('step1', None)
        try:
            job_posting = process_job_posting_form_step_1(user, form_data)
        except FormException as exception:
            return JobPostingStep1(success=False, errors=exception.errors)
        return JobPostingStep1(success=True, errors=None, job_posting_id=job_posting.id)


class JobPostingMutation(graphene.ObjectType):
    job_posting_step_1 = JobPostingStep1.Field()
