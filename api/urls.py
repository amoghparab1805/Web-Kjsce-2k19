from django.urls import path
from .views import *

urlpatterns = [
    path('sign-up/', SignUp.as_view(), name='signup'),
    path('send-mail-or-sms/', SendUserEmailOrSMS.as_view(), name='send_mail_or_sms'),
]