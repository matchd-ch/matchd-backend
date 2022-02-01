import graphene
from graphene import ObjectType
from graphene_file_upload.scalars import Upload
from graphql_auth.bases import Output
from graphql_jwt.decorators import login_required

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied

from api.schema.attachment import AttachmentKey
from api.schema.project_posting.schema import ProjectPostingInput

from db.exceptions import FormException
from db.forms import AttachmentForm, process_upload, process_attachment
from db.helper import generic_error_dict
from db.models import upload_configurations, ProjectPosting as ProjectPostingModel, ProfileType, \
    AttachmentKey as AttachmentKeyModel


class UserUpload(Output, graphene.Mutation):
    class Arguments:
        file = Upload(required=True)
        key = AttachmentKey(required=True)
        projectPosting = ProjectPostingInput(required=False)

    # pylint: disable=R0912
    # pylint: disable=R0915
    @classmethod
    @login_required
    def mutate(cls, root, info, **kwargs):
        errors = {}
        user = info.context.user
        key = kwargs.get('key', None)

        project_posting = kwargs.get('projectPosting', None)
        if project_posting is not None:
            try:
                project_posting = ProjectPostingModel.objects.get(pk=project_posting.get('id'))
            except ProjectPostingModel.DoesNotExist as exception:
                errors.update(generic_error_dict('projectPosting', str(exception), 'invalid'))
                return UserUpload(success=False, errors=errors)

        if project_posting is not None and key not in (
                AttachmentKeyModel.PROJECT_POSTING_DOCUMENTS, AttachmentKeyModel.PROJECT_POSTING_IMAGES,):
            errors.update(generic_error_dict('key', 'Invalid key', 'invalid'))
            return UserUpload(success=False, errors=errors)

        content_type = user.get_profile_content_type()
        object_id = user.get_profile_id()
        if project_posting is not None:
            if user.type in ProfileType.valid_company_types():
                if user.company != project_posting.company:
                    raise PermissionDenied('You are not the owner of this project.')
            if user.type in ProfileType.valid_student_types():
                if user.student != project_posting.student:
                    raise PermissionDenied('You are not the owner of this project.')

            content_type = ContentType.objects.get(app_label='db', model='projectposting')
            object_id = project_posting.id

        try:
            file = process_upload(user, key, info.context.FILES)
            attachment_content_type, file_attachment = process_attachment(user, key, file)
        except FormException as exception:
            return UserUpload(success=False, errors=exception.errors)

        form = AttachmentForm(data={
            'content_type': content_type,
            'object_id': object_id,
            'attachment_type': attachment_content_type,
            'attachment_id': file_attachment.id,
            'key': key
        })
        form.full_clean()
        if form.is_valid():
            form.save()
        else:
            errors.update(form.errors.get_json_data())

        if errors:
            return UserUpload(success=False, errors=errors)

        return UserUpload(success=True, errors=None)


class UploadMutation(ObjectType):
    upload = UserUpload.Field()


class UploadTypeConfiguration(ObjectType):
    content_types = graphene.NonNull(graphene.List(graphene.NonNull(graphene.String)))
    max_size = graphene.NonNull(graphene.Int)


class UploadConfiguration(ObjectType):
    content_types_configuration = graphene.NonNull(graphene.List(graphene.NonNull(UploadTypeConfiguration)))
    max_files = graphene.NonNull(graphene.Int)
    key = graphene.NonNull(AttachmentKey)


class UploadConfigurationQuery(ObjectType):
    upload_configurations = graphene.List(UploadConfiguration)

    def resolve_upload_configurations(self, info, **kwargs):
        return upload_configurations
