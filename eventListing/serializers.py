from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework import serializers
from events.models import OTP
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

# Register Serializer

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def validate_email(self, value):
        # Check if email is already registered
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(('Email is already registered.'))
        return value

    def create(self, validated_data):
        validated_data['is_active'] = False  # Set is_active to False by default
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            is_active=validated_data['is_active']
        )
        return user
    



User = get_user_model()

class OTPRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Invalid email.")
        return value

class OTPVerificationSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=6)
    new_password = serializers.CharField()

    def validate_otp(self, value):
        user = self.context['request'].user
        otp_obj = OTP.objects.filter(user=user).last()

        if not otp_obj:
            raise serializers.ValidationError("OTP verification failed.")
        
        if value != otp_obj.otp:
            raise serializers.ValidationError("Invalid OTP.")

        return value
