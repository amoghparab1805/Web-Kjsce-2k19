from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics, viewsets, permissions, status
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
import requests
import json
from .models import *
from .serializers import *

class SignUp(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        username = data['uid']
        display_name = data['providerData'][0]['displayName']
        email = data['providerData'][0]['email']
        phone_number = data['providerData'][0]['phoneNumber']
        photo_url = data['providerData'][0]['photoURL']
        provider_id = data['providerData'][0]['providerId']
        password = "pass@123"
        hashed_password = make_password(password)
        try:
            user = User.objects.get(username=username)
            if not user.display_name:
                user.display_name = data['providerData'][0]['displayName']
                user.save()
        except User.DoesNotExist:
            user = User(
                username=username,
                display_name=display_name,
                email=email,
                phone_number=phone_number,
                password=hashed_password,
                photo_url=photo_url,
                provider_id=provider_id
            )
            user.save()
        response = requests.post("https://red-hat-pirates.herokuapp.com/api/auth/token/login/", data={'username':username, 'password':password})
        token = response.json()
        return JsonResponse({
            'Success': 'Success',
            'user': user.username, # TODO : Make serializer for user
            'token': token["auth_token"]
        })
