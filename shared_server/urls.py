"""shared_server URL configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
"""

from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic.base import TemplateView


def static_page(name, path=None):
    '''Render a static extension of the base template

    This function creates a url and a View for a mostly static
    template with the titles and navigation elements from
    `base.html`. It's for rendering things like "About" and "Contact"
    pages without duplicating elements from the site template.
    '''
    if path is None:
        path = "^{}$".format(name)
    url_name = name
    template_name = name + ".html"
    return url(
        path,
        TemplateView.as_view(template_name=template_name),
        name=url_name,
    )


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^datasubmission/', include('datasubmission.urls')),
    static_page('index', path=r'^$'),
    static_page('about'),
    static_page('contact'),
    static_page('submission'),
    static_page('documents'),
    url(
        r'^data_submission/',
        TemplateView.as_view(template_name='data_submission.html'),
        name='data_submission',
    )
]
