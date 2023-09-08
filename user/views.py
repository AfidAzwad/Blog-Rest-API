from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from .serializers import *
from .emails import send_otp_via_email
from rest_framework_simplejwt.tokens import RefreshToken



class LoginAPI(APIView):
    def post(self, request):
        try:
            data = request.data
            user = User.objects.filter(email=data['email']).first()
            if not user:
                response_dict = {
                    'status' : 400,
                    'message' : 'Wrong credentials!',
                    'data' : {},
                }
                return Response(response_dict)
            
            if not user.is_active:
                response_dict = {
                    'status' : 400,
                    'message' : 'Please activate user with OTP to login!',
                    'data' : {},
                }
                return Response(response_dict)
            
            refresh_token = RefreshToken.for_user(user)
            response = Response()
            response.set_cookie(key='refresh_token', value=str(refresh_token), httponly=True)
            response.data = {
                'token': str(refresh_token.access_token)
                    }
            return response
        except Exception as e:
            return e
        
        
class LogoutAPI(APIView):
    def post(self, _):
        response = Response()
        response.delete_cookie(key='refresh_token')
        response.data = {
            'message' : 'logout successful!'
        }
        return response


class RegisterAPI(APIView):
    def post(self, request):
        try:
            data = request.data
            data['is_active'] = False
            serializer = UserSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                send_otp_via_email(serializer.data['email'])
                response_dict = {
                    'status' : 200,
                    'message' : 'Registration successfull! check email',
                    'data' : serializer.data,
                }
                return Response(response_dict)
            response_dict = {
                'status' : 400,
                'message' : 'Something went wrong !',
                'data' : serializer.errors,
            }
            return Response(response_dict)
        except Exception as e:
            return e
    
    
class VerifyOTP(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = VerifyAccountSerializer(data=data)
            if serializer.is_valid():
                email = serializer.data['email']
                otp = serializer.data['otp']
                
                user = User.objects.filter(email=email).first()
                if not user:
                    response_dict = {
                        'status' : 400,
                        'message' : 'Something went wrong !',
                        'data' : 'Invalid email!'
                    }
                    return Response(response_dict)
                if user.otp != otp:
                    response_dict = {
                        'status' : 400,
                        'message' : 'Something went wrong !',
                        'data' : 'Wrong OTP!'
                    }
                    return Response(response_dict)
                user.has_used = True
                user.is_active = True
                user.save()
                response_dict = {
                        'status' : 200,
                        'message' : 'Your account is verified!',
                        'data' : {},
                    }
                return Response(response_dict)
        except Exception as e:
            return e


class PasswordResetAPIView(APIView):
    def post(self, request):        
        try:
            data = request.data
            serializer = PasswordResetSerializer(data=data)
            if serializer.is_valid():
                user = User.objects.get(email=serializer.data['email'])
                if not user:
                    response_dict = {
                            'status' : 200,
                            'message' : 'User with this email does not exist!',
                            'data' : {},
                        }
                    return Response(response_dict)
                send_otp_via_email(serializer.data['email'])
                response_dict = {
                        'status' : 400,
                        'message' : 'A OTP has been sent to your email to reset password!',
                        'data' : {},
                    }
                return Response(response_dict)
        except Exception as e:
            return e


class PasswordConfirmAPIView(APIView):
    def post(self, request, uid):
        try:
            print(request.data)
            data = request.data
            user = User.objects.get(pk=uid)
            if user is not None and user.otp == data['otp']:
                new_password = data.get('new_password')
                confirm_new_password = data.get('confirm_new_password')

                if new_password != confirm_new_password:
                    return Response({'error': 'New passwords do not match.'}, status=status.HTTP_400_BAD_REQUEST)

                user.set_password(new_password)
                user.save()
                return Response({'message': 'Password has been successfully reset.'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid OTP or user.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return e
