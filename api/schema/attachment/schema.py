import graphene
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from graphene import ObjectType, relay
from graphene_django import DjangoObjectType
from graphql_auth.bases import Output
from graphql_jwt.decorators import login_required
from django.utils.translation import gettext as _

from db.helper import generic_error_dict, has_access_to_attachments, get_company_or_student
from db.models import AttachmentKey as AttachmentKeyModel, Attachment as AttachmentModel, Company, Student, \
    ProjectPosting as ProjectPostingModel

AttachmentKey = graphene.Enum.from_enum(AttachmentKeyModel)


class DeleteAttachment(Output, graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    @classmethod
    @login_required
    def mutate(cls, root, info, **kwargs):
        user = info.context.user
        profile_id = user.get_profile_id()
        attachment_id = kwargs.get('id', None)

        # check if the attachment exists and the user is owner of the attachment
        try:
            attachment = AttachmentModel.objects.get(pk=attachment_id)
        except AttachmentModel.DoesNotExist:
            return DeleteAttachment(success=False, errors=generic_error_dict('id', _('Attachment does not exist'),
                                                                             'not_found'))

        project_posting_type = ContentType.objects.get(app_label='db', model='projectposting')

        if attachment.content_type.id == project_posting_type.id:
            try:
                project_posting = ProjectPostingModel.objects.get(pk=attachment.object_id)
                if project_posting.get_owner() != user:
                    return PermissionDenied('You are not allowed to perform this action.')
            except ProjectPostingModel.DoesNotExist:
                return DeleteAttachment(
                    success=False, errors=generic_error_dict('id', _('ProjectPosting does not exist'), 'not_found'))
        else:
            if not attachment.object_id == profile_id:
                return PermissionDenied('You are not allowed to perform this action.')

        # delete file and attachment
        try:
            file = attachment.attachment_object
            file.delete()
            attachment.delete()
        except Exception as exception:  # pragma: no cover
            return DeleteAttachment(
                success=False,
                errors=generic_error_dict(
                    'id', f'{_("Error deleting file")}:{str(exception)}', 'error'))  # pragma: no cover
        return DeleteAttachment(success=True, errors=None)


class AttachmentMutation(ObjectType):
    deleteAttachment = DeleteAttachment.Field()


class Attachment(DjangoObjectType):
    url = graphene.NonNull(graphene.String)
    mime_type = graphene.NonNull(graphene.String)
    file_size = graphene.NonNull(graphene.Int)
    file_name = graphene.NonNull(graphene.String)

    class Meta:
        model = AttachmentModel
        interfaces = (relay.Node,)
        fields = tuple()
        convert_choices_to_enum = False

    def resolve_url(self: AttachmentModel, info):
        return self.absolute_url

    def resolve_file_size(self: AttachmentModel, info):
        return self.attachment_object.get_file_size()

    def resolve_mime_type(self: AttachmentModel, info):
        return self.attachment_object.get_mime_type()

    def resolve_file_name(self: AttachmentModel, info):
        return self.attachment_object.filename


class AttachmentConnection(relay.Connection):

    class Meta:
        node = Attachment


class AttachmentQuery(ObjectType):
    attachments = relay.ConnectionField(
        AttachmentConnection,
        key=AttachmentKey(required=True),
        slug=graphene.String(required=False),
        id=graphene.ID(required=False)
    )

    # pylint: disable=R0912
    @login_required
    def resolve_attachments(self, info, **kwargs):
        user = info.context.user
        key = kwargs.get('key')

        is_project_posting = key in AttachmentKeyModel.valid_project_posting_keys()
        is_student = key in AttachmentKeyModel.valid_student_keys()
        is_company = key in AttachmentKeyModel.valid_company_keys()

        if not is_student and not is_company and not is_project_posting:
            return []

        model = None
        if is_student:
            model = Student
        if is_company:
            model = Company
        if is_project_posting:
            model = ProjectPostingModel

        slug = kwargs.get('slug', None)
        object_id = kwargs.get('id', None)
        if slug is not None:
            try:
                attachment_owner = model.objects.get(slug=slug)
            except model.DoesNotExist:
                attachment_owner = None
        elif object_id is not None:
            try:
                attachment_owner = model.objects.get(pk=object_id)
            except model.DoesNotExist:
                attachment_owner = None
        else:
            attachment_owner = get_company_or_student(user)

        if attachment_owner is None:
            return []

        # check if the owner has a public profile or a match exists
        # if not, return an empty list
        show = has_access_to_attachments(user, attachment_owner, key)
        if not show:
            return []

        if key in (AttachmentKey.STUDENT_AVATAR_FALLBACK, AttachmentKey.COMPANY_AVATAR_FALLBACK):
            if is_student:
                fallback = AttachmentModel.get_student_avatar_fallback(attachment_owner)
                return [fallback] if fallback is not None else []
            if is_company:
                fallback = AttachmentModel.get_company_avatar_fallback(attachment_owner)
                return [fallback] if fallback is not None else []
            if is_project_posting:
                fallback = AttachmentModel.get_project_posting_fallback(attachment_owner)
                return [fallback] if fallback is not None else []
            return []

        if not is_project_posting:
            # get profile content type and id
            profile_content_type = attachment_owner.get_profile_content_type()
            profile_id = attachment_owner.get_profile_id()
        else:
            profile_content_type = ContentType.objects.get(app_label='db', model='projectposting')
            profile_id = attachment_owner.id
        return AttachmentModel.objects.filter(
            key=key,
            content_type=profile_content_type,
            object_id=profile_id).\
            prefetch_related('content_object', 'attachment_object')

    def resolve_attachments_connection(self, info, **kwargs):
        user = info.context.user
        key = kwargs.get('key')

        is_project_posting = key in AttachmentKeyModel.valid_project_posting_keys()
        is_student = key in AttachmentKeyModel.valid_student_keys()
        is_company = key in AttachmentKeyModel.valid_company_keys()

        if not is_student and not is_company and not is_project_posting:
            return []

        model = None
        if is_student:
            model = Student
        if is_company:
            model = Company
        if is_project_posting:
            model = ProjectPostingModel

        slug = kwargs.get('slug', None)
        object_id = kwargs.get('id', None)
        if slug is not None:
            try:
                attachment_owner = model.objects.get(slug=slug)
            except model.DoesNotExist:
                attachment_owner = None
        elif object_id is not None:
            try:
                attachment_owner = model.objects.get(pk=object_id)
            except model.DoesNotExist:
                attachment_owner = None
        else:
            attachment_owner = get_company_or_student(user)

        if attachment_owner is None:
            return []

        # check if the owner has a public profile or a match exists
        # if not, return an empty list
        show = has_access_to_attachments(user, attachment_owner, key)
        if not show:
            return []

        if key in (AttachmentKey.STUDENT_AVATAR_FALLBACK, AttachmentKey.COMPANY_AVATAR_FALLBACK):
            if is_student:
                fallback = AttachmentModel.get_student_avatar_fallback(attachment_owner)
                return [fallback] if fallback is not None else []
            if is_company:
                fallback = AttachmentModel.get_company_avatar_fallback(attachment_owner)
                return [fallback] if fallback is not None else []
            if is_project_posting:
                fallback = AttachmentModel.get_project_posting_fallback(attachment_owner)
                return [fallback] if fallback is not None else []
            return []

        if not is_project_posting:
            # get profile content type and id
            profile_content_type = attachment_owner.get_profile_content_type()
            profile_id = attachment_owner.get_profile_id()
        else:
            profile_content_type = ContentType.objects.get(app_label='db', model='projectposting')
            profile_id = attachment_owner.id
        return AttachmentModel.objects.filter(
            key=key,
            content_type=profile_content_type,
            object_id=profile_id).\
            prefetch_related('content_object', 'attachment_object')
