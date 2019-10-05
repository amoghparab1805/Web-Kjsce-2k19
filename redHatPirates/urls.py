from django.urls import path
from . import views

app_name = 'redhat'
urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
]