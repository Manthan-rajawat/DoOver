from django.contrib import admin
from django.urls import path
from .views import CreateUserApiView , LoginView,UserApiView,ChangePasswordView

urlpatterns = [
    path('signup/', CreateUserApiView.as_view(),name="signup"),
    path('login/', LoginView.as_view(),name="login"),
    path('profile/', UserApiView.as_view(),name="profile"),
    path('change-password/', ChangePasswordView.as_view(),name="change-password"),
]
