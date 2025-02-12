# Create your views here.
import os
import traceback
from rest_framework.exceptions import ValidationError
from rest_framework import generics, permissions, status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from .utils.email_sender import EmailSender
from .serializers import (CustomTokenObtainPairSerializer, ForgotPasswordSerializer, 
                          UserAvatarSerializer, UserProfileSerializer, UserSerializer)

from .utils.helper import validate_avatar

User = get_user_model()
email_sender = EmailSender()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        try:
            user = serializer.save()
            user.set_password(self.request.data["password"])
            user.save()

        except Exception as e:
            print(traceback.format_exc())
            raise ValidationError(f"⚠️ Internal Server Error: {str(e)}")
    
class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]
    serializer_class = CustomTokenObtainPairSerializer

@api_view(["POST"])
def logout_view(request):
    refresh_token = request.data.get("refresh")
    if not refresh_token:
        return Response({"error": "Refresh token is missing"}, status=400)
    
    try:
        token = RefreshToken(refresh_token)
        token.blacklist()  # Đánh dấu token là đã hết hạn
        return Response({"message": "Logged out successfully."}, status=200)
    except Exception as e:
        return Response({"error": f"Invalid token: {str(e)}"}, status=400)

@api_view(["GET"])
def verify_email(request, token):
    """API xác thực email"""
    user = get_object_or_404(User, email_verification_token=token)

    if user.is_email_verified:
        return Response({"message": "Email is already verified."}, status=status.HTTP_400_BAD_REQUEST)

    user.is_email_verified = True
    user.save()
    return Response({"message": "✅ Email verified successfully!"}, status=status.HTTP_200_OK)

class ForgotPasswordView(generics.GenericAPIView):
    serializer_class = ForgotPasswordSerializer

    def post(self, request, *args, **kwargs):
        """API forgot password"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            success, message = serializer.save()
            if success:
                return Response({"message": "✅ New password has been sent to your email."}, status=status.HTTP_200_OK)
            else:
                return Response({"error": message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserProfileUpdateView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        serializer = UserProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profile updated successfully!", "data": serializer.data})
        return Response(serializer.errors, status=400)
    
class UserAvatarUpdateView(generics.UpdateAPIView):
    """
    API endpoint update avatar user.
    """
    serializer_class = UserAvatarSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        avatar = request.FILES.get("avatar")
        if not avatar:
            return Response({"error": "Avatar file is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Validate file avatar
            validated_avatar = validate_avatar(avatar)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        # Nếu user đã có avatar khác mặc định, xóa avatar cũ
        if user.avatar and user.avatar.name != "avatars/default_avatar.jpg":
            user.avatar.delete(save=False)
        
        # Cập nhật avatar mới
        user.avatar = validated_avatar
        user.save()
        
        serializer = self.get_serializer(user)
        return Response({"message": "Avatar updated successfully!", "data": serializer.data}, status=status.HTTP_200_OK)
    
class ChangePasswordView(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")

        # Validation for password
        if not user.check_password(old_password):
            return Response({"error": "Incorrect current password."}, status=status.HTTP_400_BAD_REQUEST)
        
        if len(new_password) < 8:
            return Response({"error": "New password must be at least 8 characters long."}, status=status.HTTP_400_BAD_REQUEST)

        if new_password == old_password:
            return Response({"error": "New password cannot be the same as the old password."}, status=status.HTTP_400_BAD_REQUEST)

        # Set new password
        user.set_password(new_password)
        user.save()

        return Response({"message": "Password changed successfully!"}, status=status.HTTP_200_OK)