import graphene
from graphene import ObjectType
from graphene_file_upload.scalars import Upload
from graphql_auth.bases import Output
from graphql_jwt.decorators import login_required

from api.schema.attachment import Attachment, AttachmentKey
from api.schema.project_posting.schema import ProjectPostingInput

from db.context.upload.resource import Resource
from db.context.upload.uploader import Uploader
from db.models import upload_configurations


class UserUpload(Output, graphene.Mutation):

    attachment = graphene.Field(lambda: Attachment)

    class Arguments:
        file = Upload(required=True)
        key = AttachmentKey(required=True)
        projectPosting = ProjectPostingInput(required=False)

    @classmethod
    @login_required
    def mutate(cls, root, info, **kwargs):
        user = info.context.user
        key = kwargs.get('key', None)
        project_posting = kwargs.get('projectPosting', None)

        resource = Resource(user=user,
                            key=key,
                            file=info.context.FILES,
                            project_posting=project_posting)

        if not resource.is_valid:
            return UserUpload(success=False, errors=resource.errors)

        uploader = Uploader().upload(user, resource)

        return UserUpload(success=uploader.success,
                          errors=uploader.errors,
                          attachment=uploader.attachment)


class UploadMutation(ObjectType):
    upload = UserUpload.Field()


class UploadTypeConfiguration(ObjectType):
    content_types = graphene.NonNull(graphene.List(graphene.NonNull(graphene.String)))
    max_size = graphene.NonNull(graphene.Int)


class UploadConfiguration(ObjectType):
    content_types_configuration = graphene.NonNull(
        graphene.List(graphene.NonNull(UploadTypeConfiguration)))
    max_files = graphene.NonNull(graphene.Int)
    key = graphene.NonNull(AttachmentKey)


class UploadConfigurationQuery(ObjectType):
    upload_configurations = graphene.List(UploadConfiguration)

    def resolve_upload_configurations(self, info, **kwargs):
        return upload_configurations
