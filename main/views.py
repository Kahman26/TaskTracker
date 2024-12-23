from django.db.models import Count
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.response import Response

from main.models import Task, Command
from main.serializers import CommandSerializer, TaskSerializer



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











