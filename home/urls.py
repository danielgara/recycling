from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home.index'),
    path('about', views.about, name='home.about'),
    path('learn', views.learn, name='home.learn'),
    path('learn/recycling-bin-colors', views.l1, name='home.learn.l1'),
    path('learn/recyclable-vs-non-recyclable', views.l2, name='home.learn.l2'),
    path('learn/symbols-and-labels', views.l3, name='home.learn.l3'),
    path('experiencia', views.experience, name='home.experience'),
]
