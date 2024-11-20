from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Profile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email')


class ProfileSerializers(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'user', 'full_name', 'image']
        