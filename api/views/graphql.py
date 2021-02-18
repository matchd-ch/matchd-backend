from graphene_file_upload.django import FileUploadGraphQLView


class GraphQLView(FileUploadGraphQLView):
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        response = self._delete_cookies_on_response_if_needed(request, response)
        return response

    def _delete_cookies_on_response_if_needed(self, request, response):
        data = self.parse_body(request)
        body = self.get_graphql_params(request, data)[0]
        if body and ('logout' in body or 'deleteAccount' in body):
            response.delete_cookie('JWT')
        return response
