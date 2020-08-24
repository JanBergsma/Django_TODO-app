from .views import index
from .apps import TodoConfig
from django.urls import path

app_name = TodoConfig.name

urlpatterns = [
    path('', index, name='index'),
]
