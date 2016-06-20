from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.ranking, name='ranking'),
    url(r'^atletas$', views.atletas, name='atletas'),
    url(r'^atletas/([a-z]-[0-9]{4})$', views.atleta, name='atleta'),
]
