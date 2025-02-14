from django.contrib import admin
from django.urls import path
from .views import home, get_voice_query

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('get_voice_query/', get_voice_query, name='get_voice_query'),
]
