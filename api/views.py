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

class SignUp(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        username = data['uid']
        display_name = data['displayName']
        email = data['email']
        phone_number = data['phoneNumber']
        photo_url = data['photoURL']
        provider_id = data['providerId']
        password = "pass@123"
        hashed_password = make_password(password)
        try:
            user = User.objects.get(username=username)
            if not user.display_name:
                user.display_name = data['displayName']
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
            'message': 'Success',
            'user': user.username, # TODO : Make serializer for user
            'token': token["auth_token"]
        })

class SendUserEmailOrSMS(APIView):
    def post(self, request, *args, **kwargs):
        sender = User.objects.get(username = request.user.username)
        user = User.objects.get(display_name = request.data.display_name)
        if not user.email:
            # Send SMS
            pass
        if not user.phone_number:
            subject = 'Meeting with: ' + sender.username
            message = 'Open this link to join the call. http://localhost:5000/receive-call . Enter the password: pass@123'
            from_email = settings.EMAIL_HOST_USER
            to_list = [email, settings.EMAIL_HOST_USER, ]
            send_mail(subject, message, from_email, to_list, fail_silently=True)
        return JsonResponse({'message': 'Mail or SMS sent'})
