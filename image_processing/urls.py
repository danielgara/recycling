from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='scanner.index'),
    path('save', views.save, name='scanner.save'),
]
