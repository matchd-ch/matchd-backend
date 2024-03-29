import debug_toolbar
from django.conf import settings
from django.http import HttpResponse
from django.urls import include, path
from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt
from django.core.management import call_command

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from graphql_jwt.decorators import jwt_cookie

from api.views import GraphQLView, AttachmentServeView
from db.view.csv_export_view import csv_view
from db.view.impersonate_view import impersonate_view

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('admin/', include(wagtailadmin_urls)),
    path('admin/users/export', csv_view),
    path('admin/users/impersonate/<int:user_id>', impersonate_view, name="impersonate_url"),
    path('documents/', include(wagtaildocs_urls)),
    path('graphql/',
         csrf_exempt(jwt_cookie(GraphQLView.as_view(graphiql=settings.GRAPHIQL_ENABLED)))),
    path('attachment/<int:attachment_id>/', AttachmentServeView.as_view(), name='attachment_serve'),
    path('attachment/<int:attachment_id>/<str:stack>/',
         AttachmentServeView.as_view(),
         name='attachment_serve_image'),
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
