import json

from graphene_file_upload.django import FileUploadGraphQLView
from graphene_file_upload.utils import place_files_in_operations


def remove_multiple_uploads(file_list):
    keys_to_delete = list(file_list.keys())
    keys_to_delete.sort()
    keys_to_delete.pop(0)
    for key in keys_to_delete:
        del file_list[key]
    return file_list


class GraphQLView(FileUploadGraphQLView):
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        response = self._delete_cookies_on_response_if_needed(request, response)
        return response

    def parse_body(self, request):
        """Handle multipart request spec for multipart/form-data"""
        content_type = self.get_content_type(request)
        if content_type == 'multipart/form-data':
            # workaround to avoid multiple file uploads
            operations = json.loads(request.POST.get('operations', '{}'))
            files_map = json.loads(request.POST.get('map', '{}'))
            files_map = remove_multiple_uploads(files_map)
            files = remove_multiple_uploads(request.FILES)
            return place_files_in_operations(
                operations,
                files_map,
                files
            )
        return super().parse_body(request)

    def _delete_cookies_on_response_if_needed(self, request, response):
        data = self.parse_body(request)
        body = self.get_graphql_params(request, data)[0]
        if body and ('logout' in body or 'deleteAccount' in body):
            response.delete_cookie('JWT')
        return response
