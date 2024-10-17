from django.urls import path
from .views import HelloWorld

urlpatterns = [
    path('api/hello/', HelloWorld.as_view(), name='hello_world'),
]
