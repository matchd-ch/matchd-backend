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

from db.helper import generic_error_dict, validate_upload, validation_error_to_dict
from db.models import Image, Attachment, UserType, Video, File


class UserUpload(Output, graphene.Mutation):
    class Arguments:
        file = Upload()
        key = graphene.String()

    @classmethod
    @login_required
    def mutate(cls, root, info, **kwargs):
        user = info.context.user
        file = info.context.FILES.get('0')

        if file is None:
            return UserUpload(success=False, errors=generic_error_dict('file', _('Field is required'), 'required'))

        errors = {}

        validator_model_map = [
            (Image, settings.USER_UPLOADS_IMAGE_TYPES, settings.USER_UPLOADS_MAX_IMAGE_SIZE),
            (Video, settings.USER_UPLOADS_VIDEO_TYPES, settings.USER_UPLOADS_MAX_VIDEO_SIZE),
            (File, settings.USER_UPLOADS_DOCUMENT_TYPES, settings.USER_UPLOADS_MAX_DOCUMENT_SIZE)
        ]

        attachment_model = None
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
            except ValidationError as error:
                errors.update(validation_error_to_dict(error, 'file'))

        if errors:
            return UserUpload(success=False, errors=errors)

        # todo create form
        file_attachment = attachment_model.objects.create(file=file)
        user_content_type = UserType.content_type_for_user(user)
        Attachment.objects.create(
            content_type=user_content_type,
            object_id=user.student.id,
            attachment_type=ContentType.objects.get(app_label='db', model='image'),
            attachment_id=file_attachment.id,
            key=kwargs.get('key')
        )

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
        self.attachment_object.get_file_size()


class AttachmentQuery(ObjectType):
    attachments = graphene.List(AttachmentType, key=graphene.String(required=True))

    def resolve_attachments(self, info, **kwargs):
        user = info.context.user
        key = kwargs.get('key')
        return Attachment.objects.filter(
            key=key,
            content_type__model='student',
            object_id=user.student.id).\
            prefetch_related('content_object', 'attachment_object')
