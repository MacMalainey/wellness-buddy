from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^alexa/ask/$', views.alexa_ask)
]
