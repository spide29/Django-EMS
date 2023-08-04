from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import get_user_model

class UserRegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser  # Use your custom user model here
        fields = ('username', 'email', 'phone_number', 'date_of_birth', 'password', 'confirm_password')
    def validate(self, data):
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        if password != confirm_password:
            raise serializers.ValidationError({"confirm_password": ["The passwords do not match."]})
        return data
    def create(self, validated_data):
        password = validated_data.pop('password')
        confirm_password = validated_data.pop('confirm_password')
        user = CustomUser(**validated_data)  # Use your custom user model here
        user.set_password(password)
        user.confirm_password = confirm_password
        user.save()
        return user
    
class UserAuthenticationSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
