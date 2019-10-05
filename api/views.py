from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics, viewsets, permissions, status
from django.http import HttpResponse, JsonResponse
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
import requests
import json
from .models import *
from .serializers import *
from backend import settings
from .serializers import *
from datetime import datetime

class SignUp(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        username = data['uid']
        display_name = data['displayName']
        email = data['email']
        phone_number = data['phoneNumber']
        photo_url = data['photoURL']
        if(photo_url == None):
            photo_url = ''
        provider_id = data['providerId']
        password = "pass@123"
        hashed_password = make_password(password)
        age = data['age']
        gender = data['gender']
        try:
            user = User.objects.get(username=username)
            if not user.display_name:
                user.display_name = data['displayName']
                user.save()
            is_new_user = False
        except User.DoesNotExist:
            user = User(
                username=username,
                display_name=display_name,
                email=email,
                phone_number=phone_number,
                password=hashed_password,
                photo_url=photo_url,
                provider_id=provider_id,
                age=age,
                gender=gender
            )
            user.save()
            is_new_user = True      

        response = requests.post("https://red-hat-pirates.herokuapp.com/api/auth/token/login/", data={'username':username, 'password':password})
        token = response.json()

        serializer = UserSerializer(user)
        return JsonResponse({
            'message': 'Success',
            'user': serializer.data,
            'token': token["auth_token"],
            'is_new_user': is_new_user
        })

class UpdateUser(APIView):

    def post(self, request, *args, **kwargs):
        data = request.data
        uid = data['uid']
        display_name = data['displayName']
        age = data['age']
        gender = data['gender']

        try:
            user = User.objects.get(username=uid)
            user.display_name = display_name
            user.age = age
            user.gender = gender
            user.save()

        except User.DoesNotExist:
            return JsonResponse({
                'message' : 'Authentication Error'
            })

        return JsonResponse({
            'message': 'Success'
        })

        
# Add Expenditure
# 

class AddExpenditure(APIView):
    
    def post(self, request, *args, **kwargs):
        data = request.data

        amount = data['amount']
        date = data['date']
        date_object = datetime.strptime(date, '%Y-%m-%d').date()
        uid = data['uid']
        expenditure_type = data['expenditure_type']

        user = User.objects.get(username=uid)

        expenditure = Expenditure(
            amount=amount,
            expenditure_type=expenditure_type,
            date=date,
            user=user
        )
        expenditure.save()

        return JsonResponse({
            'message': 'Succcess'
        })
            

class GetExpenditures(APIView):

    def post(self, request, *args, **kwargs):

        data = request.data

        uid = data['uid']
        user = User.objects.get(username=uid)

        necessities_expenditures = Expenditure.objects.filter(user=user, expenditure_type='necessities')
        shopping_expenditures = Expenditure.objects.filter(user=user, expenditure_type='shopping')
        bills_expenditures = Expenditure.objects.filter(user=user, expenditure_type='bills')
        tax_expenditures = Expenditure.objects.filter(user=user, expenditure_type='tax')
        insurance_expenditures = Expenditure.objects.filter(user=user, expenditure_type='insurance')

        necessities_expenditures_serializer = ExpenditureSerializer(necessities_expenditures, many=True)
        shopping_expenditures_serializer = ExpenditureSerializer(shopping_expenditures, many=True)
        bills_expenditures_serializer = ExpenditureSerializer(bills_expenditures, many=True)
        tax_expenditures_serializer = ExpenditureSerializer(tax_expenditures, many=True)
        insurance_expenditures_serializer = ExpenditureSerializer(insurance_expenditures, many=True)

        return JsonResponse({
            'necessities': necessities_expenditures_serializer.data,
            'shopping': shopping_expenditures_serializer.data,
            'bills': bills_expenditures_serializer.data,
            'tax': tax_expenditures_serializer.data,
            'insurance': insurance_expenditures_serializer.data,
        })
