from django.shortcuts import render

# This module is used solely for email testing puroses.
# How to use: add a path to urls.py that points to the function in this module.

TEMPLATE_PATH = 'db/email/activation/resend/body.html'
CONTEXT_PROPS = {
    'name': 'Peter Lustig',
    'email': 'name@example.com',
    'message':
    'Praesent nonummy mi in odio. Aliquam lobortis. Morbi nec metus. Etiam feugiat lorem non metus.',
    'user': {
        'type': 'student',
        'first_name': 'Thomas',
        'last_name': 'Thomson'
    },
    'frontend_url': 'https://example.com',
    'path': 'path',
    'token': '323568914562',
    'job_posting': {
        'title': 'Title of Jobposting',
        'employee': {
            'user': {
                'first_name': 'Hans',
                'last_name': 'Hanson'
            }
        },
        'company': {
            'name': 'CompanyName'
        }
    },
    'job_posting_url': 'https://example.com/job_posting_url',
    'student': {
        'first_name': 'Petra',
        'last_name': 'Petrason'
    },
    'student_profile_url': 'https://example.com/student_profile_url',
    'project_posting': {
        'title': 'ProjectPostingTitle',
        'project_type': {
            'name': 'ProjectTypeName'
        },
        'student': {
            'user': {
                'first_name': 'Kim',
                'last_name': 'Schmidt'
            }
        }
    },
    'project_posting_url': 'https://example.com/project_posting_url',
}


def email_template_test_helper_view(request):
    return render(request, TEMPLATE_PATH, context=CONTEXT_PROPS)
