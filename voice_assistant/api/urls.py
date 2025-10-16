from django.urls import path
from . import views

urlpatterns = [
    path('translate_audio/', views.translate_audio, name='translate_audio'),
]
