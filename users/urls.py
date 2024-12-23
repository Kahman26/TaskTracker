from django.urls import path
from .views import UserRegistrationView, LoginAPIView, InfoAPIView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('info/', InfoAPIView.as_view(), name='info'),
]
