from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('get_voice_query/', views.get_voice_query, name='get_voice_query'),
]
