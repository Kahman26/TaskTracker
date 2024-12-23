from django.contrib.auth import get_user_model
from rest_framework import status, generics, serializers
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .serializers import UserRegistrationSerializer, LoginSerializer, UserSerializer


class UserRegistrationView(GenericAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [
        AllowAny
    ]
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
              "message": "User registered successfully"
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [
        AllowAny
    ]
    def post(self, request):
        """
        Login.
        """
        user = request.data #полученные данные для входа
        serializer = self.serializer_class(data=user) #эти данные прогоняем через сериализатор
        if serializer.is_valid(raise_exception=True):
            print(serializer.data)
            return Response({'tokens': serializer.data['tokens']}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class InfoAPIView(GenericAPIView):
    def post(self, request):
        token = request.data
        serializer = self.serializer_class(data=token)  # эти данные прогоняем через сериализатор
        if serializer.is_valid(raise_exception=True):
            token = Token.objects.filter(key=serializer.data.get("token"))
            if token:
                user = get_user_model().objects.filter(id=token.first().user.id)
                if user:
                    user = user.first()
                    user = UserSerializer(user)
                    return Response({'User': user.data}, status=status.HTTP_200_OK)
        return Response({'details': "Неверный токен"}, status=status.HTTP_400_BAD_REQUEST)

class UserUpdateAPIView(UpdateAPIView):
    serializer_class = UserSerializer





