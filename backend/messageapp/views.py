
from django.contrib.auth.models import User
from .models import ChatMessage
from .serializers import ChatMessageSerializer
from authapp.serializers import ProfileSerializers
from rest_framework.permissions import IsAuthenticated
from authapp.models import Profile
from rest_framework import generics, status
from django.db.models import Subquery, Q, OuterRef
from rest_framework.response import Response

class MyInboxView(generics.ListAPIView):
    serializer_class = ChatMessageSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        messages = ChatMessage.objects.filter(
            id__in = Subquery(
                User.objects.filter(
                    Q(sender__receiver = user_id) | Q(receiver__sender = user_id)
                ).distinct().annotate(
                    last_msg = Subquery(
                        ChatMessage.objects.filter(
                            Q(sender = OuterRef('id'), receiver = user_id) |
                            Q(receiver = OuterRef('id'), sender = user_id)
                        ).order_by('-id')[:1].values_list('id', flat = True)
                    )
                ).values_list('last_msg', flat=True).order_by("-id")
            ).order_by("-id")
        )
        return messages

class GetMessagesView(generics.ListAPIView):
    serializer_class = ChatMessage

    def get_queryset(self):     
        sender_id = self.kwargs['sender_id']     #get sender and receiver id from the url
        receiver_id = self.kwargs['receiver_id']

        messages = ChatMessage.objects.filter(
            sender__in = [sender_id, receiver_id],  #check for which messages sender and receiver matches with expected IDs
            receiver__in = [sender_id, receiver_id]
        )
        return messages
    
class SendMessageView(generics.CreateAPIView):
    serializer_class = ChatMessageSerializer 

class SearchUserView(generics.ListAPIView):
    serializer_class = ProfileSerializers
    queryset = Profile.objects.all()    #base query
    #permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        username = self.kwargs['username']
        #logged_in_user = self.request.user
        users = Profile.objects.filter(
            Q(user__username__icontains = username) | Q(user__email__icontains = username) | Q(full_name__icontains = username) 
        )

        if not users.exists():
            return Response(
                {'details' : 'No user found'}, 
                status=status.HTTP_404_NOT_FOUND 
            )
        serilaizer = self.get_serializer(users, many = True)
        return Response(serilaizer.data)
    