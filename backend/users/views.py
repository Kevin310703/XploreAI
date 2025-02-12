# Create your views here.
import traceback
import requests
from rest_framework.exceptions import ValidationError
from rest_framework import generics, permissions, status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.conf import settings

from .models import CustomUser

from .utils.helper import validate_avatar
from .utils.email_sender import EmailSender
from .serializers import (CustomTokenObtainPairSerializer, ForgotPasswordSerializer, 
                          UserAvatarSerializer, UserProfileSerializer, UserSerializer)

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
@permission_classes([IsAuthenticated])
def logout_view(request):
    refresh_token = request.data.get("refresh")

    if not refresh_token:
        return Response({"error": "Refresh token is missing"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        token = RefreshToken(refresh_token)
        token.blacklist()  # Đưa token vào blacklist

        # Xóa refresh token trong database
        user = request.user
        if user.refresh_token:
            user.refresh_token = None
            user.save()

        return Response({"message": "Logged out successfully."}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": f"Invalid token: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def verify_email(token):
    """API xác thực email"""
    user = get_object_or_404(User, email_verification_token=token)

    if user.is_email_verified:
        return Response({"message": "Email is already verified."}, status=status.HTTP_400_BAD_REQUEST)

    user.is_email_verified = True
    user.save()
    return Response({"message": "✅ Email verified successfully!"}, status=status.HTTP_200_OK)

@api_view(["POST"])
def google_login(request):
    auth_code = request.data.get("code")

    if not auth_code:
        return Response({"error": "No authorization code provided"}, status=status.HTTP_400_BAD_REQUEST)

    # Exchange auth code for access token
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "code": auth_code,
        "grant_type": "authorization_code",
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
    }

    token_response = requests.post(token_url, data=data)
    token_json = token_response.json()

    if "access_token" not in token_json:
        return Response({"error": "Failed to get access token"}, status=status.HTTP_400_BAD_REQUEST)

    access_token = token_json["access_token"]

    # Get user info from Google API
    user_info_url = "https://www.googleapis.com/oauth2/v2/userinfo"
    user_info_response = requests.get(user_info_url, headers={"Authorization": f"Bearer {access_token}"})
    user_info = user_info_response.json()

    email = user_info.get("email")
    google_name = user_info.get("name", "")

    if not email:
        return Response({"error": "Failed to get user email"}, status=status.HTTP_400_BAD_REQUEST)

    # Check user existss
    user, created = CustomUser.objects.get_or_create(email=email)

    # If user existed, update refresh token
    if not created:
        user.refresh_token = str(RefreshToken.for_user(user))
    else:
        user.username = email.split("@")[0]
        user.google_name = google_name
        user.refresh_token = str(RefreshToken.for_user(user))
        email_sender.send_welcome_email(email, google_name) # Send welcome email

    user.save()
    return Response({
        "message": "Login successful",
        "user_id": user.id,
        "username": user.username,
        "email": user.email,
        "name": user.google_name,
        "access_token": str(RefreshToken.for_user(user).access_token),
        "refresh_token": user.refresh_token
    })

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