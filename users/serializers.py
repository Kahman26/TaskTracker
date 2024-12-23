from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.validators import UniqueValidator


class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        return user


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=68, write_only=True)
    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = get_user_model().objects.get(username=obj["username"])
        tokens = user.tokens()

        return {"refresh": tokens["refresh"], "access": tokens["access"]}


    class Meta:
        model = get_user_model()
        fields = ["username", "password","tokens"]

    def validate(self, attrs):
        user = get_user_model().objects.filter(username=attrs.get("username")).first()
        if user:
            if user.check_password(attrs.get("password")):
                return attrs

            if not user.is_active:
                raise AuthenticationFailed("Аккаунт отключен, обратитесь в поддержку.")

        raise AuthenticationFailed("Не правильные данные.")

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(validators= [UniqueValidator(queryset=get_user_model().objects.all())])
    class Meta:
        model = get_user_model()
        fields = ["first_name", "last_name", "username"]




