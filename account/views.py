# views.py
from rest_framework.generics import CreateAPIView, GenericAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .serializers import UserRegistrationSerializer, UserAuthenticationSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model, authenticate
from .serializers import UserAuthenticationSerializer
from datetime import timedelta
from django.shortcuts import render

CustomUser = get_user_model()


def home(request):
    return render(request, 'account/signin.html')

def login(request):
    return render(request, 'account/signup.html')

def resetpassword(request):
    return render(request, 'account/reset.html')

def forgotpassword(request):
    return render(request, 'account/forgot.html')


########################################  API
class UserRegistrationAPIView(CreateAPIView):
    serializer_class = UserRegistrationSerializer
class UserListAPIView(ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer

class UserAuthenticationAPIView(GenericAPIView):
    serializer_class = UserAuthenticationSerializer
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(request, username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            response_data = {
                'access_token': access_token,
                'user_id': user.id,
                'username': user.username,
            }
            return Response(response_data, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

