import graphene
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from graphene import ObjectType
from graphene_django import DjangoObjectType
from graphene_file_upload.scalars import Upload
from graphql_auth.bases import Output
from graphql_jwt.decorators import login_required
from django.utils.translation import gettext as _

from db.forms import AttachmentForm
from db.helper import generic_error_dict, validate_upload, validation_error_to_dict
from db.models import Image, Attachment, UserType, Video, File, upload_configurations
from db.models.attachment import AttachmentKey

AttachmentKeyType = graphene.Enum.from_enum(AttachmentKey)


class UserUpload(Output, graphene.Mutation):
    class Arguments:
        file = Upload(required=True)
        key = AttachmentKeyType(required=True)

    @classmethod
    @login_required
    def mutate(cls, root, info, **kwargs):
        user = info.context.user
        file = info.context.FILES.get('0')

        if file is None:
            return UserUpload(success=False, errors=generic_error_dict('file', _('Field is required'), 'required'))

        errors = {}

        validator_model_map = [
            (Image, settings.USER_UPLOADS_IMAGE_TYPES, settings.USER_UPLOADS_MAX_IMAGE_SIZE, ),
            (Video, settings.USER_UPLOADS_VIDEO_TYPES, settings.USER_UPLOADS_MAX_VIDEO_SIZE, ),
            (File, settings.USER_UPLOADS_DOCUMENT_TYPES, settings.USER_UPLOADS_MAX_DOCUMENT_SIZE, )
        ]

        attachment_model = None
        attachment_model_name = None
        for (model, types, size) in validator_model_map:
            try:
                # validate file type only
                validate_upload(file, types)
            except ValidationError:
                continue

            try:
                # validate file type and file size
                validate_upload(file, types, size)
                attachment_model = model
                # noinspection PyProtectedMember
                attachment_model_name = model._meta.model_name
            except ValidationError as error:
                errors.update(validation_error_to_dict(error, 'file'))

        if errors:
            return UserUpload(success=False, errors=errors)

        # create file attachment (image, video or document)
        try:
            file_attachment = attachment_model.objects.create(file=file)
            file_attachment = attachment_model.objects.get(id=file_attachment.id)
        except attachment_model.DoesNotExist:
            errors.update(generic_error_dict('file', _('File could not be saved.'), 'error'))
            return UserUpload(success=False, errors=errors)

        # create user attachment
        attachment_content_type = ContentType.objects.get(app_label='db', model=attachment_model_name)
        user_content_type = UserType.content_type_for_user(user)

        form = AttachmentForm(data={
            'content_type': user_content_type,
            'object_id': user.get_profile_id(),
            'attachment_type': attachment_content_type,
            'attachment_id': file_attachment.id,
            'key': kwargs.get('key')
        })
        form.full_clean()
        if form.is_valid():
            form.save()
        else:
            errors.update(form.errors.get_json_data())

        if errors:
            return UserUpload(success=False, errors=errors)

        return UserUpload(success=True, errors=None)


class UploadMutation(graphene.ObjectType):
    upload = UserUpload.Field()


class AttachmentType(DjangoObjectType):

    url = graphene.String()
    type = graphene.String()
    file_size = graphene.Int()

    class Meta:
        model = Attachment
        fields = ('id',)

    def resolve_url(self: Attachment, info):
        return self.attachment_object.absolute_url

    def resolve_type(self: Attachment, info):
        return self.attachment_type.model

    def resolve_file_size(self: Attachment, info):
        return self.attachment_object.get_file_size()


class AttachmentQuery(ObjectType):
    attachments = graphene.List(AttachmentType, key=AttachmentKeyType(required=True))

    def resolve_attachments(self, info, **kwargs):
        user = info.context.user
        key = kwargs.get('key')

        return Attachment.objects.filter(
            key=key,
            content_type__model='student',
            object_id=user.student.id).\
            prefetch_related('content_object', 'attachment_object')


class UploadTypeConfiguration(ObjectType):
    content_types = graphene.List(graphene.String)
    max_size = graphene.Int()


class UploadConfiguration(ObjectType):
    content_types_configuration = graphene.List(UploadTypeConfiguration)
    max_files = graphene.Int()
    key = AttachmentKeyType()


class UploadConfigurationQuery(ObjectType):
    upload_configurations = graphene.List(UploadConfiguration)

    def resolve_upload_configurations(self, info, **kwargs):
        return upload_configurations
