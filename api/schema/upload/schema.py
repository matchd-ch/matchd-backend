import graphene
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from graphene import ObjectType
from graphene_django import DjangoObjectType
from graphene_file_upload.scalars import Upload
from graphql_auth.bases import Output
from graphql_jwt.decorators import login_required
from django.utils.translation import gettext as _

from db.forms import AttachmentForm
from db.helper import generic_error_dict, validate_upload, validation_error_to_dict, has_access_to_attachments
from db.models import Attachment, upload_configurations, AttachmentKey, \
    get_attachment_validator_map_for_key
from db.validators import AttachmentKeyValidator

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
        key = kwargs.get('key', None)

        if file is None:
            return UserUpload(success=False, errors=generic_error_dict('file', _('Field is required'), 'required'))

        errors = {}

        # check if user is allowed to upload files with the provided key
        try:
            attachment_key_validator = AttachmentKeyValidator()
            attachment_key_validator.validate(key, user)
        except ValidationError as error:
            errors.update(validation_error_to_dict(error, 'key'))

        if errors:
            return UserUpload(success=False, errors=errors)

        # validate uploaded file and determine the model for the attachment
        validator_model_map = get_attachment_validator_map_for_key(key)

        attachment_model = None
        attachment_model_name = None
        attachment_errors = {}
        is_valid_attachment = False
        for (model, types, size) in validator_model_map:
            type_failed = False
            # validate file type only
            try:
                validate_upload(file, types)
            except ValidationError as error:
                attachment_errors.update(validation_error_to_dict(error, 'file'))
                type_failed = True

            if not type_failed:
                # validate file type and file size
                try:
                    validate_upload(file, types, size)
                    attachment_model = model
                    # noinspection PyProtectedMember
                    attachment_model_name = model._meta.model_name
                    is_valid_attachment = True
                except ValidationError as error:
                    attachment_errors.update(validation_error_to_dict(error, 'file'))

        if not is_valid_attachment:
            return UserUpload(success=False, errors=attachment_errors)

        # create file attachment (image, video or document)
        try:
            file_attachment = attachment_model.objects.create(file=file)
            file_attachment = attachment_model.objects.get(id=file_attachment.id)
        except attachment_model.DoesNotExist:
            errors.update(generic_error_dict('file', _('File could not be saved.'), 'error'))
            return UserUpload(success=False, errors=errors)

        # create user attachment
        attachment_content_type = ContentType.objects.get(app_label='db', model=attachment_model_name)
        profile_content_type = user.get_profile_content_type()
        profile_id = user.get_profile_id()

        form = AttachmentForm(data={
            'content_type': profile_content_type,
            'object_id': profile_id,
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
    attachments = graphene.List(
        AttachmentType,
        key=AttachmentKeyType(required=True),
        user_id=graphene.Int(required=False)
    )

    def resolve_attachments(self, info, **kwargs):
        user = info.context.user
        key = kwargs.get('key')

        # if user id is None, we assume to return the list of the currently logged in user
        user_id = kwargs.get('user_id', None)
        attachment_owner = user
        if user_id is not None:
            attachment_owner = get_user_model().objects.get(pk=user_id)

        # check if the owner has a public profile
        # if not, return an empty list
        show = has_access_to_attachments(user, attachment_owner)
        if not show:
            return []

        # get profile content type and id
        profile_content_type = attachment_owner.get_profile_content_type()
        profile_id = attachment_owner.get_profile_id()

        return Attachment.objects.filter(
            key=key,
            content_type=profile_content_type,
            object_id=profile_id).\
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
