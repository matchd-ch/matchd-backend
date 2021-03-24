import graphene
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from graphene import ObjectType
from graphene_django import DjangoObjectType
from graphql_auth.bases import Output
from graphql_jwt.decorators import login_required
from django.utils.translation import gettext as _

from db.helper import generic_error_dict, has_access_to_attachments
from db.models import AttachmentKey as AttachmentKeyModel, Attachment, Company

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
            attachment = Attachment.objects.get(pk=attachment_id, object_id=profile_id)
        except Attachment.DoesNotExist:
            return DeleteAttachment(success=False, errors=generic_error_dict('id', _('Attachment does not exist'),
                                                                             'not_found'))
        # delete file and attachment
        try:
            file = attachment.attachment_object
            file.delete()
            attachment.delete()
        except Exception as exception:
            return DeleteAttachment(success=False, errors=generic_error_dict('id', '%s:%s' % (_('Error deleting file'),
                                                                                              str(exception)), 'error'))
        return DeleteAttachment(success=True, errors=None)


class AttachmentMutation(graphene.ObjectType):
    deleteAttachment = DeleteAttachment.Field()


class AttachmentType(DjangoObjectType):

    url = graphene.String()
    mime_type = graphene.String()
    file_size = graphene.Int()
    file_name = graphene.String()

    class Meta:
        model = Attachment
        fields = ('id',)
        convert_choices_to_enum = False

    def resolve_url(self: Attachment, info):
        return self.absolute_url

    def resolve_file_size(self: Attachment, info):
        return self.attachment_object.get_file_size()

    def resolve_mime_type(self: Attachment, info):
        return self.attachment_object.get_mime_type()

    def resolve_file_name(self: Attachment, info):
        return self.attachment_object.filename


class AttachmentQuery(ObjectType):
    attachments = graphene.List(
        AttachmentType,
        key=AttachmentKey(required=True),
        user_id=graphene.Int(required=False),
        slug=graphene.String(required=False)
    )

    @login_required
    def resolve_attachments(self, info, **kwargs):
        user = info.context.user
        key = kwargs.get('key')

        # if user id is None, we assume to return the list of the currently logged in user
        user_id = kwargs.get('user_id', None)
        slug = kwargs.get('slug', None)
        attachment_owner = user
        if user_id is not None:
            attachment_owner = get_object_or_404(get_user_model(), pk=user_id)
        elif slug is not None:
            attachment_owner = get_object_or_404(Company, slug=slug)

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
