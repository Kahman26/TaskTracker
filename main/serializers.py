from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from main.models import Command, Task



class CommandSerializer(ModelSerializer):
    class Meta:
        model = Command
        fields = '__all__'


class TaskSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'date_end', 'command', 'is_complete', 'status', 'priority')



