import debug_toolbar
from django.conf import settings
from django.http import HttpResponse
from django.urls import include, path
from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt
from django.core.management import call_command

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from graphql_jwt.decorators import jwt_cookie

from api.views import csrf_view, GraphQLView, AttachmentServeView


urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('admin/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),
    path('graphql/', jwt_cookie(GraphQLView.as_view(graphiql=settings.GRAPHIQL_ENABLED))),
    path('attachment/<int:attachment_id>/', AttachmentServeView.as_view(), name='attachment_serve'),
    path('attachment/<int:attachment_id>/<str:stack>/', AttachmentServeView.as_view(), name='attachment_serve_image'),
    path('csrf/', csrf_view),
]


if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns


    def indexing_debug_view(request):
        html = '<html><body>Indexing complete</body></html>'
        call_command('update_index')

        return HttpResponse(html)

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
        path('introspection/', csrf_exempt(GraphQLView.as_view(graphiql=settings.GRAPHIQL_ENABLED))),
        path('index/', indexing_debug_view),
    ]

urlpatterns = urlpatterns + [
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    path("", include(wagtail_urls)),

    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    path("pages/", include(wagtail_urls)),
]
