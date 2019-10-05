from rest_framework import serializers
from. models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'phone_number',
            'provider_id',
            'photo_url',
            'email',
            'display_name',
            'age',
            'gender',
            'username'
        ]

class ExpenditureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expenditure
        fields = [
            'amount',
            'type',
            'date',
            'user_id'
        ]