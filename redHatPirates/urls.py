from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('user-profile/', views.user, name='user_profile'),
    path('current-investments/', views.futureinvestments, name='current_investments'),
    path('past-investments/', views.dashboard, name='past_investments'),
    path('about-us/', views.dashboard, name='about_us'),
    path('customer-care/', views.dashboard, name='customer_care'),
    path('realestate/', views.realestate, name='realestate'),
]