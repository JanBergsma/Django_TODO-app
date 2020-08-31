from .views import IndexView, ClearDeletedView, CreateView, UpdateView
from .apps import TodoConfig
from django.urls import path

app_name = TodoConfig.name

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('create', CreateView.as_view(), name='create'),
    path('update', UpdateView.as_view(), name='update'),
    path('clear-completed', ClearDeletedView.as_view(), name='clear-completed'),
]
