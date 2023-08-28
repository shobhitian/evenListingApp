from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer
from django.contrib.auth import login
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from knox.views import LogoutView
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.urls import reverse
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .serializers import RegisterSerializer, UserSerializer, OTPRequestSerializer, OTPVerificationSerializer
from .tokens import account_activation_token
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.views import View
from django.http import JsonResponse
from events.models import EventCategory

from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.tokens import default_token_generator
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import OTPRequestSerializer, OTPVerificationSerializer
from events.models import OTP
from django.contrib.auth import get_user_model
from .utils import generate_otp


User = get_user_model()



class ChangeStatusView(View):
    def post(self, request, pk):
        category = get_object_or_404(EventCategory, pk=pk)
        category.status = '2' if category.status == '1' else '1'  # Toggle between 'active' and 'inactive'
        category.save()
        
        response_data = {
            'success': True,
            'message': 'Status updated successfully.'
        }
        return JsonResponse(response_data)


class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Generate token for email verification
        token = account_activation_token.make_token(user)
        uid = user.pk

        # Build verification URL
        verification_url = reverse('activate-account')
        verification_url += f'?user_id={uid}&token={token}'
        verification_url = request.build_absolute_uri(verification_url)

        # Compose email
        subject = 'Account Verification'
        message = f'Thank you for registering. Please click the following link to verify your account: {verification_url}'
        from_email = 'your_email@example.com'
        recipient_list = [user.email]

        # Send verification email
        send_mail(subject, message, from_email, recipient_list)

        return Response({
            'message': 'User registered successfully. Please check your email for verification.',
        })
    


class ActivateAccountView(APIView):
    def get(self, request):
        user_id = request.GET.get('user_id')
        token = request.GET.get('token')

        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({'message': 'Invalid activation link.'}, status=400)

        if account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({'message': 'Account activated successfully.'})
        else:
            return Response({'message': 'Invalid activation link.'}, status=400)    


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        if not user.is_active:
            return Response({'message': 'Email verification is pending. Please verify your email before logging in.'}, status=403)

        login(request, user)
        return super(LoginAPI, self).post(request, format=None)



#logout api
class LogoutAPI(LogoutView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        # Perform any additional logout logic if needed
  # Call the parent's post method to perform the logout
        response = super(LogoutAPI, self).post(request, format=None)

        # Create a custom response message
        message = "Logged out successfully."

        # Add the message to the response
        response.data = {'detail': message}

        return response
    




from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

User = get_user_model()


class OTPRequestView(APIView):
    
    def post(self, request):
        serializer = OTPRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        user = User.objects.get(email=email)

        # Generate the OTP
        otp = generate_otp()  # Implement your own OTP generation logic

        # Save the OTP in the OTP model
        otp_obj = OTP.objects.create(user=user, otp=otp)

        # Send the OTP to the user's email
        from_email = 'your_email@example.com'
        recipient_list = [user.email]
        send_mail(email, otp, from_email, recipient_list)

        # Generate or retrieve the token for the user
        token, _ = Token.objects.get_or_create(user=user)
        

        return Response({'message': 'OTP has been sent.', 'token': token.key})


class OTPVerificationView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = OTPVerificationSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        # Get the validated data from the serializer
        validated_data = serializer.validated_data

        # Update the user's password with the new password
        user = request.user
        new_password = validated_data['new_password']
        
        # Verify the OTP
        otp = validated_data['otp']
        otp_obj = OTP.objects.filter(user=user, otp=otp).first()
        if not otp_obj:
            return Response({'error': 'Invalid OTP.'}, status=400)
        
        user.set_password(new_password)
        user.save()

        # Delete the OTP model after successful verification
        otp_obj.delete()

        return Response({'message': 'Password has been reset successfully.'})
