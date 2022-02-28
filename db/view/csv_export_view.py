from django.contrib.auth.decorators import login_required
from djqscsv import render_to_csv_response

from db.models import User


@login_required
def csv_view(request):
    qs = User.objects.select_related('company').values('id', 'first_name', 'last_name', 'email',
                                                       'type', 'company__name')
    return render_to_csv_response(qs)
