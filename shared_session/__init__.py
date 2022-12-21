from django.urls import include, path
from . import views

urlpatterns = [
    path('<message>.js', views.shared_session_view, name='share'),
]

urls = urlpatterns, 'shared_session', 'shared_session'
