from django.http import HttpResponse
from django.urls import path


def test(request):

    return HttpResponse(b"teste")


urlpatterns = [path("test", test)]
