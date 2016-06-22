from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<message>.+).js$', views.shared_session_view, name='share'),
]

urls = urlpatterns, 'shared_session', 'shared_session'
