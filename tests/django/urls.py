from django.urls import path

from .view import test

urlpatterns = [path("test", test)]
