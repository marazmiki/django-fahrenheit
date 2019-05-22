from django.contrib import admin
from django.http import HttpResponse
from django.urls import path


def view(content):
    def inner(request):
        return HttpResponse(content)
    return inner


urlpatterns = [
    path('admin/', admin.site.urls),
    path('page/', view('Just a page')),
    path('forbidden/in/ru/', view('Telegram rulz!')),
    path('', view('Index')),
]
