from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^$', views.index, name='datasubmission.index'),
    url(r'success', views.success, name='datasubmission.success'),
]
