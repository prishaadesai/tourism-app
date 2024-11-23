from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .models import CustomUser
from .serializers import CustomUserSerializer, UserLoginSerializer
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
from django.http import HttpResponse

def curuser(request):
    return HttpResponse(request.user.email)

class UserRegistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        account = serializer.save()
        
        token = Token.objects.create(user=account)
        return token  

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        token = Token.objects.get(user=serializer.instance).key  
        return Response({
            'response': 'Account has been created',
            'token': token,
        });


class UserLoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        
        user = authenticate(request, email=email, password=password)

        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})

        return Response({'error': 'Invalid credentials'}, status=400)
    
