from django.urls import path, re_path
from knox import views as knox_views



from .views import LoginAPI, Register, ValidatePhoneSendOTP, ValidateOTP

app_name='auth_api'

urlpatterns = [
    re_path('validate-phone', ValidatePhoneSendOTP.as_view()),
    re_path('validate-otp', ValidateOTP.as_view()),
    re_path('register', Register.as_view()),

    re_path('login', LoginAPI.as_view()),

    re_path('logout', knox_views.LogoutView.as_view()),
]