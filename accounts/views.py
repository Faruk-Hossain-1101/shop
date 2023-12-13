from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer
from rest_framework.response import Response
from .models import User, OneTimePassword
from rest_framework import status
from .utils import send_code_to_user, get_tokens_for_user

import logging
logger = logging.getLogger(__name__)
logger = logging.getLogger('django')
logger_api = logging.getLogger('api')

class RegisterView(APIView):
    def post(self, request):
        if request.data['password'] != request.data['password2']:
            return Response({
                "status":"failed",
                "message":"Password not matched!"
            }, status=status.HTTP_406_NOT_ACCEPTABLE) 
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user = serializer.data
            send_code_to_user(user['email'])
            return Response({
                'status': "success",
                'data': user,
                'message': f"Hi {user['first_name']} thanks for signing up, a passcode has been send to your email, please verify first!",
            }, status=status.HTTP_201_CREATED)
        
        logger_api.info("Register Failed "+request.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserVerification(APIView):
    def get(self, request):
        email = request.query_params.get('Q')
        user = User.objects.filter(email=email).first()
        if user is None:
            return Response({
                "status": "failed",
                "message": f"{email} this email not exists!, please register first!",
            }, status=status.HTTP_404_NOT_FOUND)
        
        if user.is_verified:
            return Response({
                "status": "failed",
                "data": user.email,
                "message": f"{email} is already verified!",
            }, status=status.HTTP_208_ALREADY_REPORTED) 
        
        send_code_to_user(email)
        return Response({
            'status': 'success',
            'data': {'email': email},
            'message': f"Hello {user.first_name} new otp send to your mail!",
        }, status=status.HTTP_201_CREATED)
    
    def post(self, request):
        otp = request.data['otp']
        email = request.data['email']
        if otp is None:
            return Response({
                "status": 'failed',
                "message": 'Please provide a correct otp!',
            }, status=status.HTTP_404_NOT_FOUND)
        
        get_user_otp = OneTimePassword.objects.filter(otp=otp).first()
        user = User.objects.filter(email=email).first()

        if get_user_otp is None:
            return Response({
                "status": 'failed',
                "message": 'OTP not matched!',
            }, status=status.HTTP_404_NOT_FOUND)

        elif get_user_otp.user.email == email:
            user.is_verified = True
            user.save()
            return Response({
                "status": 'success',
                "tokens": get_tokens_for_user(get_user_otp.user),
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                "status": 'failed',
                "message": 'OTP not matched!',
            }, status=status.HTTP_404_NOT_FOUND)


class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user  = User.objects.filter(email=email).first()

        if user is None:
            return Response({
                "status": 'failed',
                "message": 'User not found!',
            }, status=status.HTTP_404_NOT_FOUND)
        
        if not user.check_password(password):
            return Response({
                "status": 'failed',
                "message": 'Incorrect password!',
            }, status=status.HTTP_403_FORBIDDEN)
        if not user.is_verified :
            return Response({
                "status": 'failed',
                "message": 'User email is not verified, please verify first!',
            }, status=status.HTTP_403_FORBIDDEN)

        
        return Response({
            "status": 'success',
            "tokens": get_tokens_for_user(user),
        }, status=status.HTTP_200_OK)
    

