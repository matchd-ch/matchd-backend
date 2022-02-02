from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie


@csrf_exempt
@ensure_csrf_cookie
def csrf_view(request):
    return HttpResponse(status=204)    # pragma: no cover
