from django.urls import path
from .views import *

urlpatterns = [
    path('sign-up/', SignUp.as_view(), name='signup'),
    path('update-user/', UpdateUser.as_view(), name='update_user'),
]