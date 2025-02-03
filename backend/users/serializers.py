from rest_framework import serializers
from django.contrib.auth import get_user_model

from .utils.email_sender import EmailSender

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8, required=True)
    first_name = serializers.CharField(required=True, max_length=50)
    last_name = serializers.CharField(required=True, max_length=50)
    role = serializers.CharField(default="user", read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "password", "role"]

    def create(self, validated_data):
        """Tạo user với mật khẩu đã được băm và role mặc định là 'user'"""
        password = validated_data.pop("password")
        user = User(**validated_data, role="user")
        user.set_password(password)
        user.save()
        return user

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        """Kiểm tra email có tồn tại trong hệ thống không"""
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("❌ Email không tồn tại trong hệ thống.")
        return value

    def save(self):
        """Tạo mật khẩu mới, cập nhật vào database và gửi email"""
        email = self.validated_data["email"]
        user = User.objects.get(email=email)

        # Tạo mật khẩu mới
        new_password = EmailSender.generate_password()
        user.set_password(new_password)  # Cập nhật mật khẩu
        user.save()

        # Gửi email cho người dùng
        success, message = EmailSender.send_reset_email(email, new_password)
        return success, message