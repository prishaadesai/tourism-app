from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import authenticate

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        if email and password:
            user = authenticate(email=email, password=password)
            if user is None:
                raise serializers.ValidationError("Invalid email or password.")
        else:
            raise serializers.ValidationError("Email and password are required.")
        
        data["user"] = user
        return data
    
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'password', 'role']
        extra_kwargs = {
            'password': {'write_only': True},
            'username': {'required': False} 
        }

    def create(self, validated_data):
        if CustomUser.objects.filter(email=validated_data['email']).exists():
            raise serializers.ValidationError({'Error': 'Email already in use'})

        
        validated_data['username'] = validated_data.get('username', validated_data['email'])

        account = CustomUser(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            role=validated_data['role'],
            username=validated_data['username']
        )

        account.set_password(validated_data['password'])
        account.save()
        return account