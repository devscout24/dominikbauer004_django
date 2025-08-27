from django.conf import settings
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

# Create your views here.
import jwt
from apps.User.models import CustomUser
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status, viewsets, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.tokens import RefreshToken, TokenError


from .serializers import RegisterSerializer, PasswordResetRequestSerializer

# Create your views here.

class BaseAPIView(APIView):
    
    def success_response(self, message="Thank you for your request", data=None, status_code= status.HTTP_200_OK):
        return Response(
            {
            "success": True,
            "message": message,
            "status_code": status_code,
            "data": data or {}
            }, 
            status=status_code )
        
    def error_response(self, message="I am sorry for your request", data=None, status_code= status.HTTP_400_BAD_REQUEST):
        return Response(
            {
            "success": False,
            "message": message,
            "status_code": status_code,
            "data": data or {}
            }, 
            status=status_code )    
        
class RegisterView(BaseAPIView):
    permission_classes= [AllowAny]
    authentication_classes= []
    
    def post(self, request):
        serializer=  RegisterSerializer(data= request.data)
        
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return self.success_response("User Registered successfully", data= serializer.data, status_code=status.HTTP_201_CREATED)
        
        except ValidationError as e:
            return self.error_response("Validation Error", data=e.detail)
        
        except Exception as e:
            return self.error_response("An error occurred", data= str(e), status_code= status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
class LoginView(BaseAPIView):
    permission_classes = [AllowAny]
    authentication_classes= []

    def post(self, request):
        try:
            customer_number = request.data.get('customer_number')
            password = request.data.get('password')

            if not customer_number or not password:
                raise ValidationError({
                    "customer_number": ["This field is required."],
                    "password": ["This field is required."]
                })

            # First check if user exists and get active status
            try:
                user = CustomUser.objects.get(customer_number=customer_number)
                user_exists = True
                is_active_status = user.is_active
            except CustomUser.DoesNotExist:
                user_exists = False
                is_active_status = False

            # If user exists but is inactive, return immediately
            if user_exists and not is_active_status:
                return self.error_response(
                    message="Account inactive",
                    data={
                        "debug": {
                            "user_exists": True,
                            "is_active": False,
                            "auth_attempted": False
                        },
                        "detail": "Your account is not active. Please contact support."
                    },
                    status_code=status.HTTP_403_FORBIDDEN
                )

            # Proceed with authentication only if account is active or doesn't exist
            user = authenticate(request, customer_number=customer_number, password=password)

            if not user:
                return self.error_response(
                    message="Authentication failed",
                    data={
                        "debug": {
                            "user_exists": user_exists,
                            "is_active": is_active_status,
                            "auth_failed": True
                        },
                        "detail": "Invalid customer number or password."
                    },
                    status_code=status.HTTP_400_BAD_REQUEST
                )

            # Generate tokens for successful login
            refresh = RefreshToken.for_user(user)

            return self.success_response(
                message="Login successful",
                data={
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                    "debug": {
                        "user_exists": True,
                        "is_active": True,
                        "auth_success": True
                    }
                }
            )

        except ValidationError as e:
            return self.error_response(
                message="Validation error",
                data=e.detail,
                status_code=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return self.error_response(
                message="Server error",
                data={"error": str(e)},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
            
class LogoutView(BaseAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return self.error_response(
                    "Refresh token is required",
                    status_code=status.HTTP_400_BAD_REQUEST
                )

            token = RefreshToken(refresh_token)
            token.blacklist() 

            return self.success_response(
                "Logged out successfully",
                status_code=status.HTTP_200_OK
            )

        except Exception as e:
            return self.error_response(
                "Logout failed",
                data=str(e),
                status_code=status.HTTP_400_BAD_REQUEST
            )
            
            
class RequestPasswordResetView(BaseAPIView):
    permission_classes = [AllowAny]  # Allow any user
    
    def post(self, request):
        serializer= PasswordResetRequestSerializer(data= request.data)
        
        if serializer.is_valid():
            serializer.save()
            return self.success_response("Password reset request created successfully", data= serializer.data, status_code= status.HTTP_201_CREATED)         
        
        return self.error_response("Validation error", data= serializer)