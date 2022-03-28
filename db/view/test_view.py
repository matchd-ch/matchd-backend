from django.shortcuts import render

def test_view(request):
   return render(request, 'db/email/activation/body.html', context={'user': {'type': 'student', 'first_name': 'TEST'}})