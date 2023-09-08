from django.urls import path, include
from .views import LoginAPI, LogoutAPI, RegisterAPI, VerifyOTP, PasswordResetAPIView, PasswordConfirmAPIView


urlpatterns = [
     path('api/user/login', LoginAPI.as_view(), name='login'),
     path('api/user/logout', LogoutAPI.as_view(), name='logout'),
     path('api/user/register', RegisterAPI.as_view(), name='register'),
     path('api/user/verify', VerifyOTP.as_view(), name='verify-otp'),
     path('api/user/password-reset', PasswordResetAPIView.as_view(), name='password-reset'),
     path('api/user/password-confirm/<uid>', PasswordConfirmAPIView.as_view(), name='password-confirm'),
]
