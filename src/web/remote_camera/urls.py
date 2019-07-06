from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('live_preview', views.live_preview, name='live_preview'),
    path('give_me_da_preview', views.give_me_da_preview, name='give_me_da_preview'),
]
