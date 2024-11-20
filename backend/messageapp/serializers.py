from rest_framework import serializers
from authapp.serializers import ProfileSerializers
from .models import ChatMessage

class ChatMessageSerializer(serializers.ModelSerializer):
    receiver_profile = ProfileSerializers(read_only = True)
    sender_profile = ProfileSerializers(read_only = True)
    class Meta:
        model = ChatMessage
        fields = ['id', 'user', 'sender', 'sender_profile', 'receiver', 'receiver_profile', 'message', 'is_read', 'date']
