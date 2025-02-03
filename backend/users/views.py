from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions, status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import ForgotPasswordSerializer, UserSerializer

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(self.request.data["password"])
        user.save()

class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]

@api_view(["POST"])
def logout_view(request):
    try:
        refresh_token = request.data["refresh"]
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({"message": "Logged out successfully."}, status=200)
    except Exception:
        return Response({"error": "Invalid token"}, status=400)

class ForgotPasswordView(generics.GenericAPIView):
    serializer_class = ForgotPasswordSerializer

    def post(self, request, *args, **kwargs):
        """API xử lý quên mật khẩu"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            success, message = serializer.save()
            if success:
                return Response({"message": "✅ New password has been sent to your email."}, status=status.HTTP_200_OK)
            else:
                return Response({"error": message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)