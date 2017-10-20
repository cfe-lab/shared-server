'''Middelware for adding keys to the request context
'''

from django.conf import settings


def publication_settings(req):
    return {
        'SUPPORT_PERSON': settings.SUPPORT_PERSON,
        'SUPPORT_EMAIL': settings.SUPPORT_EMAIL,
        'SUBMISSION_EXAMPLE_PAGE': settings.SUBMISSION_EXAMPLE_PAGE,
    }
