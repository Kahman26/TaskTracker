from django.urls import path
from . import views

urlpatterns = [
    path('commands/', views.CommandAPIView.as_view()),
    path('tasks/', views.TaskAPIView.as_view()),

]
