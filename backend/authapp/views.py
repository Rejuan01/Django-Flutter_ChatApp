from rest_framework.decorators import api_view
from rest_framework import status, generics
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Profile

class RegisterView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()       #used saved in db
            new_user = User.objects.get(username = request.data['username']) #retrive the user again
            new_user.set_password(request.data['password'])        # hash the password
            new_user.save()
            token = Token.objects.create(user = new_user)        #token created
            Profile.objects.create(user = new_user)             # a corresponding profile is created
            return Response(
                {
                    'token' : token.key,
                    'user' : serializer.data
                }
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        user = get_object_or_404(User, username = request.data['username'])
        if not user.check_password(request.data['password']):
            return Response({'details':'wrong credential'}, status=status.HTTP_404_NOT_FOUND)
        token, created = Token.objects.get_or_create(user=user) #get or create (if not already created anyhow)
        serializer = UserSerializer(user)  # not necessarily important in login process but need to structure the response data, consistancy and we should not show the raw data in response
        return Response(
            {
                'token':token.key,
                'user' : serializer.data
            }
        )
    


from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
    
class CheckTokenView(APIView):
    permission_classes = [IsAuthenticated] #only authenticated users can make this api call 
    authentication_classes = [TokenAuthentication, SessionAuthentication] # types of authentication used

    def get(self, request, *args, **kwargs):
        user = request.user     #get corresponding user for the token
        return Response(
            {
                'response' : 'the user email: {}'.format(user.email)  # We can also directly use .format(request.user.email)
            }
        )
    
from .serializers import ProfileSerializers

class ProfileDetail(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializers
    queryset = Profile.objects.all()     # base query, RetrieveUpdateAPIView retrive the specific profile for the pk