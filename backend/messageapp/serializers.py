from rest_framework import serializers
from .models import Profile

class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        models = Profile
        fields = ['id', 'user', 'sender', 'receiver', 'message', 'is_read', 'date']