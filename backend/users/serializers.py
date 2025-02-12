import os
import uuid
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .utils.email_sender import EmailSender

User = get_user_model()
email_sender = EmailSender()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8, required=True)
    first_name = serializers.CharField(required=True, max_length=50)
    last_name = serializers.CharField(required=True, max_length=50)
    role = serializers.CharField(default="user", read_only=True)
    avatar = serializers.ImageField(required=False)

    class Meta:
        model = User
        fields = ["id", "username", "email", 
                  "first_name", "last_name", "google_name", 
                  "password", "role", "avatar"]

    def create(self, validated_data):
        """ Created user with hash password and role = 'user' """
        validated_data["email_verification_token"] = uuid.uuid4()
        password = validated_data.pop("password")
        user = User(**validated_data, role="user")
        user.set_password(password)
        user.save()

        verification_link = f"{os.getenv('FRONTEND_URL')}/?token={user.email_verification_token}/"
        email_sender.send_verification_email(user.email, verification_link)
        
        return user

class UserAvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['avatar']

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        """Check email exist"""
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("❌ Email not exist.")
        return value

    def save(self):
        """Created new password, save in database and send to user email"""
        email = self.validated_data["email"]
        user = User.objects.get(email=email)

        # New password
        new_password = email_sender.generate_password()
        user.set_password(new_password)
        user.save()

        # Send to user
        success, message = email_sender.send_reset_email(email, new_password)
        return success, message
    
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'avatar']

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Kiểm tra xác thực email trước khi cấp token"""
    
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user

        if not user.is_email_verified:
            raise serializers.ValidationError("⚠️ Your email has not been verified! Please check your inbox.")

        return data