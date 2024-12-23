import datetime
from django.db.models import Count
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.response import Response

from main.models import Task, Command
from main.serializers import CommandSerializer, TaskSerializer

from .forms import TaskSearchForm
from main.yougile_api.yougile_api_main import YouGileAPI
from main.yougile_api.get_task import GetYouGileTask



class CommandAPIView(ListAPIView):
    serializer_class = CommandSerializer

    def get_queryset(self):

        return Command.objects.all()

class TaskAPIView(ListAPIView, CreateAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        commands = Command.objects.filter(members=self.request.user)
        return Task.objects.filter(command__in = commands)

    def post(self, request, *args, **kwargs):
        data = request.data  # полученные данные для входа
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            command = serializer.validated_data.get('command')
            if not command:
                user = request.user
                user_command = Command.objects.filter(member=user).annotate(count_member=Count('member').filter(count_member=1))
                if user_command:
                    command = user_command
                else:
                    command = Command.objects.create(title = 'Личная команда')
                    command.members.add(user)
                    command.save()
            serializer.data['author'] = request.user
            del serializer.data['command']
            task = Task.objects.create(**data)
            task.command = command
            task.save()
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)

        else:
            return Response({'detail': 'Неверные данные'}, status=status.HTTP_400_BAD_REQUEST)


def task_search_view(request):
    task_details = None
    error_message = None

    if request.method == "POST":
        form = TaskSearchForm(request.POST)
        if form.is_valid():
            task_title = form.cleaned_data["task_title"]

            # Логика работы с API YouGile
            try:
                # Замените данными вашего пользователя
                login = "kislyakim@gmail.com"
                password = "password1234"
                company_name = "adidas"

                # Аутентификация
                auth = YouGileAPI()
                company_id = auth.get_company_id(login, password, company_name)
                token = auth.get_token(login, password, company_id)

                # Работа с задачами
                tasks_api = GetYouGileTask(token)
                tasks = tasks_api.get_all_tasks()
                task = tasks_api.get_task_by_title(tasks, task_title)

                if task:
                    timestamp = datetime.datetime.fromtimestamp(task.get("timestamp", "Дата не указана") / 1000).strftime('%Y-%m-%d %H:%M:%S')
                    task_details = {
                        "title": task.get("title", "Без названия"),
                        "timestamp": timestamp,
                        "id": task.get("id", "Без ID"),
                        "description": task.get("description", "Без описания"),
                        "completed": "Да" if task.get("completed", False) else "Нет",
                        "archived": "Да" if task.get("archived", False) else "Нет",
                        "due_date": task.get("dueDate", "Без срока"),
                    }
                else:
                    error_message = f"Задача с названием '{task_title}' не найдена."
            except Exception as e:
                error_message = str(e)
    else:
        form = TaskSearchForm()

    return render(request, "task_search.html", {"form": form, "task_details": task_details, "error_message": error_message})








