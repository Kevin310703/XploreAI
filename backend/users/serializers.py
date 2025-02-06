from rest_framework import serializers
from django.contrib.auth import get_user_model
from .utils.email_sender import EmailSender

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8, required=True)
    first_name = serializers.CharField(required=True, max_length=50)
    last_name = serializers.CharField(required=True, max_length=50)
    role = serializers.CharField(default="user", read_only=True)
    avatar = serializers.ImageField(required=False)

    class Meta:
        model = User
        fields = ["id", "username", "email", 
                  "first_name", "last_name", "password", 
                  "role", "avatar"]

    def create(self, validated_data):
        """ Created user with hash password and role = 'user' """
        password = validated_data.pop("password")
        user = User(**validated_data, role="user")
        user.set_password(password)
        user.save()
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
        new_password = EmailSender.generate_password()
        user.set_password(new_password)
        user.save()

        # Send to user
        success, message = EmailSender.send_reset_email(email, new_password)
        return success, message
    
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'avatar']