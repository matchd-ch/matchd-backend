from datetime import datetime

from django.contrib import auth
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse

from graphql_jwt.utils import jwt_payload, jwt_encode

from uritemplate import expand

from wagtail.admin.messages import error

from db.models.user import User


@login_required
def impersonate_view(request, user_id):
    redirect_url = reverse("wagtailusers_users:index")

    impersonator = request.user
    try:
        impersonated_user = get_user_model().objects.get(pk=user_id)

        payload = jwt_payload(impersonated_user)
        del payload["origIat"]
        payload["exp"] = datetime.utcnow() + settings.IMPERSONATION_TOKEN_DURATION_IN_S
        payload["action"] = "impersonate"
        payload["actor"] = impersonator.username

        impersonation_jwt = jwt_encode(payload)

        redirect_url = expand(settings.IMPERSONATION_REDIRECT_URI_TEMPLATE, token=impersonation_jwt)
        auth.logout(request)
    except User.DoesNotExist:
        error(request, f"Failed to impersonate user ${user_id}, user does not exist")

    return redirect(redirect_url)
