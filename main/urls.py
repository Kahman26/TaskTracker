from django.urls import path
from . import views
from .views import task_search_view

urlpatterns = [
    path('commands/', views.CommandAPIView.as_view()),
    path('tasks/', views.TaskAPIView.as_view()),
    path("task-search/", task_search_view, name="task_search"),
]
