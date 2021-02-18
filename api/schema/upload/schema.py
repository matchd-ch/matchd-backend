import graphene
from django.contrib.contenttypes.models import ContentType
from graphene import ObjectType
from graphene_django import DjangoObjectType
from graphene_file_upload.scalars import Upload
from graphql_auth.bases import Output
from graphql_jwt.decorators import login_required

from db.models import Image, Attachment, UserType


class UserUpload(Output, graphene.Mutation):
    class Arguments:
        file = Upload()
        key = graphene.String()

    @classmethod
    @login_required
    def mutate(cls, root, info, **kwargs):
        user = info.context.user

        files = info.context.FILES
        image = Image.objects.create(file=files.get('0'))

        user_content_type = UserType.content_type_for_user(user)

        Attachment.objects.create(
            content_type=user_content_type,
            object_id=user.student.id,
            attachment_type=ContentType.objects.get(app_label='db', model='image'),
            attachment_id=image.id,
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
