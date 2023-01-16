from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse

from graphql_auth.utils import get_token

from uritemplate import expand

from wagtail.admin.messages import error

from db.models.user import User


@login_required
def impersonate_view(request, user_id):
    redirect_url = reverse("wagtailusers_users:index")

    impersonator = request.user
    try:
        impersonated_user = get_user_model().objects.get(pk=user_id)
        expiration = datetime.now() + timedelta(hours=1)

        impersonation_jwt = get_token(impersonated_user,
                                      "impersonate",
                                      exp=expiration.utctimetuple(),
                                      actor=impersonator.username)
        redirect_url = expand(settings.IMPERSONATION_REDIRECT_URI_TEMPLATE, token=impersonation_jwt)
    except User.DoesNotExist:
        error(request, f"Failed to impersonate user ${user_id}, user does not exist")

    return redirect(redirect_url)
