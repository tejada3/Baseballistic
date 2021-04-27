from django.conf.urls import url
from django.urls import path
from django.contrib import admin
from Baseball import views



urlpatterns = [
    path('', views.home_page, name='homepage'),
    path('hit/', views.hitting_info, name='display'),
    path('pitch/', views.piching_info, name='pitch'),
    path('team_stats/<str:pk>', views.team_stats, name='team_stats')




]