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
from craigslist import CraigslistHousing
 
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


class AddExpenditure(APIView):
    
    def post(self, request, *args, **kwargs):
        data = request.data

        amount = data['amount']
        date = data['date']
        date_object = datetime.strptime(date, '%Y-%m-%d').date()
        uid = data['uid']
        type = data['type']

        if(type!='income'):

            user = User.objects.get(username=uid)

            expenditure = Expenditure(
                amount=amount,
                type=type,
                date=date,
                user=user
            )
            expenditure.save()
        else:
            user = User.objects.get(username=uid)
            user.income = amount
            user.save()

        return JsonResponse({
            'message': 'Succcess'
        })
            

class GetExpenditures(APIView):

    def get(self, request, *args, **kwargs):

        uid = kwargs['uid']
        user = User.objects.get(username=uid)

        expenditures = Expenditure.objects.filter(user=user)

        expenditures_serializer = ExpenditureSerializer(expenditures, many=True)

        return JsonResponse(expenditures_serializer.data, safe=False)

class GetHousing(APIView):

    def post(self, request, *args, **kwargs):
        data = request.data
        city = data['city']
        max_price = data['max_price']
        city = city.lower()
        max_price = int(max_price)
        cl = CraigslistHousing(site=city, category='apa', filters={'max_price': max_price})
        results = cl.get_results(sort_by='newest', geotagged=True, limit=5)

        return JsonResponse(results)

