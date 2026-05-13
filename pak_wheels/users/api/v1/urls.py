from django.urls import path
from .views import signup, login, verify_otp, resend_otp

urlpatterns = [
    path('signup/', signup.SignupView.as_view(), name='signup'),
    path('login/', login.LoginView.as_view(), name='login'),
    path('verify-otp/', verify_otp.VerifyOTPView.as_view(), name='verify-otp'),
    path('resend-otp/', resend_otp.ResendOTPView.as_view(), name='resend-otp'),
]
