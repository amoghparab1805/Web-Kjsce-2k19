from django.urls import path
from .views import *

urlpatterns = [
    path('sign-up/', SignUp.as_view(), name='signup'),
    path('update-user/', UpdateUser.as_view(), name='update_user'),
    path('add-expenditure/', AddExpenditure.as_view(), name='add_expenditure'),
    path('get-expenditures/uid=<uid>/', GetExpenditures.as_view(), name='get_expenditures'),
]